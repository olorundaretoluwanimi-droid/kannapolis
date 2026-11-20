D = r'C:\Users\HP\Desktop\klaude\kannapolis'
p = D + r'\index.html'; s = open(p, encoding='utf-8').read()
# 1. a person with no known photograph: paper card beside a neutral archive image (never a stranger's face under her name)
a = "  cover(im, 60, 60, 1800, 860, { flash: flashK(t, s), colour: !s.noportrait }, .5, .5, null, lerp(1, 1.08, K(t, s))); tag(s.tag, 60, 46, { id: 'tg' });"
assert s.count(a) == 1
s = s.replace(a, """  if (s.noportrait) { cover(im, 60, 60, 820, 860, { flash: flashK(t, s) }, .5, .5, null, lerp(1.1, 1.2, K(t, s))); tag(s.imgTag, 60, 46, { id: 'tg' });
    const k = seg(t, s.t0 + .3, s.t0 + .4); x.save(); x.globalAlpha = k; paperCard(920, 60, 940, 860); x.restore();
    tag(s.tag, 920, 46, { a: k, id: 'tg2' }); txt(s.name, 980, 400, { s: 92, w: 700, c: C.ink, a: k, id: 'cn' });
    s.lines.forEach((l, i) => txt(l, 984, 480 + i * 52, { s: 34, c: '#5a4b3a', a: k, id: 'cl' + i }));
    txt('No photograph of her is known.', 984, 760, { s: 30, f: F.it, it: 1, c: '#7a6c58', a: seg(t, s.t0 + 1.2, s.t0 + 1.3), id: 'cnp' });
    if (s.date) txt(s.date, 984, 260, { s: 72, f: F.mono, w: 600, c: C.acc, a: k, id: 'cd' }); return; }
""" + a)
# 2. every quote card names the picture beside it
a = "  const k = seg(t, s.t0 + .25, s.t0 + .3); x.save(); x.globalAlpha = k; paperCard(860, 60, 1000, 860); x.restore();"
assert s.count(a) == 1
s = s.replace(a, "  if (s.imgTag) tag(s.imgTag, 60, 46, { id: 'qimg' });\n" + a)
open(p, 'w', encoding='utf-8').write(s)
b = D + r'\tools\build_film.py'; t = open(b, encoding='utf-8').read()
R = [("'n35': dict(type='card', name='Alice Caudle', line='SPINNER · CANNON MILLS · INTERVIEWED 1938', img='hine_otie', tag='WPA FEDERAL WRITERS’ PROJECT · 2 SEPT 1938', date='1938', noportrait=1),",
      "'n35': dict(type='card', name='Alice Caudle', line='', lines=['Spinner, Cannon Mills, Concord', 'Began at about ten years old', 'Interviewed by Muriel L. Wolff, 2 Sept 1938'], img='sanborn1926_0010', imgTag='SANBORN MAP · MILL HOUSES · 1926', tag='WPA FEDERAL WRITERS’ PROJECT · LIFE HISTORY', date='1938', noportrait=1),"),
     ("'q1': dict(type='quote', img='hine_otie',", "'q1': dict(type='quote', img='hine_otie', imgTag='L. W. HINE · 1912 · CHILDREN AT THE CANNON MILL, CONCORD',"),
     ("'q2': dict(type='quote', img='hine_boys',", "'q2': dict(type='quote', img='hine_boys', imgTag='L. W. HINE · 1912 · BOYS AT THE CANNON MILLS, CONCORD',"),
     ("'q3': dict(type='quote', img='charles_cannon', portrait=1,", "'q3': dict(type='quote', img='charles_cannon', portrait=1, imgTag='CHARLES A. CANNON · c. 1920',"),
     ("'q4': dict(type='quote', img='postcard_mill', colour=1,", "'q4': dict(type='quote', img='postcard_mill', colour=1, imgTag='CANNON MILLS · POSTCARD',"),
     ("'q5': dict(type='quote', img='hine_otie',", "'q5': dict(type='quote', img='hine_otie', imgTag='L. W. HINE · 1912 · CANNON MILL, CONCORD',"),
     ("'n21': dict(type='quote', img='hine_parker', fy=.35,", "'n21': dict(type='quote', img='hine_parker', fy=.35, imgTag='L. W. HINE · 1912 · HERMAN PARKER',")]
for x0, x1 in R:
    assert t.count(x0) == 1, x0[:50]; t = t.replace(x0, x1)
open(b, 'w', encoding='utf-8').write(t); print('ok')
