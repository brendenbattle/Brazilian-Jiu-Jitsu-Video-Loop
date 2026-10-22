#!/bin/bash
# Idempotent: safe to re-run. Creates .venv, installs Playwright (uses your installed Google Chrome).
set -e; cd "$(dirname "$0")/.."
command -v python3 >/dev/null || { echo "Install Python 3 first: xcode-select --install"; exit 1; }
[ -d "/Applications/Google Chrome.app" ] || { echo "Install Google Chrome first: https://www.google.com/chrome/"; exit 1; }
python3 -m venv .venv && . .venv/bin/activate && pip install -q --upgrade pip && pip install -q -r requirements.txt
python3 -m json.tool playlist.json >/dev/null && echo "playlist.json OK"
echo "Setup done. Next: scripts/first-signin.sh"
