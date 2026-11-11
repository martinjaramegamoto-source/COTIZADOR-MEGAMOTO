import json, os
D = os.path.dirname(os.path.abspath(__file__))
rows = []
for line in open(os.path.join(D, 'precios.tsv'), encoding='utf-8'):
    p = line.rstrip('\n').split('\t')
    if len(p) < 7: continue
    m, mod, lista, lp, pvp, pat, gba = p[:7]
    r = dict(marca=m, modelo=mod, lista=int(lista), listaPat=int(lp), pvp=int(pvp), pat=int(pat), gba=int(gba))
    if len(p) > 7 and p[7]:
        r['caba'] = int(p[7])                      # Moto+Pat CABA (contado patentada en CABA)
        r['listaPatCaba'] = r['lista'] + r['caba'] - r['pvp']   # lista + patentamiento CABA
    rows.append(r)

pren = {'LIGURIA 155': (2164572, 246866), 'MODENA 150': (1815600, 224483), 'OLTRE 150': (2047275, 249375), 'MODENA 300': (3240805, 384417), 'TROVARE 475': (4975393, 641083), 'TNT 15': (1853343, 220317), '180 S': (2827833, 341150), '302 S': (5972697, 656250), 'TNT 600i': (9722586, 1124375), 'LEONCINO 250': (3814645, 463750), 'LEONCINO 500 TRAIL': (5483446, 740250), 'TRK 502 X': (6949170, 903650), 'TRK 702': (7703444, 1007817), 'TRK 702 X': (8281397, 1078650), 'SC 150': (3537437, 242200), 'N 300': (2789507, 434467), 'F 352': (4515236, 582803), 'M 502 N': (4928156, 855347), 'T250X': (2793148, 366917), 'T352X': (5173400, 658583), 'T502X': (6905516, 833583), 'T 1002 VX': (10558583, 1050000), 'RK 150': (1602953, 177917), 'ORBIT III 125': (1799893, 203583), 'JET X': (2631803, 156825), 'JET 14': (2295755, 273583), 'JOYRIDE 300i': (4053239, 483583), 'MAXSYM TL 508': (8460358, 1224417), 'GIXXER 150i ABS': (2960038, 346983), 'V-STROM 250': (4442098, 541150), 'DR - 650': (6187843, 751983), 'V-STROM 650': (11368446, 1433650), 'V-STROM 800': (14058745, 1719483), 'MX 250 R': (5351294, 919814), 'MX 450 R': (5711562, 981739), '450 RALLY': (7817982, 1103972), '350R NEW': (4673330, 644483), '450RR (PISTA)': (7550683, 1108650), '400X': (4946906, 683650), '525X': (6278772, 886983), '625 NEW': (7375947, 1059483), '800 RALLY': (8874064, 1331150), '800 GT': (9151889, 1316983), '800 XPRO': (8917325, 1337817), 'RTR 200 EFI': (3330824, 275875)}
# anticipo del prendario patentando en CABA (columna "Anticipo CABA"); la cuota es la misma
prenCaba = {'LIGURIA 155': 2281015, 'MODENA 150': 1922896, 'OLTRE 150': 2167332, 'MODENA 300': 3428290, 'TROVARE 475': 5275852, 'TNT 15': 1960883, '180 S': 2994265, '302 S': 6305276, 'TNT 600i': 10285893, 'LEONCINO 250': 4039399, 'LEONCINO 500 TRAIL': 5824560, 'TRK 502 X': 7374495, 'TRK 702': 8178272, 'TRK 702 X': 8790650, 'SC 150': 3699317, 'N 300': 2977820, 'F 352': 4791562, 'M 502 N': 5238260, 'T250X': 2965524, 'T352X': 5488306, 'T502X': 7312065, 'T 1002 VX': 11127296, 'RK 150': 1692570, 'ORBIT III 125': 1900890, 'JET X': 2785148, 'JET 14': 2429185, 'JOYRIDE 300i': 4289088, 'MAXSYM TL 508': 9013485, 'GIXXER 150i ABS': 3131884, 'V-STROM 250': 4705355, 'DR - 650': 6553398, 'V-STROM 650': 12058358, 'V-STROM 800': 14896839, 'MX 250 R': 5752477, 'MX 450 R': 6139754, '450 RALLY': 8320250, '350R NEW': 4966320, '450RR (PISTA)': 8042653, '400X': 5257995, '525X': 6680318, '625 NEW': 7854181, '800 RALLY': 9464911, '800 GT': 9747187, '800 XPRO': 9511097, 'RTR 200 EFI': 3492117}
# planes que no son 12 cuotas fijas (ej. UVA)
prenExtra = {'JET X': {'prenN': 24, 'prenUva': True}}
for r in rows:
    if r['modelo'] in pren:
        a, c = pren[r['modelo']]
        r['prenAnt'], r['prenCuota'] = a, c
        if r['modelo'] in prenCaba: r['prenAntCaba'] = prenCaba[r['modelo']]
        r.update(prenExtra.get(r['modelo'], {}))

promo = json.load(open(os.path.join(D, 'promo.json'), encoding='utf-8'))
data = dict(fecha='10/10/2026', motos=rows, promo=promo)
html = open(os.path.join(D, 'template.html'), encoding='utf-8').read()
html = html.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
pass
open(os.path.join(D, '..', 'index.html'), 'w', encoding='utf-8').write(html)
print(len(rows), 'motos,', sum(1 for r in rows if 'prenAnt' in r), 'con prendario')
