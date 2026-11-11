#!/usr/bin/env python3
"""Genera catalogo/index.html (sin precios) a partir de precios.tsv + catalogo_meta.py + fuentes/*.json.
Uso: python3 datos/build_catalogo.py
"""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from catalogo_meta import META

F = lambda n: json.load(open(os.path.join(D, 'fuentes', n + '.json')))

# ---------- planilla: solo marca + modelo (los precios NO se usan) ----------
rows = []
for ln in open(os.path.join(D, 'precios.tsv'), encoding='utf-8'):
    p = ln.rstrip('\n').split('\t')
    if len(p) < 2 or p[0].lower() == 'marca':
        continue
    rows.append((p[0].strip(), p[1].strip()))

def num(s):
    m = re.search(r'[\d]+(?:[.,]\d+)?', str(s or ''))
    return float(m.group(0).replace(',', '.')) if m else None

def fmt(x, dec=1):
    if x is None: return ''
    s = f'{x:.{dec}f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',')

def unit(v, u):
    """'13,4' -> '13,4 HP'; deja tal cual si ya trae unidad."""
    v = str(v or '').strip()
    if not v: return ''
    return v if re.search(r'[A-Za-z³]', v) else f'{v} {u}'

def cv_from(power):
    """'60 kW' -> '82 CV'; '12 HP' -> '12 HP'."""
    if not power: return ''
    if 'kw' in power.lower():
        return fmt(num(power) * 1.36, 0) + ' CV'
    return power

# ---------- fuentes por marca -> {modelo: {img, specs{}}} ----------
SRC = {}

def put(modelo, img='', **sp):
    sp = {k: v for k, v in sp.items() if v not in (None, '', 0)}
    SRC[modelo] = {'img': img, 'sp': sp}

# Motomel: claves por slug del sitio
MOTOMEL_SLUG = {
    'BLITZ ONE START': 'blitz-one-110', 'BLITZ ONE FULL': 'blitz-one-full', 'BLITZ PLUS': 'blitz-plus',
    'BLITZ AUTOMATICA': 'blitz-110-automatica', 'BLITZ TUNNING': 'blitz-110-v8-tunning', 'DLX 110 DELUXE': 'dlx-deluxe',
    'MAX 110': 'max-110', 'S2 START': 's2-150', 'S2 FULL ALEACION': 'nueva-s2-150-full-aleacion', 'SIRIUS 190': 'sirius-190',
    'VICTORY 150': 'victory-150', 'SKUA 125 X-TREME': 'skua-125-xtreme', 'SKUA 150': 'skua-150', 'SKUA 250': 'skua-250',
    'XMM 250 1.9': 'xmm-250', 'SHARK 150': 'shark-150', 'STRATO e': 'stratoe', 'STRATO EURO 150': 'strato-euro-150-led',
    'STRATO ALPINO': 'strato-alpino-150'}
mm = F('motomel')
for mod, slug in MOTOMEL_SLUG.items():
    if slug not in mm: continue
    img, s = mm[slug]
    caja = s.get('caja', '')
    if caja and 'vel' not in caja: caja += ' velocidades'
    if s.get('emb') == 'Autom' and caja: caja += ' (embrague automático)'
    put(mod, mm['base'] + img if img else '', cc=s.get('cc'), hp=unit(s.get('hp'), 'HP'), peso=s.get('peso'),
        tanque=s.get('tanque'), caja=caja or ('Automática (CVT)' if mod.startswith('STRATO') else ''),
        freno=('Disco delantero' if s.get('fd') else ''), seg=s.get('abs'), llantas=s.get('llanta'))

# Formato [img, specs] con claves cc/hp/par/peso/tanque/caja/asiento/abs/extra
for marca in ('suzuki', 'kove', 'sym', 'malaguti'):
    d = F(marca)
    for mod, v in d.items():
        if mod == 'base': continue
        img, s = v
        caja = s.get('caja', '')
        if caja and caja.isdigit(): caja += ' velocidades'
        if marca in ('sym', 'malaguti'): caja = caja or 'Automática (CVT)'
        put(mod, d['base'] + img if img else '', cc=s.get('cc'), hp=s.get('hp'), par=s.get('par'), peso=s.get('peso'),
            tanque=s.get('tanque'), caja=caja, asiento=s.get('asiento'), seg=s.get('abs'), extra=s.get('extra'))

# Benelli / Keeway: img + spec (Nuxt)
for marca in ('benelli', 'keeway'):
    d = F(marca)
    for mod in set(d['img']) | set(d.get('spec', {})):
        s = d.get('spec', {}).get(mod, {})
        img = d['img'].get(mod, '')
        put(mod, d['base'] + img if img else '', cc=unit(s.get('displacement'), 'cc'), hp=cv_from(s.get('power')),
            par=s.get('max-torque'), tanque=unit(s.get('fuel-capacity'), 'L'), asiento=unit(s.get('seat-height'), 'mm'),
            freno=s.get('front-brakes'), vmax=unit(s.get('top-speed'), 'km/h'), seg='ABS' if s.get('abs') else '')

