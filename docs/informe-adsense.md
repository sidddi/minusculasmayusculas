# Informe de trabajo: «Contenido de poco valor» en minusculasmayusculas.com

Fecha: 4 de octubre de 2026
Repositorio: `sidddi/minusculasmayusculas`
Rama: `adsense-content` (subida a GitHub, **sin fusionar con `main`, sin desplegar**)
Encargo original: el prompt «Arreglar "Contenido de poco valor" en minusculasmayusculas.com (AdSense)».

Este documento resume qué se hizo, cómo se verificó y qué queda pendiente. El detalle de la auditoría inicial está en `docs/auditoria-contenido.md`, en la misma rama.

---

## 1. Diagnóstico

La parte técnica y legal ya estaba bien: ads.txt, robots.txt, sitemap, canonicals, un solo h1 por página, JSON-LD válido, aviso legal, privacidad y cookies.

El problema era el contenido:

- **Poco contenido editorial.** 5 guías de 560-690 palabras frente a 11 herramientas.
- **Guías aisladas.** Cada guía recibía un solo enlace interno (desde `guias.html`). Ninguna herramienta enlazaba a una guía, y `guias.html` solo aparecía en el footer.
- **Sin autoría visible.** Las guías no mostraban autor, fechas ni forma de reportar errores.
- **Bloques repetidos.** La pregunta «¿Se envían mis datos a algún servidor?» aparecía en 9 herramientas con frases casi idénticas.
- **Afirmaciones falsas.** Varias páginas decían cosas que su propio código no hacía (ver apartado 3).
- **JSON-LD FAQPage desalineado** con las preguntas visibles en 5 páginas.

La duplicación literal entre herramientas era baja (0-7 %). El trabajo de junio ya había diferenciado las secciones.

---

## 2. Qué se ha hecho

### 2.1 Guías: 15 en total (10 nuevas, 5 ampliadas)

Cada guía tiene entre 1.228 y 1.811 palabras de cuerpo, más:

- autor enlazado a `sobre.html` y fechas de publicación y revisión visibles;
- resumen rápido de cuatro puntos e índice de contenidos;
- migas de pan (con `BreadcrumbList`) y JSON-LD `Article` con autor y fechas;
- bloque «Sigue leyendo» con 2-3 guías y 1-3 herramientas relacionadas;
- enlace «¿Has encontrado un error?» a contacto.

| Guía | URL | Estado |
|---|---|---|
| Cuándo se escribe con mayúscula en español (25 casos) | /guia-mayusculas-espanol.html | Ampliada |
| Errores de mayúsculas en correos, currículums y trabajos | /guia-errores-mayusculas.html | Nueva |
| Las mayúsculas también llevan tilde | /guia-tildes-mayusculas.html | Ampliada |
| Mayúsculas en títulos: español frente a inglés | /guia-mayusculas-titulos.html | Ampliada |
| ¿Números en cifras o en letras? | /guia-escribir-numeros.html | Ampliada |
| Cómo escribir cantidades en letra (20 ejemplos) | /guia-cantidades-en-letra.html | Nueva |
| Cómo convertir un número a letra a mano | /guia-numero-a-letra-a-mano.html | Nueva |
| Cómo ordenar una lista alfabéticamente en español | /guia-ordenar-alfabeticamente.html | Nueva |
| Cómo eliminar duplicados sin perder datos | /guia-eliminar-duplicados.html | Nueva |
| Cómo limpiar texto copiado de PDF, Word o web | /guia-limpiar-texto-copiado.html | Nueva |
| Buscar y reemplazar con expresiones regulares: 15 recetas | /guia-buscar-reemplazar-regex.html | Nueva |
| Quitar acentos: cuándo tiene sentido y cuándo no | /guia-quitar-acentos.html | Nueva |
| Texto de relleno: para qué sirve y cómo usarlo bien | /guia-texto-de-relleno.html | Nueva |
| Cómo se cuentan las palabras | /guia-contar-palabras.html | Nueva |
| Límites de caracteres y cómo recortar | /guia-limites-caracteres.html | Ampliada |

Temas del prompt que **no** se cubrieron como guía propia: Excel/Sheets frente a herramienta online (solo hay un apartado dentro de la guía de ordenar, porque no se pudieron verificar con fuentes oficiales los detalles de cada programa) y texto invertido (poco valor; se trata en la página de la herramienta).

