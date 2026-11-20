#!/usr/bin/env python3
"""lines.json + narration durations + the shot list below → film.json (scenes, voice starts, subtitles) and audio/cues.json.
Timing: each line starts GAP s after the previous one ends; a chapter card (CARD s) opens each chapter; the opening and
the end card are fixed. Every scene lasts from its line's start to the next scene's start, so nothing is left empty."""
import json, os, subprocess
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(D, 'audio/lines.json'), encoding='utf-8'))
DUR = json.load(open(os.path.join(D, 'audio/vo/dur.json')))
GAP, CARD, LEAD, END = 0.9, 4.2, 1.2, 14.0

CH = {'open': (None, None), 'towel': ('I', 'The Towel'), 'children': ('II', 'The Children'), 'town': ('III', 'The Company Town'),
      'vote': ('IV', 'The Vote'), 'sold': ('V', 'Sold'), 'last': ('VI', 'The Last Shift'), 'now': ('VII', 'What Stands There Now')}
CHIMG = {'towel': 'postcard_mill', 'children': 'hine_school', 'town': 'sanborn1943_0006', 'vote': 'strike1934', 'sold': 'charles_cannon',
         'last': 'pillowtex_offices', 'now': 'westave_now'}

# shot per line: type + params. Rings: [src_x, src_y, r, label, at (s after line start)].
P = lambda img, **k: dict(type='photo', img=img, **k)
S = {
 'n01': dict(type='open'),
 'n02': dict(type='stat', img='pillowtex_offices', num='4,340', label='jobs lost on 30 July 2003', tag='PILLOWTEX OFFICES · KANNAPOLIS · 2005', at=2.4),
 'n03': P('sanborn1943_0001', tag='SANBORN MAP · KANNAPOLIS · 1943 · INDEX', fy=.4, z=(1.0, 1.15)),
 'n04': P('implosion', tag='THE MILL COMES DOWN · 2006', small=1),
 'n05': dict(type='title'),
 'n06': dict(type='card', name='James William Cannon', line='1852–1921 · MERCHANT, MILL BUILDER', img='postcard_kmill', tag='CANNON MILLS · POSTCARD', date='1887'),
 'n08': P('postcard_mill', tag='CANNON MILLS · POSTCARD', date='1898', colour=1, z=(1.0, 1.08)),
 'n09': P('postcard_kmill', tag='CANNON MILLS, KANNAPOLIS · POSTCARD', colour=1, fx=.6, z=(1.08, 1.0)),
 'n10': P('sanborn1926_0001', tag='SANBORN MAP · KANNAPOLIS · 1926', date='1906', z=(1.0, 1.2), fy=.3),
 'n11': P('sanborn1926_0002', tag='SANBORN MAP · KANNAPOLIS · 1926 · WEST AV. & S. MAIN', z=(1.05, 1.25), fx=.7, fy=.3),
 'n12': dict(type='word', word='KANNAPOLIS', a='“city of looms”?', b='Cannon + polis (Greek: city) — “Cannon’s town”', img='sanborn1926_0002'),
 'n13': P('hine_school', tag='PHOTO · LEWIS W. HINE · KANNAPOLIS · 1912', z=(1.0, 1.08), fy=.4),
 'n14': dict(type='film', clips=['c0', 'c1', 'c2', 'c3'], tag='FILM · “FILATURE ET TISSAGE DU COTON” · FRANCE · 1920 · ILLUSTRATIVE'),
 'n15': dict(type='film', clips=['c4', 'c5'], tag='FILM · FRANCE · 1920 · ILLUSTRATIVE'),
 'n16': P('towel_looms', tag='TOWEL LOOMS · PHOTO, FLICKR (CC BY 2.0)', colour=1, date='1914', z=(1.0, 1.1)),
 'n17': P('hine_boys', tag='PHOTO · LEWIS W. HINE · 1912', z=(1.0, 1.06)),
 'n18': P('hine_boys', tag='PHOTO · LEWIS W. HINE · CANNON MILLS, CONCORD · 1912', fx=.3, z=(1.1, 1.2)),
 'n19': P('hine_school', tag='PHOTO · LEWIS W. HINE · KANNAPOLIS · 1912', fx=.4, z=(1.15, 1.25)),
 'n20': P('hine_parker', tag='PHOTO · LEWIS W. HINE · KANNAPOLIS · 1912', ring=[1248, 420, 150, 'HERMAN PARKER', 0.4], name='Herman Parker', role='“SAID SIX YEARS OLD” · CANNON MILLS, KANNAPOLIS', z=(1.0, 1.12), fy=.35),
 'n21': dict(type='quote', img='hine_parker', fy=.35, q=['“The Logical Conclusion', 'of the Laissez Faire', 'Policy.”'], who='LEWIS W. HINE · TITLE OF THE PHOTOGRAPH · 1912'),
 'n22': P('hine_school', tag='PHOTO · LEWIS W. HINE · PUBLIC SCHOOL, KANNAPOLIS · 1912', z=(1.0, 1.1), fy=.6),
 'n23': P('hine_otie', tag='PHOTO · LEWIS W. HINE · CANNON MILLS, CONCORD · 1912', ring=[1200, 540, 120, 'OTIE HONEYCOTT', 3.2], name='“Otie Honeycott”', role='DOFFING TWO YEARS · CANNON MILL, CONCORD', z=(1.0, 1.1)),
 'n24': dict(type='film', clips=['c2', 'c3'], tag='FILM · SPINNING FRAMES · FRANCE · 1920 · ILLUSTRATIVE'),
 'n25': P('hine_housing', tag='PHOTO · LEWIS W. HINE · WORKERS’ HOUSING, CANNON MILLS, CONCORD · 1912', z=(1.0, 1.08)),
 'n26': dict(type='stat', img='hine_school', num='1938', label='Fair Labor Standards Act', tag='PHOTO · LEWIS W. HINE · 1912', at=1.0),
 'n27': P('hine_parker', tag='PHOTO · LEWIS W. HINE · 1912', z=(1.12, 1.25), fy=.3),
 'n28': dict(type='card', name='Charles A. Cannon', line='1892–1971 · TOOK OVER IN 1921', img='charles_cannon', tag='CHARLES A. CANNON · c. 1920', date='1921', portrait=1),
 'n29': P('postcard_kmill', tag='CANNON MILLS, KANNAPOLIS · POSTCARD', colour=1, date='1928', z=(1.0, 1.1)),
 'n30': P('sanborn1943_0001', tag='SANBORN MAP · KANNAPOLIS · 1943 · INDEX', z=(1.1, 1.3), fy=.45),
 'n31': P('sanborn1926_0002', tag='SANBORN MAP · KANNAPOLIS · 1926', date='1926', z=(1.0, 1.15), fy=.4),
 'n32': P('sanborn1943_0006', tag='SANBORN MAP · KANNAPOLIS · 1943 · PLANT NO. 1', date='1943', ring=[900, 1000, 300, 'PLANT NO. 1', 3.0], z=(1.0, 1.12), fy=.35),
 'n33': P('sanborn1926_0010', tag='SANBORN MAP · KANNAPOLIS · 1926 · MILL HOUSES', z=(1.0, 1.2), fy=.5),
 'n35': dict(type='card', name='Alice Caudle', line='SPINNER · CANNON MILLS · INTERVIEWED 1938', img='hine_otie', tag='WPA FEDERAL WRITERS’ PROJECT · 2 SEPT 1938', date='1938', noportrait=1),
 'n36': dict(type='stat', img='hine_boys', num='30+', label='years with the Cannon Mills', tag='PHOTO · L. W. HINE · CANNON MILLS · 1912', at=1.0),
 'q1': dict(type='quote', img='hine_otie', q=['“I was so little', 'I had to stand on a box', 'to reach my work.”'], who='ALICE CAUDLE · WPA LIFE HISTORY · 1938'),
 'n38': dict(type='film', clips=['c3', 'c4'], tag='FILM · SPINNING ROOM · FRANCE · 1920 · ILLUSTRATIVE'),
 'q2': dict(type='quote', img='hine_boys', q=['“If I’d a-been a man', 'no telling how far', 'I’d-a gone.”'], who='ALICE CAUDLE · 1938'),
 'n39': dict(type='ledger', items=[['7:00–3:30', 'her shift, 1938'], ['$31', 'pay for two full weeks'], ['$6', 'rent a month, company house']], img='sanborn1926_0010'),
 'n40': P('postcard_church', tag='KANNAPOLIS · POSTCARD', colour=1, z=(1.0, 1.08)),
 'n41': dict(type='card', name='Charles A. Cannon', line='THE 25-YEAR SUPPER · 1938', img='charles_cannon', tag='CHARLES A. CANNON · c. 1920', portrait=1),
 'q3': dict(type='quote', img='charles_cannon', portrait=1, q=['“He told about the way', 'young’uns used to stand', 'on boxes to work —', 'the way I done.”'], who='ALICE CAUDLE · 1938'),
 'n42': P('hine_housing', tag='PHOTO · L. W. HINE · 1912', z=(1.1, 1.2), fx=.6),
 'q4': dict(type='quote', img='postcard_mill', colour=1, q=['“…are you right sure', 'they’re not a-going', 'to take hit off my pay?”'], who='ALICE CAUDLE · 1938'),
 'n43': P('hine_otie', tag='PHOTO · L. W. HINE · 1912', z=(1.15, 1.25)),
 'q5': dict(type='quote', img='hine_otie', q=['“As long as I can work', 'and talk and laugh,', 'I’m happy.”'], who='ALICE CAUDLE · 1938'),
 'n44': P('eleanor_ymca', tag='ELEANOR ROOSEVELT AT THE YMCA, KANNAPOLIS · NATIONAL ARCHIVES', date='1942', z=(1.0, 1.1), fy=.35),
 'n45': dict(type='doc', img='directory1953_p140', tag='HILL’S KANNAPOLIS CITY DIRECTORY · 1953 · P. 140', hl='Cannon Mills'),
 'n46': P('sanborn1943_0006', tag='SANBORN MAP · 1943', z=(1.2, 1.3), fx=.6),
 'n47': dict(type='doc', img='strike1934', tag='DAILY WORKER · 22 SEPTEMBER 1934', wide=1, date='1934'),
 'n48': dict(type='stat', img='postcard_mill', colour=1, num='65', label='years before a union won a vote', tag='CANNON MILLS · POSTCARD', at=0.5),
 'n49': dict(type='votes', upto=0), 'n50': dict(type='votes', upto=1), 'n51': dict(type='votes', upto=3), 'n52': dict(type='votes', upto=4), 'n53': dict(type='votes', upto=4, hold=1),
 'n55': dict(type='card', name='Charles A. Cannon', line='DIED APRIL 1971', img='charles_cannon', tag='CHARLES A. CANNON · c. 1920', date='1971', portrait=1),
 'n56': P('postcard_kmill', tag='CANNON MILLS · POSTCARD', colour=1, z=(1.1, 1.0)),
 'n57': dict(type='chain', upto=0), 'n58': dict(type='chain', upto=1), 'n59': dict(type='chain', upto=2), 'n60': dict(type='chain', upto=3), 'n61': dict(type='chain', upto=3, imports=1), 'n62': dict(type='chain', upto=4),
 'n63': dict(type='stat', img='pillowtex_offices', num='2003', label='30 July · Pillowtex stops', tag='PILLOWTEX OFFICES · 2005', at=0.4),
 'n64': dict(type='stat', img='pillowtex_offices', num='4,340', label='jobs lost in one day', tag='PILLOWTEX OFFICES · 2005', at=1.4),
 'n65': dict(type='stat', img='sanborn1926_0002', num='97', label='years: 1906 → 2003', tag='SANBORN MAP · 1926', at=0.6),
 'n66': dict(type='dots', n=4340), 'n67': dict(type='dots', n=4340, hold=1),
 'n68': dict(type='stat', img='sanborn1943_0006', num='5.8M', label='square feet · about the size of the Pentagon', tag='PLANT NO. 1 · SANBORN MAP · 1943', at=1.0),
 'n69': P('implosion', tag='IMPLOSION · KANNAPOLIS · 2006', small=1, date='2006'),
 'n70': P('pillowtex_offices', tag='PILLOWTEX OFFICES · JULY 2005', colour=1, z=(1.0, 1.1)),
 'n71': dict(type='pair', a='pillowtex_offices', b='campus1', ta='THEN · PILLOWTEX OFFICES · 2005', tb='NOW · NC RESEARCH CAMPUS (CC0)'),
 'n72': dict(type='pair', a='sanborn1926_0002', b='westave_now', ta='1926 · WEST AV. ON THE SANBORN MAP', tb='NOW · WEST AVENUE, KANNAPOLIS (CC0)'),
 'n74': P('hine_school', tag='PHOTO · L. W. HINE · KANNAPOLIS · 1912', z=(1.0, 1.05)),
 'n75': P('postcard_mill', tag='CANNON MILLS · POSTCARD', colour=1, z=(1.0, 1.12)),
 'n76': dict(type='pair', a='hine_parker', b='hine_otie', ta='HERMAN PARKER · 1912', tb='CANNON MILLS, CONCORD · 1912'),
 'n77': P('westave_now', tag='WEST AVENUE · KANNAPOLIS · NOW (CC0)', colour=1, z=(1.0, 1.08)),
}
scenes, vo, subs, t, prev = [], {}, [], LEAD, None
for l in L:
    ch = l['chapter']
    if ch != prev and CH[ch][0]:
        scenes.append(dict(type='chapter', t0=round(t, 2), num=CH[ch][0], title=CH[ch][1], img=CHIMG[ch])); t += CARD
    prev = ch; d = DUR[l['id']]
    sh = dict(S[l['id']]); sh['t0'] = round(t, 2); sh['line'] = l['id']; scenes.append(sh)
    vo[l['id']] = round(t, 3)
    parts = l['subs']; n = sum(len(p) for p in parts); tt = t
    for i, p in enumerate(parts):
        dd = d * len(p) / n; subs.append([round(tt - .1, 2), round(tt + dd + (.3 if i == len(parts) - 1 else .02), 2), p]); tt += dd
    t += d + GAP
for i in range(len(subs) - 1): subs[i][1] = round(min(subs[i][1], subs[i + 1][0] - .02), 2)
scenes.append(dict(type='end', t0=round(t + .6, 2)))
dur = round(t + .6 + END, 1)
for i, s in enumerate(scenes): s['t1'] = scenes[i + 1]['t0'] if i + 1 < len(scenes) else dur
F = dict(dur=dur, scenes=scenes, vo=vo, subs=subs)
json.dump(F, open(os.path.join(D, 'film.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump([{'t0': a, 't1': b, 'text': s} for a, b, s in subs], open(os.path.join(D, 'audio/cues.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('scenes', len(scenes), 'subs', len(subs), 'duration', dur, 's =', round(dur / 60, 1), 'min')
