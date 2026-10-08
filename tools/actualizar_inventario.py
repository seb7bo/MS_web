"""Actualiza el inventario de motores TECO-Westinghouse en industrialproducts.html.

Uso (desde la carpeta del sitio):
    python tools/actualizar_inventario.py

Lee data/inventario_teco.csv y regenera:
  - las filas de la tabla de inventario,
  - los totales (modelos, unidades, baja/media tensión, rango de HP),
  - la descripción para Google y los datos estructurados (JSON-LD),
  - la fecha "Inventario actualizado a ..." y el <lastmod> del sitemap.

Columnas del CSV:
  modelo       catálogo TECO, p. ej. KPF8002 (se usa para el datasheet SUB_<modelo>.pdf)
  hp           potencia en HP
  polos        2, 4, 6 u 8
  tension      460  ó  2300/4160
  disponibles  unidades en stock; con 0 el modelo no se muestra
  manual       143-449  (carcasas 143T a 449T)  ó  5000  (carcasa 5000 y mayores)
"""
import csv, json, re, sys, urllib.parse
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / 'data' / 'inventario_teco.csv'
HTML = RAIZ / 'industrialproducts.html'
SITEMAP = RAIZ / 'sitemap.xml'

MANUALES = {
    '143-449': 'https://buy.tecowestinghouse.com/EcommerceFiles/Manuals/TWMC%20Instruction%20Manual_143%20to%20449%20frame.pdf',
    '5000': 'https://www.tecowestinghouse.com/PDF/O%26M_manual_5000_larger.pdf',
}
DATASHEET = 'https://buy.tecowestinghouse.com/EcommerceFiles/submittals/SUB_{}.pdf'
RPM = {2: 3600, 4: 1800, 6: 1200, 8: 900}
MESES_ES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
            'septiembre', 'octubre', 'noviembre', 'diciembre']
MESES_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']


def fmt(n):
    return f'{n:,}'


def error(msg):
    sys.exit(f'ERROR: {msg}')


def leer_csv():
    filas = []
    with open(CSV, encoding='utf-8-sig', newline='') as f:
        for i, r in enumerate(csv.DictReader(f), start=2):
            try:
                m = r['modelo'].strip().upper()
                hp, p, q = int(r['hp']), int(r['polos']), int(r['disponibles'])
                t = r['tension'].replace(',', '').replace(' ', '').strip()
                man = r['manual'].strip()
            except (KeyError, ValueError) as e:
                error(f'línea {i} del CSV: {e}')
            if not m:
                error(f'línea {i}: falta el modelo')
            if p not in RPM:
                error(f'línea {i} ({m}): polos debe ser 2, 4, 6 u 8')
            if t not in ('460', '2300/4160'):
                error(f'línea {i} ({m}): tension debe ser 460 o 2300/4160')
            if man not in MANUALES:
                error(f'línea {i} ({m}): manual debe ser 143-449 o 5000')
            if q < 0:
                error(f'línea {i} ({m}): disponibles no puede ser negativo')
            if q == 0:
                continue
            filas.append(dict(m=m, hp=hp, p=p, q=q, lv=(t == '460'),
                              v=('460' if t == '460' else '2,300/4,160'), man=man))
    if not filas:
        error('el CSV no tiene modelos con existencias')
    modelos = [f['m'] for f in filas]
    dup = {x for x in modelos if modelos.count(x) > 1}
    if dup:
        error('modelos repetidos: ' + ', '.join(sorted(dup)))
    filas.sort(key=lambda r: (not r['lv'], r['hp'], r['p'], r['m']))
    return filas


