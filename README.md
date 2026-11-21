# DRIFTWICK — 1 island, 365 harbours, 0 anchors

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Jo3st4r/poster-place-20261121-bot/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Jo3st4r/poster-place-20261121-bot/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

**Competition:** make.fun `the-poster-for-a-place-that-i-2-20261121-0539` — "The Poster for a Place That Isn't There". Pool $50, top 20 entries. Entry closes 21 Nov 2026 15:39 WIB.

## The idea

**DRIFTWICK — the island that never stays put.** One island, 365 harbours,
0 anchors. It drifts with the currents, so no map ever shows it in the same
place twice — and its lighthouse is the only thing that never moves.

A golden-hour vintage travel poster: the place name in huge condensed type
across a cream sky, a low coral sun, one white lighthouse on a green drifting
island, and a sailboat chasing it across a teal sea. The name is the only
text in the picture.

## How it is built

`tools/render.py` draws `assets/entry.png` (1024×1024 PNG) with Pillow —
every coordinate is fixed, no randomness, no network, so two runs produce
identical bytes. `main.py` copies that image to `/output/entry.png`.

```sh
python3 tools/render.py assets/entry.png   # regenerate the poster
python3 main.py                            # copy it to /output/entry.png
```

## Files

- `main.py` — the entry program (copies the poster)
- `tools/render.py` — the poster generator (Pillow, Noto Sans Condensed)
- `assets/entry.png` — the poster
- `README.md`, `LICENSE` (MIT)
