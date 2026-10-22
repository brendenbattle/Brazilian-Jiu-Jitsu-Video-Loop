"""Python mirror of player/playlist-core.js (keep in sync; tests check both)."""
import re
def youtube_id(url):
    m = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})', str(url)); return m.group(1) if m else None
def normalize(pl):
    out = []
    for it in (pl or {}).get('items', []):
        if not it or it.get('enabled') is False: continue
        if it.get('type') == 'youtube' and youtube_id(it.get('url')): out.append(it)
        elif it.get('type') == 'aoj' and str(it.get('url','')).startswith('https://aojplus.artofjiujitsu.com/'): out.append(it)
    return out
