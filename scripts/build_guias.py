#!/usr/bin/env python3
"""Genera las páginas de guías y el índice guias.html.

Uso (desde la raíz del repo):  python3 scripts/build_guias.py

El cuerpo de cada guía vive en scripts/guias/<slug>.html (solo el contenido del
artículo, con sus <h2>). Los metadatos están en GUIAS, más abajo. El script
añade cabecera, migas de pan, firma, fechas, resumen, índice, artículos
relacionados, footer y datos estructurados. Los .html generados se versionan:
el servidor no ejecuta ningún paso de build.
"""
import html
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, 'scripts')
BASE = 'https://minusculasmayusculas.com'
AUTOR = 'Siddharta Navarro Castellar'

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
         'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

CATEGORIAS = [
    ('mayusculas', 'Mayúsculas y ortografía',
     'Cuándo va mayúscula, por qué las mayúsculas llevan tilde y cómo se escriben los títulos en español.'),
    ('numeros', 'Números',
     'Cifras o letras, cantidades en documentos y el método para pasar un número a palabras sin equivocarte.'),
    ('listas', 'Listas y datos',
     'Ordenar alfabéticamente con criterio español y limpiar listas de repetidos sin perder información.'),
    ('limpieza', 'Limpieza y edición de texto',
     'Texto copiado de PDF o Word, sustituciones con patrones, acentos y texto de relleno.'),
    ('medir', 'Contar y medir',
     'Cómo se cuentan palabras y caracteres, y los límites de las plataformas donde escribes.'),
]

T = {  # herramientas: href -> nombre
    '/': 'Convertidor de mayúsculas y minúsculas',
    'contador-palabras.html': 'Contador de palabras',
    'contador-caracteres.html': 'Contador de caracteres',
    'buscar-reemplazar.html': 'Buscar y reemplazar',
    'ordenar-lista.html': 'Ordenar lista',
    'eliminar-duplicados.html': 'Eliminar duplicados',
    'numero-a-letra.html': 'Número a letras',
    'invertir-texto.html': 'Invertir texto',
    'quitar-acentos.html': 'Quitar acentos',
    'eliminar-espacios.html': 'Eliminar espacios',
    'texto-aleatorio.html': 'Texto aleatorio',
}

