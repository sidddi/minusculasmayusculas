# Auditoría de contenido · minusculasmayusculas.com

Fecha: 4 de octubre de 2026. Rama: `adsense-content`.
Motivo: AdSense marca el sitio como «Contenido de poco valor» (27 jun 2026).

## 1. Cómo está construido el sitio

- HTML estático puro. Sin build, sin plantillas ni parciales: cada página repite su `<head>`, su CSS inline, la cabecera con el menú desplegable y el footer.
- `converter.js` es el único JS compartido (convertidor de la home). El resto de herramientas lleva su lógica inline.
- El sitemap se mantiene a mano.
- Despliegue: push a `main` → GitHub Actions → `git pull` en el servidor Hetzner (`.github/workflows/deploy.yml`). Todo lo que hay en el repo se publica, salvo `README.md` y `tests.html`, que el workflow borra.
- Todo el procesamiento de texto ocurre en el navegador (verificado leyendo el código de las 11 herramientas: no hay `fetch`, `XMLHttpRequest` ni formularios que envíen el texto).

## 2. Inventario (antes de los cambios)

Palabras de contenido propio = texto dentro de `<main>`, sin la interfaz de la herramienta, sin menú ni footer. «Compartido» = % de secuencias de 8 palabras que aparecen también en otra página.

| Página | Tipo | Palabras | Compartido | Notas |
|---|---|---:|---:|---|
| index.html | Herramienta | 1.045 | 1 % | Bien. FAQ de privacidad repetida en otras páginas |
| ordenar-lista.html | Herramienta | 840 | 5 % | FAQ falsa: dice que sin «ignorar mayúsculas» van primero las mayúsculas (ASCII); en realidad van primero las minúsculas. Errata «Per defecto» |
| texto-aleatorio.html | Herramienta | 836 | 0 % | Afirma que el lorem ipsum se usa «desde hace siglos»: dato no verificable |
| numero-a-letra.html | Herramienta | 803 | 1 % | Bug: «1500,5» sin céntimos da «coma cincuenta» |
| buscar-reemplazar.html | Herramienta | 813 | 3 % | Sin soporte de expresiones regulares; `$&` en el reemplazo se interpreta |
| contador-palabras.html | Herramienta | 823 | 1 % | Dice que los párrafos se separan por líneas en blanco: el código cuenta cada salto de línea |
| contador-caracteres.html | Herramienta | 849 | 3 % | SMS: confunde qué letras sacan el mensaje de GSM-7 (la ñ sí está en GSM-7). Errata «las primeras 125 caracteres» |
| eliminar-duplicados.html | Herramienta | 654 | 7 % | Por debajo de 800. FAQ casi idéntica a la de ordenar-lista |
| eliminar-espacios.html | Herramienta | 873 | 2 % | Bien |
| invertir-texto.html | Herramienta | 700 | 2 % | Afirma que no hay riesgo con caracteres especiales: falso con emojis compuestos y acentos combinados |
| quitar-acentos.html | Herramienta | 958 | 3 % | FAQ falsa: «ø se convierte en o» (no cambia; tampoco ł, ß, æ, œ) |
| guia-mayusculas-espanol.html | Guía | 686 | 0 % | Correcta, corta |
| guia-tildes-mayusculas.html | Guía | 560 | 0 % | Correcta, corta |
| guia-mayusculas-titulos.html | Guía | 609 | 0 % | Correcta, corta |
| guia-limites-caracteres.html | Guía | 652 | 0 % | Error: dice que la eñe saca el SMS de GSM-7 |
| guia-escribir-numeros.html | Guía | 633 | 0 % | Párrafo confuso («treinta y dos mil... no») |
| guias.html | Índice | 198 | 0 % | Lista plana, sin temas ni fechas |
| sobre.html | Identidad | 428 | 0 % | Sin metodología ni política de correcciones |
| contacto.html | Identidad | 230 | 0 % | Correcta |
| aviso-legal / privacidad / cookies | Legal | 620-690 | 0-2 % | Correctas (no se tocan) |

## 3. Diagnóstico