def fila_html(r, qmax):
    subj = f"Cotización motor TECO-Westinghouse {r['m']} ({r['hp']} HP, {r['p']} polos, {r['v']} V)"
    mail = 'mailto:contacto@marasesupply.com?subject=' + urllib.parse.quote(subj)
    tens = 'bt' if r['lv'] else 'mt'
    return f'''          <tr data-m="{r['m']}" data-hp="{r['hp']}" data-p="{r['p']}" data-t="{tens}" data-q="{r['q']}">
            <th scope="row" data-l="model"><span class="brand-s">TECO-Westinghouse</span><span class="mdl">{r['m']}</span></th>
            <td data-l="hp"><b>{fmt(r['hp'])}</b> HP</td>
            <td data-l="poles">{r['p']}</td>
            <td data-l="rpm">{fmt(RPM[r['p']])}</td>
            <td data-l="volt">{r['v']} V</td>
            <td data-l="qty"><span class="qty"><b>{r['q']}</b><span class="qbar"><i style="--q:{r['q'] / qmax:.3f}"></i></span></span></td>
            <td data-l="docs" class="docs"><a href="{DATASHEET.format(r['m'])}" target="_blank" rel="noopener" title="Datasheet TECO-Westinghouse {r['m']} (PDF)">Datasheet</a><a href="{MANUALES[r['man']]}" target="_blank" rel="noopener" title="Manual de instrucciones (PDF)" data-en="Manual">Manual</a></td>
            <td class="act"><a class="qt" href="{mail}" data-en="Quote">Cotizar</a></td>
          </tr>'''


def json_ld(filas):
    items = []
    for i, r in enumerate(filas):
        items.append({"@type": "ListItem", "position": i + 1, "item": {
            "@type": "Product",
            "name": f"Motor TECO-Westinghouse {r['m']} {r['hp']} HP {r['p']} polos {r['v']} V",
            "subjectOf": [
                {"@type": "DigitalDocument", "name": f"Datasheet {r['m']}", "encodingFormat": "application/pdf",
                 "url": DATASHEET.format(r['m'])},
                {"@type": "DigitalDocument", "name": "Manual de instrucciones", "encodingFormat": "application/pdf",
                 "url": MANUALES[r['man']].replace('%26', '&')},
            ],
            "model": r['m'],
            "brand": {"@type": "Brand", "name": "TECO-Westinghouse"},
            "category": "Motores eléctricos " + ("de baja tensión" if r['lv'] else "de media tensión"),
            "description": (f"Motor eléctrico TECO-Westinghouse modelo {r['m']}, {r['hp']} HP, {r['p']} polos "
                            f"({fmt(RPM[r['p']])} RPM síncronas a 60 Hz), {r['v']} V. En stock en MARASE Supply, "
                            f"México. Precio y entrega por cotización."),
            "additionalProperty": [
                {"@type": "PropertyValue", "name": "Potencia", "value": r['hp'], "unitText": "HP"},
                {"@type": "PropertyValue", "name": "Polos", "value": r['p']},
                {"@type": "PropertyValue", "name": "Velocidad síncrona", "value": RPM[r['p']], "unitText": "RPM"},
                {"@type": "PropertyValue", "name": "Tensión", "value": r['v'] + " V"},
            ]}})
    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "name": "Motores TECO-Westinghouse en stock — MARASE Supply",
          "numberOfItems": len(filas), "itemListElement": items}
    return '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>'