# Morbidelli: solo imágenes (specs de las prioritarias abajo)
d = F('morbidelli')
for mod, img in d['img'].items():
    put(mod, d['base'] + img)

# TVS
d = F('tvs')
for mod, img in d['img'].items():
    base_mod = mod.replace(' ABS', '')
    s = d['spec'].get(mod) or d['spec'].get(base_mod, {})
    caja = s.get('caja', '')
    if caja.isdigit(): caja += ' velocidades'
    put(mod, d['base'] + img, cc=unit(s.get('cc'), 'cc'), hp=s.get('hp'), par=unit(s.get('nm'), 'Nm'),
        peso=unit(s.get('peso'), 'kg'), tanque=unit(s.get('tanque'), 'L'), caja=caja,
        seg='ABS' if mod.endswith('ABS') else '', extra=s.get('extra'))

# IKA
d = F('ika')
for mod, img in d['img'].items():
    put(mod, d['base'] + img)

# ---------- fichas detalladas de las prioritarias (doc del proyecto catalogo-specs.md) ----------
DET = {
 '800 XPRO': dict(motor='Bicilíndrico DOHC 8v, refrigeración líquida', cc='799 cc', hp='94,5 CV', par='80 Nm', caja='6 velocidades + quickshifter',
   peso='190 kg (odm)', asiento='865-875 mm', tanque='20 L', susp='KYB invertida 48 mm / mono KYB, multiajustables', freno='Doble disco 310 mm / disco 220 mm',
   seg='ABS doble canal desconectable', llantas='Rayos tubeless 21"/18"', extra='Control de tracción, 3 modos, crucero, TFT 7" con mirroring, full LED. Despeje 275 mm. Garantía 3 años'),
 '800 RALLY': dict(cc='799 cc', hp='94,5 CV', par='79 Nm', caja='6 velocidades', peso='176 kg (odm)', asiento='895 mm', tanque='19 L',
   susp='Invertida 49 mm / mono piggyback, regulables', freno='Disco 310 mm / 240 mm', seg='ABS desconectable', llantas='Rayos 21"/18"',
   extra='Despeje 293 mm. 2 modos de manejo, TFT 7"'),
 '800 GT': dict(cc='799 cc', hp='94,5 CV', par='79 Nm', caja='6 velocidades + quickshifter', peso='195 kg (odm)', asiento='826 mm', tanque='22 L',
   susp='KYB invertida 43 mm / mono, regulables', freno='Doble disco 310 mm / 220 mm', seg='ABS en curva (IMU Bosch)', llantas='Aleación 19"/17" tubeless',
   extra='Control de tracción, 4 modos, crucero, puños y asiento calefactables, TPMS, cubremanos'),
 '525X': dict(motor='Bicilíndrico DOHC, refrigeración líquida', cc='494 cc', hp='53 HP', par='50,5 Nm', caja='6 velocidades', tanque='20 L',
   freno='Doble disco Brembo / disco Brembo', seg='ABS doble canal desconectable', extra='Velocidad máxima 170 km/h. Garantía 3 años'),
 'DR - 650': dict(motor='Monocilíndrico 4T, aire/aceite', cc='644 cc', hp='43 CV', caja='5 velocidades', peso='166 kg', asiento='885 mm', tanque='13 L',
   freno='Disco / disco', llantas='Rayos 21"/17"', extra='Despeje 265 mm. Disponible para prueba de manejo'),
 'V-STROM 650': dict(motor='V-Twin 90° DOHC 8v, líquida', cc='645 cc', hp='70 CV', par='62 Nm', caja='6 velocidades', peso='216 kg', asiento='835 mm',
   tanque='20 L', freno='Doble disco / disco', seg='ABS doble canal', llantas='Rayos 19"/17" tubeless',
   extra='Chasis de aluminio. Incluye baúl Shad SH58X. Disponible para prueba de manejo'),
 'V-STROM 250': dict(motor='Monocilíndrico SOHC, refrigerado por aceite', cc='249 cc', hp='26,5 CV', par='22,2 Nm', caja='6 velocidades', peso='167 kg',
   tanque='12 L', seg='ABS doble canal', llantas='Aleación 19"/17"',
   extra='Incluye top case Shad TR41 de aluminio, parabrisas, cubrecárter y USB. Garantía 24 meses / 24.000 km'),
 'TRK 702': dict(motor='Bicilíndrico DOHC 8v, líquida', cc='698 cc', hp='76 CV', caja='6 velocidades', freno='Doble disco 320 mm / 260 mm',
   seg='ABS doble canal', extra='TFT con navegador, USB. Incluye kit de bauleras + top case'),
 'TRK 702 X': dict(cc='698 cc', hp='70 CV', par='70 Nm', caja='6 velocidades', peso='235 kg (odm)', asiento='835 mm', tanque='20 L',
   susp='Invertida 50 mm / mono, regulables', freno='Doble disco 320 mm / 260 mm', seg='ABS', llantas='Rayos 19"/17"',
   extra='Control de tracción, modos de manejo, TFT 5" con Bluetooth'),
 'TRK 502': dict(motor='Bicilíndrico DOHC 8v, líquida', cc='500 cc', hp='47,6 HP', par='45 Nm', caja='6 velocidades', asiento='800-825 mm',
   tanque='20 L', susp='Invertida 50 mm / mono', freno='Doble disco 320 mm / 260 mm', seg='ABS', llantas='Aleación 17"/17"'),
 'T352X': dict(motor='Bicilíndrico DOHC 8v, líquida', cc='349 cc', hp='40,9 CV', par='31,5 Nm', caja='6 velocidades, antirrebote', peso='180 kg (odm)',
   asiento='820 mm', tanque='18 L', susp='Invertida 41 mm / mono', freno='Disco 300 mm / 240 mm', seg='ABS Bosch (trasero desconectable)',
   llantas='Rayos 19"/17" tubeless', extra='Control de tracción, 3 modos, TFT 7", Bluetooth'),
 'T502X': dict(motor='Bicilíndrico DOHC 8v, líquida', cc='486 cc', hp='46,9 CV', par='45 Nm', caja='6 velocidades, antirrebote', peso='210 kg (odm)',
   asiento='830 mm', tanque='18 L', susp='Invertida 43 mm / mono', freno='Doble disco 300 mm / 240 mm', seg='ABS Bosch con modo off-road',
   llantas='Rayos 19"/17" tubeless', extra='TFT vertical 7", Morbidelli Connect con GPS, TPMS, USB/USB-C'),
}

