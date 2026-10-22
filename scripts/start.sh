#!/bin/bash
# Starts the loop with sleep prevention. Usage: scripts/start.sh  (Ctrl+C or scripts/stop.sh to end)
cd "$(dirname "$0")/.."; rm -f "$HOME/.bjj-tv-stop"
. .venv/bin/activate
exec caffeinate -dimsu python3 controller/loop.py
