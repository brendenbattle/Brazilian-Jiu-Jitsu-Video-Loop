# Norah's BJJ TV Loop

Plays Norah's study videos (YouTube + AOJ+) back to back on the living-room TV and loops forever. No clicking.
Family project. Works on the old MacBook Air (HDMI to TV) or the MacBook Pro: the whole thing is this folder.

## What you need
- macOS 12 Monterey or newer is best. (Check: Apple menu → About This Mac.) See "Old Mac notes".
- Google Chrome. Python 3 (`xcode-select --install` gives you one).
- An AOJ+ membership. **You** sign in once in the TV's Chrome profile. This repo never sees, stores, or asks for your password.

## Setup (about 15 min, every step safe to re-run)
1. Copy this folder to the Mac (AirDrop, USB, or `git clone`), e.g. to `~/bjj-tv-loop`.
2. Terminal: `cd ~/bjj-tv-loop && scripts/setup.sh`
3. `scripts/first-signin.sh` opens Chrome on the TV profile (`~/.bjj-tv-profile`). Sign in to AOJ+ and tick "remember me". Optional: sign in to YouTube Premium (removes ads). Then quit Chrome (Cmd+Q).
4. Plug in HDMI. System Settings → Displays: set the TV as the main display (or turn on mirroring). Sound output: the TV.
5. Test it: `scripts/start.sh`. Chrome opens fullscreen and starts playing. Stop it with `scripts/stop.sh` from another Terminal window, or press Ctrl+C.
6. Make it start at login: `scripts/install-autostart.sh`. Also turn on auto-login for the TV user: System Settings → Users & Groups → Automatically log in as.

## Every day
- **Turn on:** open the lid or log in. It starts by itself. You can also run `scripts/start.sh`.
- **Turn off (kid-safe):** run `scripts/stop.sh`, or double-click it in Finder (set Terminal as the app that opens .sh files). For an even easier switch, set up an Apple Shortcut that runs `~/bjj-tv-loop/scripts/stop.sh` and add it to the Dock or your iPhone. Turning off the TV only blanks the screen. The loop keeps running.
- **Change videos:** edit `playlist.json` (see below). Changes take effect from the next video. No restart needed.

## Editing the playlist (anyone can do this)
`playlist.json` holds a list of items. Copy an existing line and change it:
```json
{ "type": "youtube", "title": "Any label", "url": "https://www.youtube.com/watch?v=XXXXXXXXXXX", "enabled": true },
{ "type": "aoj",     "title": "Any label", "url": "https://aojplus.artofjiujitsu.com/programs/...", "enabled": true }
```
Rules: there's a comma between items but none after the last one. `enabled: false` skips a video without deleting it. The list plays in order, top to bottom.
Run `python3 tests/validate_playlist.py` afterward to catch typos and YouTube videos that block embedding.
Settings: `shuffle`, `max_minutes_per_video` (a safety cap if a video never reports "ended").

## How it works
`controller/loop.py` uses Playwright to drive your installed Chrome with the dedicated, signed-in profile:
- **YouTube:** loads the local page `player/index.html` (YouTube IFrame API). When the video fires `ended`, the loop moves on.
- **AOJ+:** opens the lesson page, starts its `<video>`, and waits for `ended`. If the profile got signed out, AOJ+ items are skipped and the YouTube items keep playing.
- **Recovery:** errors, stalls, and timeouts move on to the next video. If everything fails, it waits 2 minutes and tries again. If the process crashes, launchd restarts it.
- **Sleep:** `caffeinate` keeps the screen and the Mac awake while it runs.
- **Autoplay:** Chrome starts with `--autoplay-policy=no-user-gesture-required` and the player starts muted, then unmutes. If sound stays off, press any key.

Fallback with no Playwright and YouTube only: `scripts/youtube-only.sh`.

## Old Mac notes
- MacBook Air 2015–2017 can run up to macOS 12 Monterey. 2013–2014 models stop at macOS 11 Big Sur. 2018 and later run newer versions.
- Current Chrome requires macOS 12 or later. On Big Sur, Chrome stops getting updates, and Playwright may not support the OS. In that case, use the MacBook Pro, or `youtube-only.sh` with the last Chrome version that installs. Another option is the **AOJ+ Apple TV/Roku app** for AOJ+ content (see BUILD_PLAN, Phase 0).
- Old Airs top out at 1080p over HDMI through a Thunderbolt/Mini DisplayPort adapter. That's fine for this.

## Moving to the MacBook Pro
Copy the folder, then run steps 2–6 again. The sign-in lives in `~/.bjj-tv-profile` on each Mac, so sign in once on each machine. Never copy cookies or passwords between machines.

## Troubleshooting
Logs are in `logs/loop.log`. "not signed in" means you should run `first-signin.sh` again. A black screen with no sound means you should press a key or check the Sound output.
