# Build plan (resumable: tick boxes as you go; every phase stands on its own)

## Phase 0: Decide (10 min)
- [ ] Check the Air's model year and macOS (About This Mac). Monterey (12) or newer means go ahead. Big Sur or older: use the MacBook Pro, or YouTube-only mode.
- [ ] Try the zero-code option first. AOJ+ has Apple TV (tvOS 17.5+), Roku, iOS, and Android apps, plus playlists and autoplay on the web player. If an AOJ+ playlist on Roku or Apple TV auto-advances well enough for the AOJ+ part, the Mac only needs to handle YouTube, or nothing at all.
- [ ] Find out whether each `/programs/...` link is one video or a multi-lesson program. If it's multi-lesson, decide whether to list each lesson URL separately (recommended) or rely on AOJ+'s next-lesson autoplay.

## Phase 1: YouTube-only loop (done in the starter repo, tested on the box)
- [x] `playlist.json` seeded with 9 items. All 4 YouTube IDs pass the oEmbed check (embeddable).
- [x] `player/index.html`: IFrame API, auto-advance, loop, muted-start/unmute, error skip, stall watchdog.
- [x] Logic tests: `node tests/test_core.js`, `python3 tests/test_core.py`
- [ ] On the Mac, run `scripts/youtube-only.sh` and confirm 2 videos advance by themselves on the TV.

## Phase 2: AOJ+ in a signed-in profile
- [ ] `scripts/setup.sh`, then `scripts/first-signin.sh`. Brenden signs in himself.
- [ ] `scripts/start.sh`. Watch one AOJ+ lesson end and advance to the next.
- [ ] If AOJ+ doesn't start: open the lesson in the TV profile, inspect the player (Cmd+Opt+I), and note the play-button selector and whether `<video>` sits inside an iframe. Then update `AOJ_JS_START` in `controller/loop.py` (PROMPTS.md, Prompt 2).
- [ ] If AOJ+ moves to its own next lesson before our script does, set the playlist to the first lesson only, or disable autoplay in AOJ+ settings.

## Phase 3: Unattended
- [ ] `scripts/install-autostart.sh`. Turn on auto-login. Reboot to test.
- [ ] Energy settings: never sleep on power adapter. Turn off the screen saver. caffeinate covers this too.
- [ ] Test the off switch: `scripts/stop.sh` should stop it, and it should stay stopped after a reboot until `start.sh` runs.
- [ ] Leave it running for 2 hours. Check `logs/loop.log` for errors and signed-out messages.

## Phase 4: Nice-to-haves
- [ ] One-tap off and on (Apple Shortcut or a Dock app).
- [ ] Coach agent workflow: edit `playlist.json`, then `tests/validate_playlist.py` (PROMPTS.md, Prompt 4).
- [ ] Optional start and end timestamps per YouTube item (`start`/`end` fields) to loop just the key technique.
- [ ] Quiet hours, e.g. stop automatically at 8 PM.
- [ ] Move to the MacBook Pro if needed (README).
