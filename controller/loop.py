"""Main loop. Drives a persistent, signed-in Chrome profile through playlist.json forever.
- YouTube items -> local player page (?yt=ID), waits for title BJJTV:ended|error.
- AOJ+ items    -> opens the lesson page, starts the <video>, waits for 'ended'.
No credentials are ever handled here: Brenden signs in once in this profile (scripts/first-signin.sh).
"""
import json, os, sys, time, threading, random, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROFILE = pathlib.Path(os.environ.get('BJJTV_PROFILE', pathlib.Path.home() / '.bjj-tv-profile'))
STOP = pathlib.Path.home() / '.bjj-tv-stop'   # kid-safe off switch: file exists => stop
PORT = 8765
sys.path.insert(0, str(ROOT / 'controller'))
import serve, core

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

def wait_title(page, deadline):
    while time.time() < deadline:
        if STOP.exists(): return 'stop'
        t = page.title()
        if t.startswith('BJJTV:'): return t.split(':', 1)[1]
        time.sleep(2)
    return 'timeout'

def play_youtube(page, it, max_s):
    page.goto(f'http://127.0.0.1:{PORT}/?yt={core.youtube_id(it["url"])}')
    return wait_title(page, time.time() + max_s)

AOJ_JS_START = """async () => {
  const v = document.querySelector('video');
  if (!v) { const b = document.querySelector('[class*=play], button[aria-label*=Play i], .vjs-big-play-button'); if (b) b.click(); return 'noplayer'; }
  try { v.muted = false; await v.play(); } catch (e) { v.muted = true; try { await v.play(); } catch (e2) { return 'blocked'; } }
  const el = v.closest('div') || v; if (el.requestFullscreen) { try { await el.requestFullscreen(); } catch(e){} }
  return 'playing';
}"""
def play_aoj(page, it, max_s, grace):
    page.goto(it['url'], wait_until='domcontentloaded')
    if '/sign_in' in page.url or 'login' in page.url:
        log('AOJ+ not signed in -> skipping. Run scripts/first-signin.sh'); return 'signed_out'
    deadline = time.time() + max_s
    state = 'noplayer'
    for _ in range(10):  # player (often in an iframe) can load late
        for fr in page.frames:
            try: state = fr.evaluate(AOJ_JS_START)
            except Exception: continue
            if state == 'playing': break
        if state == 'playing': break
        time.sleep(2)
    if state != 'playing': return 'error'
    while time.time() < deadline:
        if STOP.exists(): return 'stop'
        for fr in page.frames:
            try:
                r = fr.evaluate("() => { const v=document.querySelector('video'); return v ? [v.ended, v.currentTime, v.duration] : null }")
            except Exception: continue
            if r and (r[0] or (r[2] and r[1] >= r[2] - 0.5)):
                time.sleep(grace); return 'ended'
        time.sleep(3)
    return 'timeout'

def main():
    threading.Thread(target=serve.run, args=(PORT,), daemon=True).start()
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE), channel='chrome', headless=False, no_viewport=True,
            ignore_default_args=['--enable-automation'],
            args=['--kiosk', '--autoplay-policy=no-user-gesture-required', '--disable-session-crashed-bubble', '--noerrdialogs'])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        fails = 0; i = -1
        while not STOP.exists():
            pl = json.loads((ROOT / 'playlist.json').read_text())   # re-read each video: live edits
            items = core.normalize(pl); s = pl.get('settings', {})
            if not items: log('empty playlist'); time.sleep(30); continue
            if s.get('shuffle'): random.shuffle(items)
            i = (i + 1) % len(items); it = items[i]
            max_s = 60 * s.get('max_minutes_per_video', 25)
            log('playing', it['type'], it['title'])
            try:
                r = play_youtube(page, it, max_s) if it['type'] == 'youtube' else play_aoj(page, it, max_s, s.get('aoj_ended_grace_seconds', 3))
            except Exception as e:
                log('crash', e); r = 'error'
                try: page = ctx.new_page()
                except Exception: return 1   # launchd restarts us
            log('->', r)
            fails = 0 if r == 'ended' else fails + 1
            if fails >= 2 * len(items): log('everything failing; sleeping 2 min'); time.sleep(120); fails = 0
        log('stop file found; exiting'); ctx.close()
    return 0

if __name__ == '__main__': sys.exit(main())
