#!/usr/bin/env python3
"""Score, light foley and narration for "What Happened to Kannapolis?" → out/mix.wav (48 kHz stereo). All timing from ../film.json.
Score (core/audio/sampler: VSCO 2 CE CC0, Salamander piano CC BY 3.0): warm, gentle, chapter by chapter; music dips ≈ 8 dB under the voice."""
import json, os, sys
import numpy as np, soundfile as sf, soxr
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.environ.get('LIB') or os.path.expanduser('~/lemo-opuscar'); sys.path.insert(0, LIB)
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, noise, env_exp, t_, thump, norm, limit, brown
F = json.load(open(os.path.join(D, 'film.json'), encoding='utf-8')); DUR = F['dur']; SC = F['scenes']
N = int(DUR * SR); S.seed(5); np.random.seed(5)
BAR = 3.75
CH = {'D': ('D2', ['A3', 'D4', 'F#4'], ['D4', 'F#4', 'A4', 'D5', 'A4', 'F#4']), 'Bm': ('B1', ['F#3', 'B3', 'D4'], ['B3', 'D4', 'F#4', 'B4', 'F#4', 'D4']),
      'G': ('G1', ['G3', 'B3', 'D4'], ['G3', 'B3', 'D4', 'G4', 'D4', 'B3']), 'A': ('A1', ['E3', 'A3', 'C#4'], ['A3', 'C#4', 'E4', 'A4', 'E4', 'C#4']),
      'Em': ('E2', ['E3', 'G3', 'B3'], ['E3', 'G3', 'B3', 'E4', 'B3', 'G3']), 'F#m': ('F#1', ['F#3', 'A3', 'C#4'], ['F#3', 'A3', 'C#4', 'F#4', 'C#4', 'A3']),
      'C': ('C2', ['G3', 'C4', 'E4'], ['C4', 'E4', 'G4', 'C5', 'G4', 'E4'])}
def b2(n): return n if n[-1] != '1' else n[:-1] + '2'
ev = []
def E(*a): ev.append(a)
def bar(t0, name, arp='piano', vel=.28, gain=1.0, pad=True):
    b, p, a = CH[name]; E(t0, 'contrabass', b2(b), BAR, .3, -.15, .36 * gain)
    if pad:
        for i, n in enumerate(p): E(t0, 'violas' if i < 2 else 'violins', n, BAR + .25, .24, (-.3, .1, .35)[i], .18 * gain)
    if arp:
        for i, n in enumerate(a): E(t0 + i * BAR / 6, arp, n, 1.6, vel + .05 * (i == 0), -.25 + .1 * i, .32 * gain)
# chapter → (progression, arpeggio instrument, gain, melody instrument or None)
STYLE = {'open': (['Bm', 'G', 'D', 'A'], 'piano', .8, None), 'towel': (['D', 'G', 'Bm', 'A'], 'piano', 1.0, 'clarinet'),
         'children': (['Bm', 'Em', 'G', 'F#m'], 'harp', .85, None), 'town': (['G', 'D', 'Em', 'C'], 'piano', 1.0, 'clarinet'),
         'vote': (['Em', 'C', 'G', 'D'], 'harp', .9, 'horn'), 'sold': (['Bm', 'G', 'Em', 'F#m'], 'piano', .85, None),
         'last': (['Bm', 'G'], 'piano', .55, None), 'now': (['D', 'G', 'Bm', 'A'], 'piano', 1.0, 'horn'), 'end': (['D', 'G', 'D'], 'harp', .9, None)}
MEL = {'D': ['F#4', 'A4', 'D5', 'A4'], 'G': ['G4', 'B4', 'D5', 'B4'], 'Bm': ['F#4', 'B4', 'D5', 'B4'], 'A': ['E4', 'A4', 'C#5', 'A4'],
       'Em': ['E4', 'G4', 'B4', 'G4'], 'C': ['E4', 'G4', 'C5', 'G4'], 'F#m': ['F#4', 'A4', 'C#5', 'A4']}
