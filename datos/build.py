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

pren = {
 'GIXXER 150i ABS': (2959166, 347083), 'V-STROM 250': (4435412, 541917), 'DR - 650': (6183338, 752500),
 'V-STROM 650': (13406051, 1200000), '450RR (PISTA)': (8926383, 950900), 'MX 250 R': (3529636, 919814),
 'MX 450 R': (5811562, 981739), '350R NEW': (4671720, 644668), '450 RALLY': (7817982, 1103972),
 '400X': (5007498, 683829), '525X': (6004943, 887687), '625 NEW': (7373469, 1059767),
 '800 XPRO': (10018092, 1200000), '800 RALLY': (10017791, 1200000), '800 GT': (10172072, 1200000),
 'RK 150': (1613035, 177917), 'TNT 15': (2000957, 215250), '180 S': (2319278, 335417),
 'LEONCINO 250': (3396967, 463750), '302 S': (3577004, 656250), 'LEONCINO 500 TRAIL': (3588079, 740250),
 'TRK 502 X': (5810328, 904750), 'TRK 702': (7278471, 978250), 'TRK 702 X': (8799886, 1050583),
 'TNT 600i': (9040122, 1124375), 'JET X': (2663107, 314417), 'ORBIT III 125': (1657310, 203583),
 'JET 14': (2295755, 273583), 'JOYRIDE 300i': (4046892, 483583), 'MAXSYM TL 508': (12933471, 1224417),
 'SC 150': (2839048, 242200), 'F 352': (4515236, 582803), 'N 300': (2711122, 434467),
 'M 502 N': (4336538, 855347), 'T250X': (2793148, 366917), 'T352X': (5173400, 658583),
 'T502X': (6905516, 833583), 'T 1002 VX': (10558583, 1050000), 'RTR 200 EFI': (2414146, 275875),
 'MODENA 150': (1814728, 224583), 'OLTRE 150': (2032513, 249375), 'LIGURIA 155': (2068199, 246866),
 'MODENA 300': (3240805, 384417), 'TROVARE 475': (5733738, 641083),
}
# anticipo del prendario patentando en CABA (columna "Anticipo CABA" de la hoja "promo en pesos"); la cuota es la misma
prenCaba = {
 'GIXXER 150i ABS': 3131012, 'V-STROM 250': 4698669, 'DR - 650': 6548893, 'V-STROM 650': 14095963,
 '450RR (PISTA)': 9418353, 'MX 250 R': 3860119, 'MX 450 R': 6239753, '350R NEW': 4964710, '450 RALLY': 7617074,
 '400X': 5638473, '525X': 6398457, '625 NEW': 7851703, '800 XPRO': 10608692, '800 RALLY': 10608638,
 '800 GT': 10767370, 'RK 150': 1702735, 'TNT 15': 2111777, '180 S': 2470148, 'LEONCINO 250': 3396967,
 '302 S': 4329966, 'LEONCINO 500 TRAIL': 3874440, 'TRK 502 X': 6203718, 'TRK 702': 7733640, 'TRK 702 X': 9317998,
 'TNT 600i': 9584100, 'JET X': 2817925, 'ORBIT III 125': 1754681, 'JET 14': 2429185, 'JOYRIDE 300i': 4283157,
 'MAXSYM TL 508': 13616742, 'SC 150': 2981338, 'F 352': 4791562, 'N 300': 2793088, 'M 502 N': 4630157,
 'T250X': 2965524, 'T352X': 5488306, 'T502X': 7312065, 'T 1002 VX': 11127296, 'RTR 200 EFI': 3399083,
 'MODENA 150': 1922024, 'OLTRE 150': 2410976, 'LIGURIA 155': 2490580, 'MODENA 300': 3428290, 'TROVARE 475': 6063438,
}
for r in rows:
    if r['modelo'] in pren:
        a, c = pren[r['modelo']]
        r['prenAnt'], r['prenCuota'] = a, c
        if r['modelo'] in prenCaba: r['prenAntCaba'] = prenCaba[r['modelo']]

promo = json.load(open(os.path.join(D, 'promo.json'), encoding='utf-8'))
data = dict(fecha='10/10/2026', motos=rows, promo=promo)
html = open(os.path.join(D, 'template.html'), encoding='utf-8').read()
html = html.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
pass
open(os.path.join(D, '..', 'index.html'), 'w', encoding='utf-8').write(html)
print(len(rows), 'motos,', sum(1 for r in rows if 'prenAnt' in r), 'con prendario')
