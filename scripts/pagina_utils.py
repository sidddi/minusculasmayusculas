"""Utilidades para editar las páginas HTML a mano de forma segura.

Cada sustitución exige que el texto original aparezca exactamente una vez;
si no, el script se detiene en lugar de dejar la página a medias.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def leer(nombre):
    with open(os.path.join(ROOT, nombre), encoding='utf-8') as f:
        return f.read()


def escribir(nombre, s):
    with open(os.path.join(ROOT, nombre), 'w', encoding='utf-8') as f:
        f.write(s)


def sustituir(s, viejo, nuevo, pagina=''):
    n = s.count(viejo)
    if n != 1:
        raise SystemExit(f'[{pagina}] se esperaba 1 aparición y hay {n}: {viejo[:80]!r}')
    return s.replace(viejo, nuevo)


def insertar_antes(s, marca, bloque, pagina=''):
    return sustituir(s, marca, bloque + marca, pagina)


def bloque_details(s, resumen_parcial, pagina=''):
    """Devuelve el <details>…</details> cuyo <summary> contiene el texto dado."""
    patron = re.compile(r'[ \t]*<details>\s*<summary>(?:(?!</details>).)*?' + re.escape(resumen_parcial)
                        + r'(?:(?!</details>).)*?</details>\n?', re.S)
    m = list(patron.finditer(s))
    if len(m) != 1:
        raise SystemExit(f'[{pagina}] FAQ no encontrada o repetida ({len(m)}): {resumen_parcial!r}')
    return m[0].group(0)


def cambiar_faq(s, resumen_parcial, nuevo, pagina=''):
    viejo = bloque_details(s, resumen_parcial, pagina)
    return s.replace(viejo, nuevo)


def faq(pregunta, *parrafos):
    cuerpo = '\n'.join(f'          <p>\n            {p}\n          </p>' for p in parrafos)
    return f'''        <details>
          <summary>{pregunta}</summary>
{cuerpo}
        </details>

'''


def texto_plano(fragmento):
    t = re.sub(r'<[^>]+>', '', fragmento)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def sincronizar_faq_jsonld(s, pagina=''):
    """Regenera el JSON-LD FAQPage a partir de las preguntas visibles."""
    sec = re.search(r'<section class="faq-section".*?</section>', s, re.S)
    if not sec:
        return s
    items = []
    for d in re.finditer(r'<details>\s*<summary>(.*?)</summary>(.*?)</details>', sec.group(0), re.S):
        items.append({
            '@type': 'Question',
            'name': texto_plano(d.group(1)),
            'acceptedAnswer': {'@type': 'Answer', 'text': texto_plano(d.group(2))},
        })
    nuevo = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': items}
    bloque = re.search(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>', s, re.S)
    if not bloque:
        raise SystemExit(f'[{pagina}] no hay bloque FAQPage')
    js = json.dumps(nuevo, ensure_ascii=False, indent=2).replace('\n', '\n  ')
    return s.replace(bloque.group(0), '<script type="application/ld+json">\n  ' + js + '\n  </script>')


def relacionados(titulo, items):
    lis = '\n'.join(f'          <li><a href="{h}">{t}</a><span>{d}</span></li>' for h, t, d in items)
    return f'''      <section class="related-section" aria-label="{titulo}">
        <h2>{titulo}</h2>
        <ul class="related-list">
{lis}
        </ul>
      </section>

'''