# chapter spans from the scene list (chapter cards mark boundaries)
LCH = {l['id']: l['chapter'] for l in json.load(open(os.path.join(D, 'audio/lines.json'), encoding='utf-8'))}
spans, cur, start = [], 'open', 0.0
for s in SC:
    ch = LCH.get(s.get('line'), None) if s['type'] != 'end' else 'end'
    if s['type'] == 'chapter': ch = None
    if s['type'] == 'chapter' or (s['type'] == 'end'):
        spans.append((cur, start, s['t0'])); start = s['t0']
        cur = 'end' if s['type'] == 'end' else next(LCH[x['line']] for x in SC[SC.index(s) + 1:] if x.get('line'))
spans.append((cur, start, DUR))
for ch, a, b in spans:
    prog, arp, g, mel = STYLE[ch]; t, i = a, 0
    if ch != 'open': E(a, 'timpani', 'D2', 2.0, .32, 0, .3 * g)
    while t < b - 1.0:
        name = prog[i % len(prog)]; bar(t, name, arp=arp, gain=g, pad=(ch != 'last'))
        if mel and i % 4 in (1, 3):
            for j, n in enumerate(MEL[name][:3]): E(t + j * BAR / 3, mel, n, BAR / 3 + .3, .26, -.1, .26 * g)
        t += BAR; i += 1
mus = S.render(ev, dur=DUR, master=False)[:N]; mus = S.room(mus, size=.6, mix=.25)
if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
# ── light foley: a soft shutter when a photograph cuts in, paper when a card or document lands ──
fx = np.zeros((N, 2), np.float32)
def shutter(v=1.0):
    d = .09; a = hp(noise(d), 2000) * env_exp(d, .006); b = np.pad(hp(noise(.05), 1500) * env_exp(.05, .005), (int(.045 * SR), 0))[:len(a)]; return norm(a + b * .8) * v
def paper(v=1.0):
    d = .25; return bp(noise(d), 1200, 6000) * env_exp(d, .05) * (1 - np.exp(-t_(d) / .01)) * v
prev_img = None
for s in SC:
    if s['type'] in ('quote', 'doc', 'ledger'): add(fx, paper(.8), s['t0'] + .25, .22, .2)
    elif s['type'] in ('photo', 'stat', 'card', 'pair', 'film') and s.get('img') != prev_img: add(fx, shutter(.6), s['t0'], .16, -.2)
    elif s['type'] == 'chapter': add(fx, thump(.4, 60), s['t0'], .18)
    prev_img = s.get('img')
fx += np.repeat(lp(brown(DUR), 400)[:N, None] * .008, 2, axis=1).astype(np.float32)
# ── narration ──
voc = np.zeros((N, 2), np.float32); VO = {}
for k, at in F['vo'].items():
    x, sr = sf.read(os.path.join(D, f'audio/vo/{k}.wav')); x = x if x.ndim == 1 else x.mean(1)
    x = soxr.resample(x, sr, SR); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .11
    add(voc, x, at, 1.0, 0); VO[k] = (at, at + len(x) / SR)
g = np.ones(N)
for a, b in VO.values(): g[int(a * SR):int(b * SR)] = np.minimum(g[int(a * SR):int(b * SR)], .4)
from scipy.ndimage import uniform_filter1d
g = uniform_filter1d(g, int(.4 * SR)); mus *= g[:, None]; fx *= (.6 + .4 * g)[:, None]
out = mus * 3.0 + fx * .7 + voc
tail = int(2.0 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
def tp_limit(x, ceil):
    from scipy.signal import resample_poly
    from scipy.ndimage import maximum_filter1d, minimum_filter1d, uniform_filter1d
    up = resample_poly(x, 4, 1); n = int(.004 * SR * 4)
    g = np.minimum(1, ceil / np.maximum(maximum_filter1d(np.abs(up), 2 * n + 1), 1e-9)); g = uniform_filter1d(minimum_filter1d(g, 2 * n + 1), n)
    return resample_poly(up * g, 1, 4)[:len(x)]
out = np.stack([tp_limit(limit(out[:, c], .5), .45) for c in range(2)], 1)
os.makedirs(os.path.join(D, 'out'), exist_ok=True); sf.write(os.path.join(D, 'out/mix.wav'), out.astype(np.float32), SR)
def db(a): return 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12)
vm = np.zeros(N, bool)
for a, b in VO.values(): vm[int(a * SR):int(b * SR)] = True
print('mix', round(DUR, 1), 's | voice', round(db(voc[vm]), 1), 'bed under voice', round(db((mus * 3 + fx * .7)[vm]), 1), 'music alone', round(db((mus * 3)[~vm]), 1))