# Orden = orden dentro de cada categoría en guias.html
GUIAS = [
    # ── Mayúsculas y ortografía ──
    dict(
        slug='guia-mayusculas-espanol', cat='mayusculas',
        h1='Cuándo se escribe con mayúscula en español',
        title='Cuándo se escribe con mayúscula en español: 25 casos resueltos',
        desc='La regla general y 25 casos concretos con ejemplos: cargos, meses, puntos cardinales, instituciones, internet, después de dos puntos y más, según la RAE.',
        card='La regla general y 25 casos resueltos con ejemplos: cargos, meses, puntos cardinales, instituciones, internet y qué pasa después de los dos puntos.',
        published='2026-06-12', modified='2026-10-04',
        resumen=[
            'En español la minúscula es la norma. La mayúscula hay que justificarla.',
            'Van con mayúscula el inicio de enunciado, los nombres propios y las denominaciones oficiales de instituciones.',
            'Van con minúscula los días, los meses, las estaciones, los idiomas, los gentilicios, los cargos y los puntos cardinales.',
            'Si dudas con un texto lleno de mayúsculas, pásalo todo a minúscula y levanta solo lo que puedas justificar.',
        ],
        guias=['guia-tildes-mayusculas', 'guia-mayusculas-titulos', 'guia-errores-mayusculas'],
        tools=[('/', 'Para normalizar un texto entero a minúsculas y recuperar la mayúscula de cada oración.')],
    ),
    dict(
        slug='guia-errores-mayusculas', cat='mayusculas',
        h1='Errores de mayúsculas en correos, currículums y trabajos',
        title='Errores de mayúsculas en correos, currículums y trabajos académicos',
        desc='Los errores de mayúsculas más repetidos en correos formales, currículums y trabajos académicos, con la versión incorrecta, la correcta y el porqué.',
        card='Los fallos que más se repiten en correos formales, currículums y trabajos académicos, con la versión mala, la buena y el motivo.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'Los errores de mayúsculas se concentran en tres sitios: saludos y firmas, puestos y titulaciones, y títulos de trabajos.',
            'Cargos, profesiones, asignaturas genéricas y meses van en minúscula aunque parezcan importantes.',
            'Las titulaciones oficiales completas y los nombres de asignaturas concretas sí pueden ir con mayúscula.',
            'Un correo o un CV con mayúsculas de más parece traducido. Uno con mayúsculas de menos parece descuidado.',
        ],
        guias=['guia-mayusculas-espanol', 'guia-mayusculas-titulos', 'guia-tildes-mayusculas'],
        tools=[('/', 'Para arreglar de golpe un texto escrito con el bloqueo de mayúsculas puesto.'),
               ('buscar-reemplazar.html', 'Para corregir la misma mayúscula indebida en todo el documento a la vez.')],
    ),
    dict(
        slug='guia-tildes-mayusculas', cat='mayusculas',
        h1='Las mayúsculas también llevan tilde',
        title='Las mayúsculas también llevan tilde: la norma, el mito y cómo escribirlas',
        desc='La RAE es clara: las mayúsculas se acentúan. De dónde viene el mito, la excepción de las siglas, cómo escribir Á, É, Í, Ó, Ú en cada teclado y ejemplos de ambigüedad.',
        card='De dónde viene el mito de que las mayúsculas no se acentúan, la excepción de las siglas y cómo escribir Á, É, Í, Ó, Ú en cada teclado.',
        published='2026-06-12', modified='2026-10-04',
        resumen=[
            'Las mayúsculas llevan tilde siempre que la palabra la lleve. Nunca hubo una norma que dijera lo contrario.',
            'La única excepción son las siglas escritas enteras en mayúscula: CIA, no CÍA.',
            'La eñe y la diéresis también se mantienen: AÑO, PINGÜINO.',
            'Si el teclado se te resiste, escribe en minúscula con tildes y convierte el texto después.',
        ],
        guias=['guia-mayusculas-espanol', 'guia-quitar-acentos', 'guia-mayusculas-titulos'],
        tools=[('/', 'Convierte a mayúsculas conservando tildes, eñes y diéresis.')],
    ),
    dict(
        slug='guia-mayusculas-titulos', cat='mayusculas',
        h1='Mayúsculas en títulos: el estilo español frente al inglés',
        title='Mayúsculas en títulos: el estilo español frente al inglés',
        desc='En inglés los títulos capitalizan casi todas las palabras; en español, solo la primera y los nombres propios. Reglas, excepciones, publicaciones, subtítulos y títulos web.',
        card='Por qué «Cómo Ganar Amigos» es un calco del inglés, qué excepciones tiene el español y cómo titular webs, vídeos y trabajos.',
        published='2026-06-12', modified='2026-10-04',
        resumen=[
            'En español, un título lleva mayúscula en la primera palabra y en los nombres propios. Nada más.',
            'El «title case» (Cada Palabra En Mayúscula) es una convención del inglés.',
            'Excepción: los nombres de periódicos, revistas y colecciones sí llevan mayúscula en las palabras significativas.',
            'La regla no cambia en webs, vídeos ni presentaciones.',
        ],
        guias=['guia-mayusculas-espanol', 'guia-errores-mayusculas', 'guia-limites-caracteres'],
        tools=[('/', 'Pasa una lista de títulos en «title case» a minúsculas y recupera la mayúscula inicial.')],
    ),
    # ── Números ──
    dict(
        slug='guia-escribir-numeros', cat='numeros',
        h1='¿Números en cifras o en letras?',
        title='¿Números en cifras o en letras? Guía práctica con ejemplos',
        desc='Cuándo se escribe «veinte» y cuándo «20»: la recomendación de la RAE, los casos que van siempre en cifras, los ordinales y los errores más frecuentes.',
        card='Cuándo se escribe «veinte» y cuándo «20», qué casos van siempre en cifras, cómo se escriben los ordinales y los errores más comunes.',
        published='2026-06-12', modified='2026-10-04',
        resumen=[
            'En textos corrientes, letra para los números que se dicen en una palabra (tres, quince, cien) y cifra para los complejos (1.250).',
            'Siempre en cifra: fechas, horas en formato digital, decimales, medidas con símbolo, páginas y artículos de normas.',
            'Nada de mezclar a medias: «3.000» o «tres mil», nunca «3 mil». La excepción es millón y superiores: «3 millones».',
            'Los ordinales abreviados llevan punto: 1.º, 2.ª, 3.er.',
        ],
        guias=['guia-cantidades-en-letra', 'guia-numero-a-letra-a-mano', 'guia-limites-caracteres'],
        tools=[('numero-a-letra.html', 'Escribe en letras cualquier número hasta 999 999 999 999.')],
    ),
    dict(
        slug='guia-cantidades-en-letra', cat='numeros',
        h1='Cómo escribir cantidades en letra en cheques, contratos y facturas',
        title='Cómo escribir cantidades en letra: cheques, contratos y facturas (20 ejemplos)',
        desc='Cómo se escriben en letra los importes en documentos: euros y céntimos, veintiún o veintiuna, cien o ciento, millones, y 20 ejemplos resueltos.',
        card='Euros y céntimos, «veintiún» o «veintiuna», «cien» o «ciento», millones y 20 importes resueltos, listos para copiar.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'En un documento, el importe va dos veces: en cifra y en letra. Así se evita que alguien altere la cifra.',
            '«Uno» se acorta ante el sustantivo masculino: veintiún euros, treinta y un euros, un millón de euros.',
            'Las centenas concuerdan con el sustantivo femenino: doscientas libras, quinientas acciones.',
            'Los céntimos se escriben aparte: «mil doscientos euros con cincuenta céntimos».',
        ],
        guias=['guia-numero-a-letra-a-mano', 'guia-escribir-numeros', 'guia-errores-mayusculas'],
        tools=[('numero-a-letra.html', 'Para obtener el importe en letra con céntimos y en mayúsculas, como lo piden muchos formularios.')],
    ),
    dict(
        slug='guia-numero-a-letra-a-mano', cat='numeros',
        h1='Cómo convertir un número a letra a mano, paso a paso',
        title='Cómo convertir un número a letra a mano: método paso a paso',
        desc='Un método en cuatro pasos para escribir cualquier número en letras sin equivocarte, con los casos difíciles: 21, 100 y 101, 1.000, 1.001 y 1.000.000.',
        card='Un método en cuatro pasos para escribir cualquier número en palabras, con los casos que más fallan: 21, 100 y 101, 1.001, 1.000.000.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'Parte el número en grupos de tres cifras desde la derecha y escribe cada grupo por separado.',
            'Del 16 al 29 se escribe en una sola palabra. Del 31 en adelante, con «y».',
            '«Mil» no lleva «un» delante. «Millón» sí: un millón, dos millones.',
            'Cuando hayas terminado, léelo en voz alta y comprueba que suena al número original.',
        ],
        guias=['guia-cantidades-en-letra', 'guia-escribir-numeros', 'guia-ordenar-alfabeticamente'],
        tools=[('numero-a-letra.html', 'Para comprobar el resultado que has escrito a mano.')],
    ),
    # ── Listas y datos ──
    dict(
        slug='guia-ordenar-alfabeticamente', cat='listas',
        h1='Cómo ordenar una lista alfabéticamente en español',
        title='Cómo ordenar una lista alfabéticamente en español: ñ, tildes y números',
        desc='Las reglas del orden alfabético en español: la ñ, la ch y la ll, las tildes, las mayúsculas, los números y el orden natural. Con ejemplos en texto, hojas de cálculo y código.',
        card='La ñ, la ch y la ll, las tildes, las mayúsculas y los números: qué dice la norma y por qué los programas fallan.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'La ñ va entre la n y la o. La ch y la ll no tienen lugar propio desde 1994: van dentro de la c y de la l.',
            'Las tildes y las mayúsculas no cambian el orden. «Ávila» va junto a «avión».',
            'Los programas que ordenan por código de carácter mandan «Ávila» detrás de la z. Es el error más frecuente.',
            'Para listas con números («tema 2», «tema 10») necesitas orden natural, no alfabético.',
        ],
        guias=['guia-eliminar-duplicados', 'guia-limpiar-texto-copiado', 'guia-quitar-acentos'],
        tools=[('ordenar-lista.html', 'Ordena con el criterio español y ofrece orden natural para números.'),
               ('eliminar-duplicados.html', 'Para quitar los repetidos antes de ordenar.'),
               ('eliminar-espacios.html', 'Los espacios al inicio de línea alteran el orden: quítalos antes.')],
    ),
    dict(
        slug='guia-eliminar-duplicados', cat='listas',
        h1='Cómo eliminar duplicados de una lista sin perder datos',
        title='Cómo eliminar duplicados de una lista: mayúsculas, tildes y espacios invisibles',
        desc='Por qué dos líneas que parecen iguales no lo son, cómo tratar mayúsculas, tildes y espacios, y casos reales: listas de correos, nombres e inventarios.',
        card='Por qué dos líneas que parecen iguales no lo son: mayúsculas, tildes y espacios invisibles. Con casos de correos, nombres e inventarios.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'Antes de quitar duplicados, decide qué significa «igual» en tu lista: con o sin mayúsculas, con o sin tildes.',
            'Los duplicados que no se van suelen ser espacios invisibles al final de la línea.',
            'En correos electrónicos, ignora mayúsculas. En códigos de producto, normalmente no.',
            'Guarda siempre la lista original. Una deduplicación mal planteada borra datos que no eran repetidos.',
        ],
        guias=['guia-ordenar-alfabeticamente', 'guia-limpiar-texto-copiado', 'guia-quitar-acentos'],
        tools=[('eliminar-duplicados.html', 'Quita líneas repetidas conservando el orden original.'),
               ('eliminar-espacios.html', 'Limpia espacios invisibles que crean duplicados fantasma.'),
               ('quitar-acentos.html', 'Para comparar nombres escritos con y sin tilde.')],
    ),
    # ── Limpieza y edición ──
    dict(
        slug='guia-limpiar-texto-copiado', cat='limpieza',
        h1='Cómo limpiar texto copiado de un PDF, Word o una web',
        title='Cómo limpiar texto copiado de PDF, Word o una web: saltos, espacios y comillas',
        desc='Saltos de línea a mitad de frase, espacios dobles, espacios de no separación, guiones de corte y comillas raras: de dónde salen y un flujo para limpiarlos.',
        card='Saltos de línea a mitad de frase, espacios de no separación, guiones de corte y comillas mezcladas: de dónde salen y cómo quitarlos.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'Un PDF guarda líneas, no párrafos. Por eso al copiar aparecen saltos a mitad de frase.',
            'Limpia en este orden: espacios especiales, saltos de línea, espacios dobles, guiones de corte y, al final, comillas.',
            'Conserva los saltos de párrafo antes de unir líneas, o perderás la estructura.',
            'Revisa siempre a mano los guiones: «bien-estar» y «franco-alemán» no se arreglan igual.',
        ],
        guias=['guia-buscar-reemplazar-regex', 'guia-eliminar-duplicados', 'guia-contar-palabras'],
        tools=[('eliminar-espacios.html', 'Une líneas partidas y reduce espacios múltiples.'),
               ('buscar-reemplazar.html', 'Para los arreglos con patrón: guiones de corte, comillas, saltos.'),
               ('contador-palabras.html', 'Para comprobar que no has perdido texto por el camino.')],
    ),
    dict(
        slug='guia-buscar-reemplazar-regex', cat='limpieza',
        h1='Buscar y reemplazar con expresiones regulares: 15 recetas',
        title='Buscar y reemplazar con expresiones regulares: 15 recetas con antes y después',
        desc='Lo mínimo de expresiones regulares para editar texto y 15 recetas probadas: espacios dobles, fechas, saltos de línea, comillas, números, correos y más.',
        card='Lo mínimo que necesitas saber de expresiones regulares y 15 recetas probadas con su antes y después.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'Una expresión regular describe un patrón: «cualquier número de cuatro cifras», «dos espacios o más».',
            'Con diez símbolos cubres casi todo: <code>.</code>, <code>\\d</code>, <code>\\s</code>, <code>+</code>, <code>*</code>, <code>?</code>, <code>[ ]</code>, <code>( )</code>, <code>^</code> y <code>$</code>.',
            'Los paréntesis capturan, y en el reemplazo recuperas lo capturado con <code>$1</code>, <code>$2</code>…',
            'Prueba primero con la búsqueda y mira el número de coincidencias antes de reemplazar.',
        ],
        guias=['guia-limpiar-texto-copiado', 'guia-eliminar-duplicados', 'guia-contar-palabras'],
        tools=[('buscar-reemplazar.html', 'Tiene un modo de expresiones regulares para probar estas recetas.'),
               ('eliminar-espacios.html', 'Si solo necesitas quitar espacios, sin escribir patrones.')],
    ),
    dict(
        slug='guia-quitar-acentos', cat='limpieza',
        h1='Quitar acentos: cuándo tiene sentido y cuándo es un error',
        title='Quitar acentos: cuándo es correcto (URLs, archivos, datos) y cuándo no',
        desc='Cuándo conviene quitar tildes (URLs, nombres de archivo, búsquedas, bases de datos) y cuándo cambia el significado: sábana y sabana, papá y papa.',
        card='URLs, nombres de archivo, búsquedas y bases de datos: dónde sí quitar tildes y por qué nunca en un texto para personas.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'Quitar acentos es una operación técnica para máquinas, no una forma de escribir.',
            'Tiene sentido en URLs, nombres de archivo, identificadores y comparaciones de datos.',
            'En un texto que va a leer una persona, la tilde distingue palabras: sábana y sabana, papá y papa.',
            'Decide qué hacer con la ñ antes de empezar. No es un acento: es otra letra.',
        ],
        guias=['guia-tildes-mayusculas', 'guia-eliminar-duplicados', 'guia-limites-caracteres'],
        tools=[('quitar-acentos.html', 'Quita tildes y diéresis, con opción de conservar la ñ.'),
               ('eliminar-duplicados.html', 'Para cruzar listas una vez normalizadas.')],
    ),
    dict(
        slug='guia-texto-de-relleno', cat='limpieza',
        h1='Texto de relleno: para qué sirve y cómo usarlo bien',
        title='Texto de relleno y lorem ipsum: para qué sirve y cómo usarlo bien',
        desc='Para qué sirve el texto aleatorio de prueba en maquetas, software y plantillas, alternativas al lorem ipsum y cómo evitar que acabe publicado.',
        card='Para qué sirve en maquetas, pruebas de software y plantillas, qué alternativas hay al lorem ipsum y cómo evitar que acabe publicado.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'El texto de relleno sirve para juzgar la forma sin distraerte con el contenido.',
            'El lorem ipsum viene de un texto de Cicerón deformado. En español, un relleno en castellano mide mejor la maqueta.',
            'Prueba siempre con más texto del previsto y con casos extremos: palabras largas, títulos de dos líneas, campos vacíos.',
            'Marca el relleno para poder encontrarlo antes de publicar.',
        ],
        guias=['guia-limites-caracteres', 'guia-contar-palabras', 'guia-mayusculas-titulos'],
        tools=[('texto-aleatorio.html', 'Genera palabras, frases o párrafos de relleno en español.'),
               ('contador-palabras.html', 'Para saber cuánto texto real cabrá en el hueco.')],
    ),
    # ── Contar y medir ──
    dict(
        slug='guia-contar-palabras', cat='medir',
        h1='Cómo se cuentan las palabras: por qué cada programa da una cifra',
        title='Cómo se cuentan las palabras: Word, Google Docs y contadores online',
        desc='Por qué Word, Google Docs y un contador online pueden dar cifras distintas: guiones, números, URLs, signos sueltos. Para qué sirve contar palabras y cómo hacerlo bien.',
        card='Guiones, números, URLs y signos sueltos: por qué dos programas dan cifras distintas y qué recuento usar en cada caso.',
        published='2026-10-04', modified='2026-10-04',
        resumen=[
            'No hay una definición universal de «palabra». Cada programa aplica la suya.',
            'Las diferencias salen de los casos límite: guiones, rayas, números, URLs, siglas con puntos.',
            'Si alguien te pide un número de palabras, usa el contador que use esa persona.',
            'Para límites de plataforma, cuenta caracteres, no palabras.',
        ],
        guias=['guia-limites-caracteres', 'guia-limpiar-texto-copiado', 'guia-texto-de-relleno'],
        tools=[('contador-palabras.html', 'Palabras, frases, párrafos y tiempo de lectura en tiempo real.'),
               ('contador-caracteres.html', 'Para límites que se miden en caracteres.')],
    ),
    dict(
        slug='guia-limites-caracteres', cat='medir',
        h1='Escribir corto: límites de caracteres y cómo aprovecharlos',
        title='Límites de caracteres en X, SMS, Google y redes: qué cuenta y cómo recortar',
        desc='Los límites de X, SMS, títulos y meta descriptions de Google y otras plataformas, qué cuenta como carácter (tildes en SMS, URLs, emojis) y técnicas para recortar.',
        card='Los límites de las plataformas más usadas, qué cuenta exactamente como carácter y técnicas concretas para recortar sin perder el mensaje.',
        published='2026-06-12', modified='2026-10-04',
        resumen=[
            'Hay límites duros (no te dejan pasar) y límites de truncado (se corta lo que se ve).',
            'En X, cada enlace cuenta 23 caracteres y la mayoría de emojis cuentan 2.',
            'En un SMS, una sola á, í, ó o ú baja el límite de 160 a 70 caracteres. La ñ y la é no.',
            'Pon lo importante al principio. Así sobrevive a cualquier truncado.',
        ],
        guias=['guia-contar-palabras', 'guia-quitar-acentos', 'guia-escribir-numeros'],
        tools=[('contador-caracteres.html', 'Muestra el recuento frente a los límites de X, SMS, meta description e Instagram.'),
               ('quitar-acentos.html', 'Para dejar un SMS dentro del juego de caracteres básico.')],
    ),
]

