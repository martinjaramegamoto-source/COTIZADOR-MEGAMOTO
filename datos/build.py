import json, os
D = os.path.dirname(os.path.abspath(__file__))
rows = []
for line in open(os.path.join(D, 'precios.tsv'), encoding='utf-8'):
    p = line.rstrip('\n').split('\t')
    if len(p) < 7: continue
    m, mod, lista, lp, pvp, pat, gba = p
    rows.append(dict(marca=m, modelo=mod, lista=int(lista), listaPat=int(lp), pvp=int(pvp), pat=int(pat), gba=int(gba)))

pren = {
 'GIXXER 150i ABS': (2959166, 347083), 'V-STROM 250': (4435412, 541917), 'DR - 650': (6234460, 740250),
 'V-STROM 650': (10188021, 1354442), 'MX 250 R': (3631567, 813920), 'MX 450 R': (5317798, 981739),
 '350R NEW': (4360766, 644668), '450 RALLY': (7186526, 1103972), '400X': (5321018, 647878),
 '525X': (4758702, 887687), '625 NEW': (7458649, 1050000), '800 XPRO': (10018092, 1200000),
 '800 RALLY': (8870625, 1331510), '800 GT': (9922442, 1317614), 'RK 150': (1613035, 177917),
 'TNT 15': (2000957, 215250), '180 S': (2319278, 335417), 'LEONCINO 250': (3396967, 463750),
 '302 S': (3577004, 656250), 'TRK 502 X': (5810328, 904750), 'TRK 702': (7278471, 978250),
 'TRK 702 X': (8799886, 1050583), 'TNT 600i': (9040122, 1124375), 'JET X': (2663107, 314417),
 'ORBIT III 125': (1657310, 203583), 'JET 14': (2535104, 273583), 'JOYRIDE 300i': (4046892, 483583),
 'MAXSYM TL 508': (12933471, 1224417), 'SC 150': (2839048, 242200), 'F 352': (4515236, 582803),
 'N 300': (2711122, 434467), 'M 502 N': (4336538, 855347), 'T250X': (2793148, 366917),
 'T352X': (5173400, 658583), 'T502X': (6905516, 833583), 'T 1002 VX': (10558583, 1050000),
 'RTR 200 EFI': (2414146, 275875), 'MODENA 150': (1814728, 224583), 'OLTRE 150': (2032513, 249375),
 'LIGURIA 155': (2068199, 246866), 'TROVARE 475': (5733738, 641083),
}
for r in rows:
    if r['modelo'] in pren:
        a, c = pren[r['modelo']]
        r['prenAnt'], r['prenCuota'] = a, c

promo = json.load(open(os.path.join(D, 'promo.json'), encoding='utf-8'))
data = dict(fecha='10/10/2026', motos=rows, promo=promo)
html = open(os.path.join(D, 'template.html'), encoding='utf-8').read()
html = html.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
pass
open(os.path.join(D, '..', 'index.html'), 'w', encoding='utf-8').write(html)
print(len(rows), 'motos,', sum(1 for r in rows if 'prenAnt' in r), 'con prendario')