def reemplazar(s, patron, nuevo, nombre):
    s2, n = re.subn(patron, nuevo, s, flags=re.S)
    if n == 0:
        error(f'no encontré en la página: {nombre}. ¿Se modificó esa parte del HTML?')
    return s2


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    filas = leer_csv()
    N = len(filas)
    U = sum(r['q'] for r in filas)
    NLV = sum(1 for r in filas if r['lv'])
    NMV = N - NLV
    HPMIN, HPMAX = min(r['hp'] for r in filas), max(r['hp'] for r in filas)
    QMAX = max(r['q'] for r in filas)
    hoy = date.today()
    mes_es, mes_en = f'{MESES_ES[hoy.month - 1]} de {hoy.year}', f'{MESES_EN[hoy.month - 1]} {hoy.year}'
    rango = f'{HPMIN}–{fmt(HPMAX)}'

    s = HTML.read_text(encoding='utf-8')
    tbody = '\n'.join(fila_html(r, QMAX) for r in filas)
    s = reemplazar(s, r'(<table class="inv-table" id="invTable">.*?<tbody>\n).*?(\n\s*</tbody>)',
                   lambda m: m.group(1) + tbody + m.group(2), 'tabla de inventario')
    s = reemplazar(s, r'<script type="application/ld\+json">.*?</script>', lambda m: json_ld(filas), 'datos estructurados')
    s = reemplazar(s, r'(<b data-count=")\d+(">)\d+(</b><span data-en="Models in stock">)',
                   lambda m: f'{m.group(1)}{N}{m.group(2)}{N}{m.group(3)}', 'contador de modelos')
    s = reemplazar(s, r'(<b data-count=")\d+(">)\d+(</b><span data-en="Units available">)',
                   lambda m: f'{m.group(1)}{U}{m.group(2)}{U}{m.group(3)}', 'contador de unidades')
    s = reemplazar(s, r'<b>[\d,]+–[\d,]+</b>(<span data-en="Horsepower range)',
                   lambda m: f'<b>{rango}</b>{m.group(1)}', 'rango de HP')
    s = reemplazar(s, r'<li data-en="From [\d,]+ to [\d,]+ HP, 2 to 8 poles">De [\d,]+ a [\d,]+ HP, de 2 a 8 polos</li>',
                   f'<li data-en="From {HPMIN} to {fmt(HPMAX)} HP, 2 to 8 poles">De {HPMIN} a {fmt(HPMAX)} HP, de 2 a 8 polos</li>',
                   'lista de rango de HP')
    s = reemplazar(s, r'(data-en="TECO motors in stock">Motores TECO en stock · )\d+( modelos)',
                   lambda m: f'{m.group(1)}{N}{m.group(2)}', 'botón de la portada')
    s = reemplazar(s, r'<p data-en="\d+ models and \d+ units available.*?</p>',
                   (f'<p data-en="{N} models and {U} units available for delivery: {NLV} low voltage (460 V) and '
                    f'{NMV} medium voltage (2,300/4,160 V). Price and lead time by quotation.">{N} modelos y {U} '
                    f'unidades disponibles para entrega: {NLV} de baja tensión (460 V) y {NMV} de media tensión '
                    f'(2,300/4,160 V). Precio y tiempo de entrega por cotización.</p>'),
                   'párrafo del inventario')
    s = reemplazar(s, r'Inventory updated [A-Za-z]+ \d{4}\.', f'Inventory updated {mes_en}.', 'fecha (inglés)')
    s = reemplazar(s, r'Inventario actualizado a [a-z]+ de \d{4}\.', f'Inventario actualizado a {mes_es}.', 'fecha (español)')
    s = reemplazar(s, r'<meta name="description" content="Motores TECO-Westinghouse en stock[^"]*">',
                   (f'<meta name="description" content="Motores TECO-Westinghouse en stock en México: {N} modelos de '
                    f'baja tensión 460 V y media tensión 2,300/4,160 V, de {HPMIN} a {fmt(HPMAX)} HP y de 2 a 8 polos. '
                    f'También bombas, sopladores, instrumentación TTR y PQM, cable y consumibles. Por cotización y con '
                    f'contacto directo.">'), 'meta description')
    s = reemplazar(s, r'<meta property="og:description" content="[^"]*">',
                   (f'<meta property="og:description" content="{N} modelos de motores TECO-Westinghouse en stock, de '
                    f'{HPMIN} a {fmt(HPMAX)} HP, en baja y media tensión. Por cotización y con contacto directo.">'),
                   'og:description')
    HTML.write_text(s, encoding='utf-8', newline='')

    if SITEMAP.exists():
        sm = SITEMAP.read_text(encoding='utf-8')
        sm = re.sub(r'(<loc>https://marasesupply.com/industrialproducts.html</loc><lastmod>)[\d-]+(</lastmod>)',
                    lambda m: f'{m.group(1)}{hoy.isoformat()}{m.group(2)}', sm)
        SITEMAP.write_text(sm, encoding='utf-8', newline='\n')

    print(f'Listo: {N} modelos ({NLV} baja, {NMV} media tensión), {U} unidades, {HPMIN}–{fmt(HPMAX)} HP.')
    print(f'Fecha de actualización: {mes_es}.')


if __name__ == '__main__':
    main()
