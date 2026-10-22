#!/bin/bash
PL="$HOME/Library/LaunchAgents/com.family.bjjtv.plist"; launchctl unload "$PL" 2>/dev/null; rm -f "$PL"; echo removed
