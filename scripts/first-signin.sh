#!/bin/bash
# Opens normal Chrome on the dedicated TV profile. YOU sign in to AOJ+ here yourself (check "remember me"),
# optionally let Chrome/Keychain save it. Nothing is stored by this repo. Quit Chrome when done.
PROFILE="${BJJTV_PROFILE:-$HOME/.bjj-tv-profile}"
open -na "Google Chrome" --args --user-data-dir="$PROFILE" "https://aojplus.artofjiujitsu.com/sign_in" "https://www.youtube.com"
