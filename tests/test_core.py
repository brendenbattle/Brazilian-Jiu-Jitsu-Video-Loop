import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0, str(R/'controller')); import core
pl = json.loads((R/'playlist.json').read_text())
assert len(core.normalize(pl)) == 9
assert core.youtube_id('https://www.youtube.com/watch?v=bddWtJxLWKg') == 'bddWtJxLWKg'
assert core.normalize({'items':[{'type':'aoj','url':'http://aojplus.artofjiujitsu.com/x'}]}) == []
print('py core: all tests passed')