Lo técnico está bien: ads.txt, robots.txt, sitemap, canonicals, un solo `h1` por página, JSON-LD válido, sin imágenes sin `alt` (la única imagen es `og-image.png`, que no se muestra en página). El único enlace «roto» es `chrome://settings/cookies` en la política de cookies, que es intencionado.

La duplicación literal entre herramientas es baja. El trabajo de junio ya diferenció las secciones. El problema real es otro:

1. **Muy poco contenido editorial.** Cinco guías de 560-690 palabras frente a 11 herramientas. Para un revisor, el sitio es «11 utilidades y unos artículos cortos».
2. **Las guías están aisladas.** Cada guía recibe un solo enlace interno (desde `guias.html`). Ninguna herramienta enlaza a una guía. `guias.html` solo está en el footer.
3. **Sin señales de autoría en las guías.** No hay autor visible, ni fecha, ni forma de reportar errores. El JSON-LD tiene autor, pero la página no lo muestra.
4. **Bloques repetidos.** La pregunta «¿Se envían mis datos a algún servidor?» aparece en 9 herramientas con frases casi idénticas. También se repiten «¿Hay límite…?» y «¿Funciona en el móvil?».
5. **Afirmaciones falsas** sobre el funcionamiento de las herramientas (ver tabla). Un sitio que dice algo que su propia herramienta no hace transmite poco cuidado.
6. **FAQPage desalineado.** En 5 páginas el JSON-LD de FAQ no coincide con las preguntas visibles (contador-caracteres, eliminar-espacios, numero-a-letra, quitar-acentos, texto-aleatorio).
7. **Falta lo que diferencia una herramienta buena de una cualquiera:** ejemplos de entrada y salida y una sección honesta de limitaciones.

### Puntuación de las guías existentes (1-5)

| Guía | Profundidad | Ejemplos | Estructura | Enlaces a herramientas | Decisión |
|---|:-:|:-:|:-:|:-:|---|
| Mayúsculas en español | 3 | 3 | 4 | 1 | Ampliar a guía de referencia con casos (cargos, puntos cardinales, instituciones, internet…) |
| Tildes en mayúsculas | 3 | 3 | 4 | 1 | Ampliar (siglas, acrónimos, teclados, ejemplos de ambigüedad) |
| Mayúsculas en títulos | 3 | 4 | 4 | 1 | Ampliar (obras, publicaciones, subtítulos, web/SEO) |
| Límites de caracteres | 3 | 2 | 4 | 2 | Ampliar y corregir SMS; fecha de comprobación |
| Números: cifras o letras | 3 | 3 | 3 | 1 | Reescribir el párrafo confuso y ampliar |

## 4. Plan

1. Plantilla común de guía (generada por `scripts/build_guias.py`): migas de pan, autor enlazado a `sobre.html`, fechas, tiempo de lectura, resumen rápido, índice, artículos y herramientas relacionadas, enlace para reportar errores, JSON-LD `Article` + `BreadcrumbList`.
2. Ampliar las 5 guías a 1.200+ palabras y escribir 9 nuevas (14 en total), priorizando ordenar listas, texto de relleno y números en letra (las páginas con más tráfico).
3. Herramientas: corregir las afirmaciones falsas, añadir ejemplos reales y limitaciones, sustituir las FAQ repetidas por preguntas propias de cada herramienta, enlazar 2-3 guías y 2-3 herramientas con una frase que explique por qué. Regenerar el JSON-LD `FAQPage` desde las preguntas visibles.
4. Mejoras pequeñas de herramientas que el contenido necesita para ser honesto: orden natural de números en Ordenar lista, modo de expresiones regulares en Buscar y reemplazar, mayúscula tras `?` y `!` y tras signos de apertura en el convertidor, y corregir los decimales en Número a letras. Todas opcionales o retrocompatibles.
5. `guias.html` como índice temático. Enlace «Guías» en la cabecera de todas las páginas. Guías destacadas en la home.
6. `sobre.html`: cómo se hacen y revisan las guías, fuentes, cómo se prueban las herramientas, política de correcciones.
7. Sitemap, crawl local, validación de JSON-LD, prueba de las herramientas y comprobación a 375 px.