# ---------- tipo legible ----------
TIPOS = [('calle110', 'Urbanas 110'), ('calle', 'Calle / naked'), ('scooter', 'Scooters'), ('aventura', 'Aventura / trail'),
         ('enduro', 'Enduro / cross'), ('deportiva', 'Deportivas'), ('custom', 'Custom')]
CORR = {'DURBAN 150': 'enduro', 'NEO 110 FULL': 'calle110'}  # correcciones de categoría

LABELS = [('motor', 'Motor'), ('cc', 'Cilindrada'), ('hp', 'Potencia'), ('par', 'Torque'), ('caja', 'Transmisión'), ('peso', 'Peso'),
          ('asiento', 'Altura de asiento'), ('tanque', 'Tanque'), ('susp', 'Suspensión'), ('freno', 'Frenos'), ('seg', 'Seguridad'),
          ('llantas', 'Llantas'), ('vmax', 'Velocidad máxima')]

motos, falt_img, vistos = [], [], set()
for marca, mod in rows:
    if mod in vistos: continue
    vistos.add(mod)
    if mod not in META:
        print('SIN META:', mod); continue
    cat, cc, foto, nombre = META[mod]
    cat = CORR.get(mod, cat)
    src = SRC.get(mod, {'img': '', 'sp': {}})
    sp = dict(src['sp']); sp.update(DET.get(mod, {}))
    if 'cc' not in sp and cc: sp['cc'] = f'{cc} cc'
    if mod == 'STRATO e': sp.pop('cc', None); sp['motor'] = 'Eléctrico'
    extra = sp.pop('extra', '')
    ficha = [[lab, str(sp[k])] for k, lab in LABELS if sp.get(k)]
    img = src['img']
    propia = f'img/{foto}.webp' if foto else ''
    if not img and not propia: falt_img.append(mod)
    motos.append(dict(id=re.sub(r'[^a-z0-9]+', '-', (marca + ' ' + nombre).lower()).strip('-'), marca=marca, nombre=nombre,
                      tipo=cat, cc=cc, img=img, img2=propia, ficha=ficha, extra=extra))

orden_marca = ['Kove', 'Suzuki', 'Benelli', 'Morbidelli', 'Keeway', 'SYM', 'Malaguti', 'Motomel', 'TVS', 'IKA', 'Benda']
motos.sort(key=lambda m: (orden_marca.index(m['marca']) if m['marca'] in orden_marca else 99, -m['cc'], m['nombre']))
marcas = [m for m in orden_marca if any(x['marca'] == m for x in motos)] + sorted({x['marca'] for x in motos} - set(orden_marca))

tpl = open(os.path.join(D, 'catalogo_template.html'), encoding='utf-8').read()
out = tpl.replace('/*DATA*/', 'const MOTOS=' + json.dumps(motos, ensure_ascii=False) + ';const MARCAS=' + json.dumps(marcas, ensure_ascii=False)
                  + ';const TIPOS=' + json.dumps(TIPOS, ensure_ascii=False) + ';')
os.makedirs(os.path.join(D, '..', 'catalogo'), exist_ok=True)
open(os.path.join(D, '..', 'catalogo', 'index.html'), 'w', encoding='utf-8').write(out)
print(f'{len(motos)} motos, {len(marcas)} marcas. Sin imagen: {falt_img}')
print('Specs vacías:', [m['nombre'] for m in motos if len(m['ficha']) <= 1])
