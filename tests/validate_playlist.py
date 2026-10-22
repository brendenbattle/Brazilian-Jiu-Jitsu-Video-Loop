"""Run after editing playlist.json: python3 tests/validate_playlist.py  (checks JSON + YouTube embeddability via oEmbed)."""
import json, pathlib, sys, urllib.request, urllib.parse
R = pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0, str(R/'controller')); import core
pl = json.loads((R/'playlist.json').read_text()); bad = 0
for it in pl['items']:
    if it.get('type') == 'youtube':
        try:
            u = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(it['url'])
            t = json.load(urllib.request.urlopen(u, timeout=10))['title']; print('OK  yt ', t)
        except Exception as e: bad += 1; print('BAD yt ', it['url'], e)
    elif it.get('type') == 'aoj': print('ok  aoj', it['url'], '(needs sign-in; not checked)')
    else: bad += 1; print('BAD type', it)
print(f'{len(core.normalize(pl))} playable items; {bad} problems'); sys.exit(1 if bad else 0)
