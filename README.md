# Dota 2 Audio Cue Quiz

A sound plays. Type the Dota 2 ability or item it belongs to.

An up-to-date take on Chudooder's 2018 quiz (chudooder.github.io/d2acq): every current hero through patch 7.41 (Kez, Largo, Ringmaster and Muerta included), plus item sounds and a browsable sound database.

## What's in it

- **Quiz**: a sound plays; type the ability or item it belongs to. Tick *Hero abilities*, *Items* or both before you start.
- **Heroes**: every hero (the Spirit Bear counts as its own hero) with each ability's icon and a player for its sound. Filter by hero or ability name.
- **Items**: every item with a sound, grouped as in the shop (plus neutral tiers), each with its icon and a player.

## How to play

- A sound plays when the round starts. Click the socket to hear it again.
- Type the name and pick it from the list (arrow keys + Enter, or click). Typing the exact name and pressing Enter also works.
- A right answer is worth 100 points, plus 20 for every answer in your current streak.
- **Hint** shows four choices; a right answer then scores one fifth.
- You have one life: a single wrong answer ends the run. The end screen plays back the sound that got you.
- A few items use the same in-game sound (Magic Stick and Magic Wand, Sange and Sange and Yasha, Desolator and Stygian Desolator, Cheese and Block of Cheese); either name counts.
- Best scores are kept separately for abilities only, items only, and both.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole site: markup, styles and script |
| `data.json` | Heroes, item groups, and every sound: name, hero or item group, and where its sound and icon sit in the packs |
| `audio-*.mp3` | Sounds, re-encoded to mono 64 kbps MP3 and concatenated |
| `icons-*.webp` | Ability and item icons (128 px) and hero portraits (256 px), WebP, concatenated |
| `build/pack.py` | Rebuilds the packs and `data.json` from downloaded Liquipedia files |

## Credits

Ability sounds and icons: [Liquipedia](https://liquipedia.net/dota2/Main_Page) (CC-BY-SA 3.0 for wiki content; game assets belong to Valve). Hero and ability data: OpenDota dotaconstants. Dota 2 is a trademark of Valve Corporation. This is a fan project and is not affiliated with Valve or Liquipedia.