Las guías se generan con `scripts/build_guias.py` a partir de los fragmentos de `scripts/guias/*.html`. El mismo script genera `guias.html`.

### 2.2 `guias.html`, navegación y home

- `guias.html` es ahora un índice con 5 temas (Mayúsculas y ortografía, Números, Listas y datos, Limpieza y edición de texto, Contar y medir), con resumen, fecha y tiempo de lectura de cada guía.
- Enlace «Guías» en la cabecera de todas las páginas, además del footer.
- La home enlaza 4 guías destacadas.
- Ninguna página huérfana: cada guía recibe al menos 3 enlaces internos.

### 2.3 Las 11 herramientas

En cada una:

- ejemplos reales de entrada y salida, generados con la propia herramienta;
- sección de limitaciones honesta, sacada de leer el código;
- FAQ propias: se sustituyeron las preguntas repetidas entre páginas (privacidad, «¿hay límite?», «¿funciona en el móvil?») por preguntas específicas;
- bloque de relacionados con 2-3 guías y 2-3 herramientas, cada una con una frase que explica por qué;
- JSON-LD `FAQPage` regenerado automáticamente a partir de las preguntas visibles.

Todas superan las 1.000 palabras de contenido (entre 1.036 y 1.402).

### 2.4 Mejoras pequeñas de herramientas

Se hicieron porque el contenido no podía ser exacto sin ellas. Son opcionales o no cambian el comportamiento por defecto:

- **Ordenar lista:** nueva casilla «Orden natural de números» (tema 2 antes que tema 10).
- **Buscar y reemplazar:** nueva casilla «Usar expresiones regulares» (`$1`, `\n`, `\t` en el reemplazo; aviso si el patrón no es válido). En el modo normal, el reemplazo es ahora literal: antes `$&` se interpretaba.
- **Convertidor (home):** «Mayúsculas después de punto» también actúa tras `?`, `!` y `…`, y salta los signos de apertura (`¿ ¡ «`). «Capitalizar Cada Palabra» también salta esos signos. Se actualizó `tests.html` en consecuencia.
- **Número a letras (bugs reales):** 2.500.000.000 daba «dos mil millones quinientos millones»; en femenino daba «doscientos mil personas»; y 1500,5 sin céntimos daba «coma cincuenta».
- **Texto aleatorio:** las frases interrogativas y exclamativas llevan ahora signo de apertura.

### 2.5 Señales de confianza

- `sobre.html`: nuevas secciones «Cómo se hacen las guías» (fuentes: Ortografía 2010, DPD, rae.es, FundéuRAE y documentación oficial de plataformas), «Cómo se prueban las herramientas» y «Errores y correcciones». **No se añadió ningún dato personal** que no estuviera ya en el sitio.
- Se quitó de `sobre.html` una frase no verificable («buena parte de las herramientas existen porque alguien las pidió»).

### 2.6 Otros

- `sitemap.xml` regenerado: 32 URLs.
- `llms.txt` y `README.md` actualizados.
- Open Graph básico añadido a las 3 páginas legales.
- Arreglados dos desbordamientos a 375 px que ya existían (email en contacto, tabla de cookies).
- `.github/workflows/deploy.yml`: añadido `rm -rf docs scripts` tras el `git pull`, para que la auditoría y el generador no se publiquen.

---

## 3. Afirmaciones falsas corregidas

| Página | Decía | Realidad (verificada en el código) |
|---|---|---|
| quitar-acentos | «ø se convierte en o» | ø, ł, ß, æ, œ y đ no cambian |
| contador-palabras | Los párrafos se separan por líneas en blanco | Cuenta cada línea con texto |
| contador-palabras | Coincide con Word «en la práctica totalidad de los casos» | Coincide en texto normal; difiere en casos límite |
| contador-caracteres, guía de límites | Las tildes o la ñ sacan un SMS de GSM-7 | La ñ, la é y la ü sí están en GSM-7; á, í, ó y ú no |
| ordenar-lista | Sin «Ignorar mayúsculas» van primero las mayúsculas (ASCII) | Van primero las minúsculas y se mantiene el orden español |
| ordenar-lista | Ordena cada idioma con sus reglas | Usa siempre las reglas del español |
| eliminar-duplicados | Un espacio al final crea un duplicado distinto | La herramienta ya ignora los espacios de los extremos |
| invertir-texto | «No hay riesgo» con caracteres especiales | Los emojis compuestos se rompen al invertir letras |
| texto-aleatorio | El lorem ipsum se usa «desde hace siglos» | No hay pruebas antes de Letraset (años sesenta) |
| numero-a-letra | Escribir en letra es «requisito legal» en facturas | Solo la Ley Cambiaria (cheques y letras de cambio) fija qué prevalece |

