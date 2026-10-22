#!/bin/bash
# Kid-safe off switch. Creates the stop file, then closes the kiosk.
touch "$HOME/.bjj-tv-stop"; sleep 4
pkill -f "controller/loop.py"; pkill -f "bjj-tv-profile"; echo "BJJ TV stopped. scripts/start.sh to resume."
