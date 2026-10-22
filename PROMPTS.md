# Ready-to-paste prompts for a coding agent
Constraints to keep in every prompt: never handle AOJ+ credentials (Brenden signs in himself in `~/.bjj-tv-profile`). Never download or record AOJ+ video, since their terms forbid copying. Keep `playlist.json` the single source of truth and keep it simple to edit.

## Prompt 1: Verify on the target Mac
"In ~/bjj-tv-loop, run scripts/setup.sh, then node or python tests, then python3 tests/validate_playlist.py. Report macOS version, Chrome version, and whether Playwright launched channel='chrome'. If Playwright fails on this macOS, make scripts/youtube-only.sh work and report what failed. Don't change playlist.json."

## Prompt 2: Fix AOJ+ playback selectors
"AOJ+ (an Uscreen-based site) lessons don't auto-start or don't report end in controller/loop.py. Brenden is already signed in to the Chrome profile ~/.bjj-tv-profile. Launch loop.py with a single AOJ+ item, inspect the page frames, and find the <video> element or player iframe, the play control, and the end signal. Update AOJ_JS_START and the ended check to be robust (iframe-aware, retry, fullscreen). Don't log in, don't read cookies, don't download media. Test with one lesson end to end."

## Prompt 3: Unattended hardening
"Harden bjj-tv-loop for running unattended overnight: confirm the launchd KeepAlive and stop-file behavior survives a reboot. Add a quiet-hours setting in playlist.json settings (e.g. 'off_after': '20:00', 'on_at': '07:00'). Add log rotation. Make sure caffeinate is released when stopped. Update README and BUILD_PLAN checkboxes."

## Prompt 4: Playlist maintenance (non-developer agent)
"Update ~/bjj-tv-loop/playlist.json from these coach notes: <paste>. For each new video, add {type, title, url, enabled:true}. Use type 'youtube' for youtube.com or youtu.be links and 'aoj' for aojplus.artofjiujitsu.com links. Set enabled:false on videos the notes say to retire instead of deleting them. Keep valid JSON. Then run python3 tests/validate_playlist.py and fix anything marked BAD."

## Prompt 5: Clip support
"Add optional 'start' and 'end' (seconds) per item. For YouTube, pass them through to loadVideoById({videoId,startSeconds,endSeconds}). For AOJ+, seek video.currentTime=start and treat currentTime>=end as ended. Add tests in tests/ for both cores."

## Prompt 6: One-tap off/on switch
"Create a macOS app (Automator or Shortcuts, documented steps) named 'BJJ TV Off' that runs scripts/stop.sh, and 'BJJ TV On' that runs scripts/start.sh in the background. Put them in the Dock. No admin rights needed."
