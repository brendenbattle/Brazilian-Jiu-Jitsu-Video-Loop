#!/bin/bash
# Installs a LaunchAgent: start at login, restart if it crashes (unless stop file exists).
set -e; DIR="$(cd "$(dirname "$0")/.." && pwd)"; PL="$HOME/Library/LaunchAgents/com.family.bjjtv.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$DIR/logs"
cat > "$PL" <<P
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>com.family.bjjtv</string>
<key>ProgramArguments</key><array><string>/bin/bash</string><string>$DIR/scripts/start.sh</string></array>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><dict><key>PathState</key><dict><key>$HOME/.bjj-tv-stop</key><false/></dict></dict>
<key>StandardOutPath</key><string>$DIR/logs/loop.log</string><key>StandardErrorPath</key><string>$DIR/logs/loop.log</string>
</dict></plist>
P
launchctl unload "$PL" 2>/dev/null || true; launchctl load "$PL"; echo "Autostart installed: $PL"
