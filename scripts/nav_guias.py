#!/usr/bin/env python3
"""Añade el enlace «Guías» a la cabecera y los estilos comunes nuevos a las
páginas escritas a mano (herramientas, sobre, contacto y legales).
Es idempotente: si la página ya lo tiene, no la toca."""
import re
from pagina_utils import leer, escribir

PAGINAS = ['index.html', 'contador-palabras.html', 'contador-caracteres.html',
           'buscar-reemplazar.html', 'ordenar-lista.html', 'eliminar-duplicados.html',
           'numero-a-letra.html', 'invertir-texto.html', 'quitar-acentos.html',
           'eliminar-espacios.html', 'texto-aleatorio.html', 'sobre.html',
           'contacto.html']
# Las páginas legales usan una cabecera simple sin menú y no se tocan.

CSS = '''
    /* ── Enlace a guías, ejemplos y contenido relacionado ── */
    .nav-right { display: flex; align-items: center; gap: 6px; margin-left: auto; }
    .nav-link {
      padding: 8px 10px;
      font-size: 0.88rem;
      font-weight: 500;
      color: var(--primary);
      text-decoration: none;
      border-radius: var(--radius);
    }
    .nav-link:hover { background: var(--primary-light); }
    .ejemplo {
      background: #f8f9fa;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 10px 14px;
      margin: 0 0 14px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.85rem;
      line-height: 1.6;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      color: var(--text);
    }
    .why-section h3 { font-size: 1.02rem; font-weight: 600; margin: 18px 0 8px; color: var(--text); }
    .plain-list { margin: 0 0 12px 20px; }
    .plain-list li { font-size: 0.95rem; color: #3c4043; line-height: 1.7; margin-bottom: 6px; }
    .why-section code, details code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.86em;
      background: #f1f3f4;
      padding: 1px 5px;
      border-radius: 4px;
    }
    .related-section { margin-bottom: 36px; }
    .related-section h2 { font-size: 1.25rem; font-weight: 600; color: var(--text); margin-bottom: 14px; }
    .related-list { list-style: none; display: grid; gap: 8px; }
    .related-list li { border: 1px solid var(--border); border-radius: var(--radius); padding: 10px 14px; }
    .related-list a { font-weight: 600; color: var(--primary); text-decoration: none; }
    .related-list a:hover { text-decoration: underline; }
    .related-list span { display: block; font-size: 0.88rem; color: var(--muted); line-height: 1.55; margin-top: 2px; }
    @media (max-width: 420px) {
      .header-bar { flex-wrap: wrap; }
      .nav-link { padding: 8px 6px; }
    }
'''

for p in PAGINAS:
    s = leer(p)
    if 'class="nav-right"' in s:
        continue
    # Estilos: antes del primer </style>
    s = s.replace('</style>', CSS + '  </style>', 1)
    # Cabecera: envolver el menú de herramientas junto al enlace a guías
    m = re.search(r'(\n([ \t]*)<div class="tools-menu">.*?</nav>\s*</div>)', s, re.S)
    if not m:
        raise SystemExit(f'{p}: no encuentro el menú de herramientas')
    ind = m.group(2)
    bloque = m.group(1)
    nuevo = (f'\n{ind}<div class="nav-right">\n{ind}  <a class="nav-link" href="guias.html">Guías</a>'
             + bloque.replace('\n', '\n  ') + f'\n{ind}</div>')
    s = s.replace(bloque, nuevo, 1)
    escribir(p, s)
    print('ok', p)
