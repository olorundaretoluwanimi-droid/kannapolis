D = r'C:\Users\HP\Desktop\klaude\kannapolis'
b = D + r'\tools\build_film.py'; t = open(b, encoding='utf-8').read()
def rep(s, a, c):
    assert s.count(a) == 1, a[:60]; return s.replace(a, c)
t = rep(t, "CHIMG = {'towel': 'postcard_mill',", "CHIMG = {'towel': 'towel_looms',")
t = rep(t, " 'n06': dict(type='card', name='James William Cannon', line='1852–1921 · MERCHANT, MILL BUILDER', img='postcard_kmill', tag='CANNON MILLS · POSTCARD', date='1887'),",
        " 'n06': dict(type='film', clips=['c0', 'c1'], tag='FILM · OPENING AND COMBING COTTON · FRANCE · 1920 · ILLUSTRATIVE', name='James William Cannon', role='1852–1921 · MERCHANT, MILL BUILDER', date='1887'),")
t = rep(t, " 'n08': P('postcard_mill', tag='CANNON MILLS · POSTCARD', date='1898', colour=1, z=(1.0, 1.08)),",
        " 'n08': P('towel_looms', tag='TOWEL LOOMS · PHOTO, FLICKR (CC BY 2.0)', colour=1, date='1898', z=(1.0, 1.1)),")
t = rep(t, " 'n16': P('towel_looms', tag='TOWEL LOOMS · PHOTO, FLICKR (CC BY 2.0)', colour=1, date='1914', z=(1.0, 1.1)),",
        " 'n16': P('postcard_mill', tag='CANNON MILLS · POSTCARD · “LARGEST MANUFACTURERS OF TOWELS IN THE WORLD”', colour=1, date='1914', z=(1.0, 1.25), fx=.72, fy=.3),")
open(b, 'w', encoding='utf-8').write(t)
p = D + r'\index.html'; s = open(p, encoding='utf-8').read()
s = rep(s, "  const X = (W - 1146) / 2; cover(fr[j], X, 60, 1146, 860, { flash: 1 - seg(l - ci * per, 0, .12) }, .5, .5, [164, 4, 955, 712]); tag(s.tag, X, 46, { id: 'tg' });",
        "  const X = (W - 1146) / 2; cover(fr[j], X, 60, 1146, 860, { flash: 1 - seg(l - ci * per, 0, .12) }, .5, .5, [164, 4, 955, 712]); tag(s.tag, X, 46, { id: 'tg' });\n"
        "  if (s.name) nameBox(s.name, s.role, X, 790, seg(t, s.t0 + .4, s.t0 + .5)); if (s.date) dateBox(s.date, X + 1146, 60, seg(t, s.t0 + .2, s.t0 + .3));")
s = rep(s, "    'Narration  ElevenLabs voice “Storyteller Oxley” via AI33 Pro · Music  original score; VSCO 2 CE (CC0), Salamander Grand Piano (CC BY 3.0, Alexander Holm)',\n    'Unofficial film. Dates and figures are from the sources named; where sources disagree, the film says “about”.' ];",
        "    'Music  original score; VSCO 2 CE (CC0), Salamander Grand Piano (CC BY 3.0, Alexander Holm)' ];")
s = rep(s, "cr.forEach((c, i) => txt(c, 124, 600 + i * 40, { s: 21, c: i === 5 ? C.dim : '#CDBFA6', a: k3 }));", "cr.forEach((c, i) => txt(c, 124, 600 + i * 40, { s: 21, c: '#CDBFA6', a: k3 }));")
open(p, 'w', encoding='utf-8').write(s); print('ok')
