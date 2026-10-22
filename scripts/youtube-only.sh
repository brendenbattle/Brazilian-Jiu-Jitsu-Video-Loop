#!/bin/bash
# Fallback with zero Python deps beyond stdlib: YouTube-only loop in Chrome kiosk.
cd "$(dirname "$0")/.."; python3 controller/serve.py & SV=$!
caffeinate -dimsu open -Wna "Google Chrome" --args --user-data-dir="$HOME/.bjj-tv-profile" --kiosk --autoplay-policy=no-user-gesture-required "http://127.0.0.1:8765/"
kill $SV