BY_SLUG = {g['slug']: g for g in GUIAS}


def fecha_larga(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} de {MESES[int(m) - 1]} de {y}'


def slugify(text):
    text = re.sub(r'<[^>]+>', '', text).lower()
    for a, b in zip('áéíóúüñ', 'aeiouun'):
        text = text.replace(a, b)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60].rstrip('-')


def palabras(fragment):
    txt = re.sub(r'<[^>]+>', ' ', fragment)
    txt = html.unescape(txt)
    return len(re.findall(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", txt))


def leer(nombre):
    with open(os.path.join(HERE, nombre), encoding='utf-8') as f:
        return f.read()


HEAD_SCRIPTS = '''  <script id="Cookiebot" src="https://consent.cookiebot.com/uc.js" data-cbid="82f67e93-af6b-4ca1-9a41-38ddc2bcd654" data-blockingmode="auto" type="text/javascript"></script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1180780703286273" crossorigin="anonymous"></script>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-S2CEDDK0K4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-S2CEDDK0K4');
  </script>'''

TOOLS_MENU = '''        <div class="nav-right">
          <a class="nav-link" href="guias.html">Guías</a>
          <div class="tools-menu">
            <button class="tools-btn" id="tools-btn" aria-haspopup="true" aria-expanded="false">
              Herramientas <span class="caret">&#9662;</span>
            </button>
            <nav class="tools-dropdown" id="tools-dropdown" aria-label="Herramientas">
              <a href="/">Mayúsculas y Minúsculas</a>
              <a href="contador-palabras.html">Contador de Palabras</a>
              <a href="contador-caracteres.html">Contador de Caracteres</a>
              <a href="buscar-reemplazar.html">Buscar y Reemplazar</a>
              <a href="ordenar-lista.html">Ordenar Lista</a>
              <a href="eliminar-duplicados.html">Eliminar Duplicados</a>
              <a href="numero-a-letra.html">Número a Letras</a>
              <a href="invertir-texto.html">Invertir Texto</a>
              <a href="quitar-acentos.html">Quitar Acentos</a>
              <a href="eliminar-espacios.html">Eliminar Espacios</a>
              <a href="texto-aleatorio.html">Texto Aleatorio</a>
            </nav>
          </div>
        </div>'''

MENU_JS = '''  <script>
    (function() {
      var btn = document.getElementById('tools-btn');
      var menu = document.getElementById('tools-dropdown');
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        var open = menu.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      document.addEventListener('click', function(e) {
        if (menu.classList.contains('open') && !menu.contains(e.target)) {
          menu.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
        }
      });
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          menu.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
        }
      });
    })();
  </script>'''

FOOTER = '''  <footer>
    <div class="container">
      <p>© 2026 minusculasmayusculas.com</p>
      <nav aria-label="Pie de página">
        <a href="sobre.html">Sobre el proyecto</a>
        <span class="sep">|</span>
        <a href="contacto.html">Contacto</a>
        <span class="sep">|</span>
        <a href="guias.html">Guías</a>
        <span class="sep">|</span>
        <a href="aviso-legal.html">Aviso legal</a>
        <span class="sep">|</span>
        <a href="politica-privacidad.html">Política de privacidad</a>
        <span class="sep">|</span>
        <a href="politica-cookies.html">Cookies</a>
      </nav>
    </div>
  </footer>'''


def e(s):
    return html.escape(s, quote=True)


def ld(obj):
    return ('  <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + '\n  </script>')


def pagina(title, desc, url, og_type, css, ld_blocks, header_inner, main_inner):
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
{HEAD_SCRIPTS}
  <meta charset="UTF-8" />
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:locale" content="es_ES" />
  <meta property="og:site_name" content="minusculasmayusculas.com" />
  <meta property="og:image" content="{BASE}/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Minúsculas y Mayúsculas: herramientas de texto online gratuitas" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(desc)}" />
  <meta name="twitter:image" content="{BASE}/og-image.png" />

  <style>{css}  </style>
  <!-- Structured data (Schema.org) -->
{chr(10).join(ld_blocks)}
</head>
<body>

  <header>
    <div class="container">
      <div class="header-bar">
        <a class="brand" href="/">minusculas<strong>mayusculas</strong>.com</a>
{TOOLS_MENU}
      </div>
{header_inner}
    </div>
  </header>
{MENU_JS}

  <main>
    <div class="container">
{main_inner}
    </div><!-- /container -->
  </main>

{FOOTER}

</body>
</html>
'''


def construir_guia(g, css):
    cuerpo = leer(f"guias/{g['slug']}.html").strip()
    # ids en los h2 para el índice
    toc = []

    def add_id(m):
        attrs, inner = m.group(1), m.group(2)
        if 'id=' in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            hid = slugify(inner)
            attrs = f' id="{hid}"' + attrs
        toc.append((hid, re.sub(r'<[^>]+>', '', inner)))
        return f'<h2{attrs}>{inner}</h2>'
    cuerpo = re.sub(r'<h2([^>]*)>(.*?)</h2>', add_id, cuerpo, flags=re.S)

    n = palabras(cuerpo) + sum(palabras(x) for x in g['resumen'])
    minutos = max(1, math.ceil(n / 200))
    g['palabras'] = n
    g['minutos'] = minutos
    url = f"{BASE}/{g['slug']}.html"

    actualizado = ''
    if g['modified'] != g['published']:
        actualizado = f' · Actualizado el <time datetime="{g["modified"]}">{fecha_larga(g["modified"])}</time>'

    resumen = '\n'.join(f'            <li>{x}</li>' for x in g['resumen'])
    indice = ''
    if len(toc) >= 4:
        items = '\n'.join(f'            <li><a href="#{h}">{t}</a></li>' for h, t in toc)
        indice = f'''        <nav class="toc" aria-label="Índice del artículo">
          <h2>En esta guía</h2>
          <ol>
{items}
          </ol>
        </nav>
'''

    rel = []
    for s in g['guias']:
        r = BY_SLUG[s]
        rel.append(f'''            <li><a href="{s}.html">{r['h1']}</a><span>{r['card']}</span></li>''')
    for href, motivo in g['tools']:
        rel.append(f'''            <li><a href="{href}">{T[href]}</a><span>{motivo}</span></li>''')

    header_inner = f'''      <nav class="breadcrumbs" aria-label="Migas de pan">
        <ol>
          <li><a href="/">Inicio</a></li>
          <li><a href="guias.html">Guías</a></li>
          <li aria-current="page">{g['h1']}</li>
        </ol>
      </nav>
      <h1>{g['h1']}</h1>'''

    main_inner = f'''      <article class="article">
        <p class="byline">
          Por <a href="sobre.html" rel="author">{AUTOR}</a> ·
          Publicado el <time datetime="{g['published']}">{fecha_larga(g['published'])}</time>{actualizado} ·
          Lectura: {minutos} min
        </p>

        <aside class="resumen" aria-label="Resumen rápido">
          <h2>Resumen rápido</h2>
          <ul>
{resumen}
          </ul>
        </aside>

{indice}
{cuerpo}

        <section class="related" aria-label="Artículos y herramientas relacionadas">
          <h2>Sigue leyendo</h2>
          <ul>
{chr(10).join(rel)}
          </ul>
        </section>

        <p class="report">
          ¿Has encontrado un error o una explicación que no se entiende?
          <a href="contacto.html">Escríbeme</a> y lo corrijo. Las guías se revisan
          con las obras de la RAE y la FundéuRAE como referencia; puedes leer cómo se
          preparan en <a href="sobre.html#como-se-hacen-las-guias">Sobre el proyecto</a>.
        </p>
      </article>'''

    ld_blocks = [
        ld({
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': g['h1'],
            'description': g['desc'],
            'url': url,
            'inLanguage': 'es',
            'datePublished': g['published'],
            'dateModified': g['modified'],
            'wordCount': n,
            'image': f'{BASE}/og-image.png',
            'author': {'@type': 'Person', 'name': AUTOR, 'url': f'{BASE}/sobre.html'},
            'publisher': {'@type': 'Person', 'name': AUTOR, 'url': f'{BASE}/sobre.html'},
            'mainEntityOfPage': url,
        }),
        ld({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Guías', 'item': f'{BASE}/guias.html'},
                {'@type': 'ListItem', 'position': 3, 'name': g['h1'], 'item': url},
            ],
        }),
    ]
    out = pagina(g['title'], g['desc'], url, 'article', css, ld_blocks, header_inner, main_inner)
    with open(os.path.join(ROOT, g['slug'] + '.html'), 'w', encoding='utf-8') as f:
        f.write(out)


def construir_indice(css):
    url = f'{BASE}/guias.html'
    grupos = []
    for cid, nombre, intro in CATEGORIAS:
        items = []
        for g in GUIAS:
            if g['cat'] != cid:
                continue
            items.append(f'''            <li>
              <h3><a href="{g['slug']}.html">{g['h1']}</a></h3>
              <p>{g['card']}</p>
              <span class="guide-meta">Actualizada el <time datetime="{g['modified']}">{fecha_larga(g['modified'])}</time> · {g['minutos']} min de lectura</span>
            </li>''')
        grupos.append(f'''        <section class="guide-group" aria-labelledby="cat-{cid}">
          <h2 id="cat-{cid}">{nombre}</h2>
          <p>{intro}</p>
          <ul class="guide-list">
{chr(10).join(items)}
          </ul>
        </section>''')

    header_inner = '''      <nav class="breadcrumbs" aria-label="Migas de pan">
        <ol>
          <li><a href="/">Inicio</a></li>
          <li aria-current="page">Guías</li>
        </ol>
      </nav>
      <h1>Guías de escritura y edición de texto</h1>'''

    main_inner = f'''      <div class="article">
        <p>
          Las herramientas de este sitio hacen la parte mecánica: convertir, contar,
          ordenar, limpiar. Estas guías explican la parte de criterio. Cuándo va
          mayúscula. Cómo se ordena una lista en español. Por qué tu lista sigue teniendo
          duplicados. Cómo se escribe un importe en un contrato.
        </p>
        <p>
          Cada guía empieza con un resumen de cuatro líneas, por si solo necesitas la
          respuesta, y sigue con ejemplos reales y errores frecuentes, por si quieres
          entenderla. Las normas ortográficas se contrastan con las obras de la RAE.
          Las escribe y revisa {AUTOR}; puedes leer
          <a href="sobre.html#como-se-hacen-las-guias">cómo se preparan</a>.
        </p>
{chr(10).join(grupos)}
      </div>'''

    ld_blocks = [
        ld({
            '@context': 'https://schema.org',
            '@type': 'CollectionPage',
            'name': 'Guías de escritura y edición de texto',
            'description': 'Guías prácticas sobre mayúsculas, tildes, números, listas, limpieza de texto y límites de caracteres en español.',
            'url': url,
            'inLanguage': 'es',
            'author': {'@type': 'Person', 'name': AUTOR, 'url': f'{BASE}/sobre.html'},
            'hasPart': [{'@type': 'Article', 'headline': g['h1'], 'url': f"{BASE}/{g['slug']}.html"} for g in GUIAS],
        }),
        ld({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Guías', 'item': url},
            ],
        }),
    ]
    out = pagina('Guías de escritura y edición de texto en español | Minúsculas y Mayúsculas',
                 'Guías prácticas con ejemplos sobre mayúsculas, tildes, números en letra, ordenar listas, eliminar duplicados, limpiar texto y límites de caracteres.',
                 url, 'website', css, ld_blocks, header_inner, main_inner)
    with open(os.path.join(ROOT, 'guias.html'), 'w', encoding='utf-8') as f:
        f.write(out)


def main():
    css = leer('guia-base.css').rstrip() + '\n' + leer('guia-extra.css')
    for g in GUIAS:
        construir_guia(g, css)
    construir_indice(css)
    for g in GUIAS:
        print(f"{g['slug']:32} {g['palabras']:5} palabras  {g['minutos']} min")


if __name__ == '__main__':
    main()
