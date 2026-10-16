"""Pack downloaded Liquipedia sounds and icons into the few files the quiz loads.

Usage: PATCH=7.41 python3 pack.py <raw_dir> <manifest.json> <out_dir>

manifest.json:
{
  "heroes":  [{"n": "Abaddon", "i": "Abaddon_icon_dota2_gameasset.png"}, ...],   # display order
  "groups":  ["Consumables", "Attributes", ...],                                   # item group order
  "same":    [["Cheese", "Block of Cheese"], ...],     # optional: names that share one sound
  "entries": [{"t": "a", "h": "Abaddon", "n": "Mist Coil", "a": "<mp3>", "i": "<png>"},
              {"t": "i", "h": "Armor",   "n": "Black King Bar", "a": "<mp3>", "i": "<png>"}, ...]
}
t is "a" for a hero ability (h = hero) or "i" for an item (h = item group).
Audio is re-encoded to mono 64 kbps MP3 (max 8 s), icons to 128 px WebP (portraits 256 px),
then concatenated into packs. data.json records [pack, offset, length] for each sound and icon.
"""
import hashlib, io, json, os, subprocess, sys, tempfile
from datetime import date
from PIL import Image

PACK_LIMIT = 12 * 1024 * 1024
PATCH = os.environ.get("PATCH", "7.41")


def enc_audio(path):
    with tempfile.NamedTemporaryFile(suffix=".mp3") as t:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "44100",
                        "-b:a", "64k", "-t", "8", t.name], check=True)
        return open(t.name, "rb").read()


def enc_icon(path, size=128):
    im = Image.open(path).convert("RGBA")
    im.thumbnail((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=82)
    return b.getvalue()


def main(raw, manifest, out):
    os.makedirs(out, exist_ok=True)
    man = json.load(open(manifest, encoding="utf-8"))
    packs = {"a": [[]], "i": [[]]}
    sizes = {"a": [0], "i": [0]}

    def put(kind, data):
        if sizes[kind][-1] + len(data) > PACK_LIMIT:
            packs[kind].append([]); sizes[kind].append(0)
        p = len(packs[kind]) - 1
        ref = [p, sizes[kind][p], len(data)]
        packs[kind][p].append(data); sizes[kind][p] += len(data)
        return ref

    def icon(name, size=128):
        if name and os.path.exists(os.path.join(raw, name)):
            try:
                return put("i", enc_icon(os.path.join(raw, name), size))
            except Exception as e:
                print("skip icon", name, e)
        return None

    heroes = [{"n": h["n"], "i": icon(h.get("i"), 256)} for h in man["heroes"]]
    lst = []
    for it in man["entries"]:
        try:
            a = enc_audio(os.path.join(raw, it["a"]))
        except Exception as e:
            print("skip audio", it["a"], e); continue
        src = open(os.path.join(raw, it["a"]), "rb").read()
        entry = {"t": it["t"], "h": it["h"], "n": it["n"], "a": put("a", a),
                 "_h": hashlib.sha1(src).hexdigest()}
        ref = icon(it.get("i"))
        if ref: entry["i"] = ref
        lst.append(entry)

    # entries whose source sound is byte-identical (e.g. the three Healing Lotuses) share a group id,
    # so the quiz accepts any of their names
    by_hash = {}
    for e in lst:
        by_hash.setdefault(e.pop("_h"), []).append(e)
    gid = 0
    for group in by_hash.values():
        if len(group) > 1:
            for e in group: e["g"] = gid
            gid += 1
    # "same": lists of names whose sounds are different uploads of the same in-game cue
    for names in man.get("same", []):
        for e in lst:
            if e["n"] in names: e["g"] = gid
        gid += 1

    names = {"a": [], "i": []}
    total = 0
    for kind, prefix, ext in (("a", "audio", "mp3"), ("i", "icons", "webp")):
        for k, chunks in enumerate(packs[kind]):
            fn = f"{prefix}-{k}.{ext}"
            blob = b"".join(chunks)
            open(os.path.join(out, fn), "wb").write(blob)
            names[kind].append(fn); total += len(blob)
    data = {"patch": PATCH, "built": date.today().isoformat(), "source": "liquipedia.net",
            "bytes": total, "packs": names, "heroes": heroes, "groups": man["groups"], "list": lst}
    json.dump(data, open(os.path.join(out, "data.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    na = sum(1 for x in lst if x["t"] == "a"); ni = len(lst) - na
    print(f"{na} abilities, {ni} items, {len(heroes)} heroes, {total/1e6:.1f} MB in "
          f"{len(names['a'])} audio + {len(names['i'])} icon packs")


if __name__ == "__main__":
    main(*sys.argv[1:4])
