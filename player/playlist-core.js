// Pure logic shared by browser player and tests. No DOM.
(function (root) {
  function youtubeId(url) {
    var m = String(url).match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([A-Za-z0-9_-]{11})/);
    return m ? m[1] : null;
  }
  function normalize(pl) {
    var items = (pl && pl.items) || [];
    return items.filter(function (it) {
      if (!it || it.enabled === false) return false;
      if (it.type === 'youtube') return !!youtubeId(it.url);
      if (it.type === 'aoj') return /^https:\/\/aojplus\.artofjiujitsu\.com\//.test(it.url);
      return false;
    });
  }
  function nextIndex(i, n) { return n ? (i + 1) % n : -1; }
  // Skip after too many consecutive failures to avoid a hot loop.
  function Rotator(items, opts) {
    opts = opts || {};
    this.items = items; this.i = -1; this.fails = 0; this.maxFails = opts.maxFails || items.length * 2;
  }
  Rotator.prototype.next = function () { this.i = nextIndex(this.i, this.items.length); return this.items[this.i]; };
  Rotator.prototype.fail = function () { this.fails++; return this.fails >= this.maxFails; /* true => pause & retry later */ };
  Rotator.prototype.ok = function () { this.fails = 0; };
  var api = { youtubeId: youtubeId, normalize: normalize, nextIndex: nextIndex, Rotator: Rotator };
  if (typeof module !== 'undefined') module.exports = api; else root.PlaylistCore = api;
})(this);