---

## 4. Verificación

- **Herramientas:** 43 pruebas automáticas en Chromium real (Playwright), 2-9 entradas por herramienta: 0 fallos, 0 errores de JavaScript.
- **`tests.html`:** 74 de 74 pruebas pasan.
- **Crawl local:** 0 enlaces rotos, 0 anclas rotas, 0 páginas huérfanas.
- **SEO técnico:** títulos y descripciones únicos en las 32 páginas, canonical autorreferente, `lang="es"`, un solo h1, sin noindex, sitemap XML válido.
- **JSON-LD:** todos los bloques son JSON válido; los FAQPage coinciden con las preguntas visibles.
- **Intacto:** `ads.txt` y `robots.txt` sin cambios (diff vacío). Los scripts de Cookiebot, AdSense y Analytics están idénticos en el `<head>` de las 32 páginas. No se añadieron bloques de anuncios.
- **Móvil:** a 375 px ninguna página tiene scroll horizontal y el menú desplegable queda dentro de la pantalla.
- **Privacidad:** se leyó el código de las 11 herramientas. Ninguna envía el texto a un servidor; la afirmación «se procesa en tu navegador» es cierta.
- **Duplicación:** tras los cambios, el texto repetido entre páginas se limita a la plantilla (menú, tarjetas de relacionados, aviso de errores).
- **Fuentes:** las normas citadas se contrastaron con páginas de rae.es, el BOE (Ley 19/1985) y la documentación de Google Search Central y X. Las URLs de rae.es se verificaron mediante búsqueda, porque el acceso directo estaba bloqueado desde el entorno de trabajo.

---

## 5. Pendiente para el propietario

1. **Revisar y fusionar** la rama `adsense-content` en `main`.
2. **Completar `sobre.html`** con información real que no se inventó: foto, trayectoria, por qué empezó el proyecto, desde cuándo existe.
3. **Abrir a mano** los enlaces a rae.es de las guías para confirmar que cargan.
4. **Límites sin fuente oficial:** Instagram (2.200 y 150), LinkedIn (220) y YouTube (100) no están documentados por las plataformas. En las guías no aparecen; en el contador de caracteres quedan marcados como orientativos.
5. **Opcional:** capturas o ilustraciones propias en 3-4 guías.

---

## 6. Despliegue y revisión de AdSense

1. Revisar en local: `python3 -m http.server` en la raíz y abrir `http://localhost:8000`.
2. Fusionar: `git checkout main && git merge adsense-content && git push origin main`.
3. El push a `main` dispara el despliegue automático a Hetzner (GitHub Actions).
4. En Search Console, reenviar el sitemap y pedir la indexación de `guias.html` y de algunas guías.
5. **Esperar unos días** a que Google rastree las páginas nuevas. Después, solicitar la revisión en AdSense.

No se ha tocado la cuenta de AdSense ni se ha solicitado ninguna revisión.

---

## 7. Commits de la rama

```
cc85954 chore: sobre.html con metodología, sitemap con 32 URLs, llms.txt, README y comprobaciones
ff7e1cb feat: contenido propio en las 11 herramientas
5e1c225 feat: enlace «Guías» en la cabecera y estilos comunes para ejemplos y relacionados
5fb83b0 fix: mejoras de herramientas que el contenido necesita para ser exacto
00c242f feat: plantilla común de guías, 10 guías nuevas y 5 ampliadas
c9cf094 docs: auditoría de contenido y plan para la revisión de AdSense
```

---

## 8. Riesgos que siguen abiertos

- **Fechas:** las 10 guías nuevas tienen la misma fecha de publicación. Conviene publicar las próximas espaciadas en el tiempo.
- **Autoría:** la señal de autor sigue siendo solo un nombre. Completar `sobre.html` es lo que más puede ayudar.
- **Antigüedad y tráfico:** el sitio es joven y tiene poco tráfico (84 clics en septiembre). Ningún cambio de contenido garantiza la aprobación; esta ronda elimina las causas evidentes de «poco valor».
