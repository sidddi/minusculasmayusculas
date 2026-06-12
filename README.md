# minusculasmayusculas.com

Suite de herramientas online gratuitas para trabajar con texto en español: conversión de mayúsculas/minúsculas, contadores, buscar y reemplazar, ordenar listas, eliminar duplicados, números a letras y más. Sin registro, sin servidor, sin coste. Incluye además una sección de guías de escritura.

**Herramientas:**
- https://minusculasmayusculas.com — Convertidor de mayúsculas y minúsculas
- https://minusculasmayusculas.com/contador-palabras.html — Contador de palabras
- https://minusculasmayusculas.com/contador-caracteres.html — Contador de caracteres
- https://minusculasmayusculas.com/buscar-reemplazar.html — Buscar y reemplazar texto
- https://minusculasmayusculas.com/ordenar-lista.html — Ordenar lista de palabras
- https://minusculasmayusculas.com/eliminar-duplicados.html — Eliminar líneas duplicadas
- https://minusculasmayusculas.com/numero-a-letra.html — Convertir números a letras
- https://minusculasmayusculas.com/invertir-texto.html — Invertir texto (letras, palabras o líneas)
- https://minusculasmayusculas.com/quitar-acentos.html — Quitar acentos
- https://minusculasmayusculas.com/eliminar-espacios.html — Eliminar espacios
- https://minusculasmayusculas.com/texto-aleatorio.html — Generador de texto aleatorio (lorem ipsum en español)

**Contenido editorial:**
- https://minusculasmayusculas.com/guias.html — Índice de guías de escritura
- 5 guías originales: mayúsculas en español, tildes en mayúsculas, mayúsculas en títulos, límites de caracteres y números en cifras o letras

**Páginas institucionales:** sobre.html (quién hace el sitio), contacto.html, aviso-legal.html, politica-privacidad.html, politica-cookies.html

---

## Estructura del proyecto

```
minusculasmayusculas.com/
├── index.html                  # Convertidor de mayúsculas y minúsculas
├── contador-palabras.html      # Contador de palabras, caracteres, frases y tiempo de lectura
├── contador-caracteres.html    # Contador de caracteres con/sin espacios, palabras y frases
├── buscar-reemplazar.html      # Buscar y reemplazar texto con opciones avanzadas
├── ordenar-lista.html          # Ordenar lista A-Z, Z-A, por longitud o aleatoriamente
├── eliminar-duplicados.html    # Eliminar líneas duplicadas de una lista
├── numero-a-letra.html         # Convertir números a su escritura en letras
├── invertir-texto.html         # Invertir texto por letras, palabras o líneas
├── quitar-acentos.html         # Quitar tildes y diéresis (opción de conservar ñ)
├── eliminar-espacios.html      # Limpiar espacios múltiples, tabulaciones y líneas vacías
├── texto-aleatorio.html        # Generador de texto de relleno en español
├── guias.html                  # Índice de guías de escritura
├── guia-mayusculas-espanol.html    # Guía: cuándo se escribe con mayúscula
├── guia-tildes-mayusculas.html     # Guía: las mayúsculas también llevan tilde
├── guia-mayusculas-titulos.html    # Guía: mayúsculas en títulos (español vs inglés)
├── guia-limites-caracteres.html    # Guía: límites de caracteres por plataforma
├── guia-escribir-numeros.html      # Guía: números en cifras o en letras
├── sobre.html                  # Sobre el proyecto (quién lo hace y principios)
├── contacto.html               # Página de contacto
├── converter.js                # Lógica de conversión de texto (client-side)
├── tests.html                  # Tests manuales de las funciones de converter.js
├── aviso-legal.html            # Aviso legal (LSSICE)
├── politica-privacidad.html    # Política de privacidad (RGPD)
├── politica-cookies.html       # Política de cookies
├── llms.txt                    # Descripción del sitio para IA (GEO: ChatGPT, Claude, Perplexity, Gemini)
├── ads.txt                     # Archivo de autorización de vendedores de AdSense
├── sitemap.xml                 # Sitemap para buscadores
├── robots.txt                  # Directrices para crawlers
└── .github/
    └── workflows/
        └── deploy.yml          # CI/CD: despliegue automático a Hetzner
```

---

## Contenido y AdSense

En junio de 2026, AdSense rechazó el sitio por «contenido de poco valor». Para resolverlo se aplicaron estos cambios (2026-06-12):

1. **Contenido único por herramienta.** Las 11 páginas de herramientas compartían la misma plantilla de secciones («Cómo funciona», «Casos de uso habituales», «Por qué usar esta herramienta», «Preguntas frecuentes»). Ahora cada página tiene títulos de sección propios, estructura distinta y una sección sustantiva específica (tablas de equivalencias, límites por plataforma, reglas de la RAE, ejemplos antes/después...).
2. **Páginas de confianza.** Se crearon `sobre.html` (quién mantiene el sitio y con qué principios) y `contacto.html` (email funcional), enlazadas desde el footer de todas las páginas.
3. **Sección de guías.** Cinco artículos originales de escritura en español (600–750 palabras de cuerpo cada uno) más su índice `guias.html`, enlazados desde el footer.
4. **Footer común** en todas las páginas: Sobre el proyecto | Contacto | Guías | Aviso legal | Política de privacidad | Cookies.

Pendiente (manual): comprobar indexación en Search Console y solicitar la revisión de AdSense marcando «Confirmo que he resuelto los problemas».

---

## Funcionalidades

### Contador de palabras (`contador-palabras.html`)

Analiza texto en tiempo real y muestra:

| Estadística | Descripción |
|-------------|-------------|
| Palabras | Número total de palabras |
| Caracteres (con espacios) | Longitud total del texto |
| Caracteres (sin espacios) | Longitud sin contar espacios |
| Frases | Bloques separados por `.`, `!` o `?` |
| Párrafos | Bloques separados por saltos de línea |
| Tiempo de lectura | Calculado a 200 palabras/minuto |

Funcionalidades adicionales: botón "Copiar texto", botón "Limpiar", soporte completo del español.

---

### Herramienta de conversión (`index.html` + `converter.js`)

Cuatro modos de conversión, todos procesados en el navegador sin enviar datos a ningún servidor:

| Botón | Función | Ejemplo |
|-------|---------|---------|
| Mayúsculas después de punto | Capitaliza el inicio del texto y la primera letra tras cada punto | `hola. cómo estás` → `Hola. Cómo estás` |
| todo minúsculas | Convierte todo el texto a minúsculas | `HOLA MUNDO` → `hola mundo` |
| TODO MAYÚSCULAS | Convierte todo el texto a mayúsculas | `hola mundo` → `HOLA MUNDO` |
| Capitalizar Cada Palabra | Primera letra de cada palabra en mayúscula | `hola mundo` → `Hola Mundo` |

Funcionalidades adicionales:
- Contador de caracteres y palabras en tiempo real
- Botón "Copiar texto" con feedback visual
- Botón "Limpiar"
- Soporte completo de caracteres del español (á, é, í, ó, ú, ñ, Á, É, Í, Ó, Ú, Ñ)

### Buscar y reemplazar (`buscar-reemplazar.html`)

Motor de búsqueda y sustitución de texto con las siguientes opciones:

| Opción | Descripción |
|--------|-------------|
| Distinguir mayúsculas/minúsculas | La búsqueda es case-sensitive cuando está activa |
| Solo palabra completa | Ignora coincidencias parciales dentro de palabras más largas |

Funcionalidades adicionales: contador de coincidencias en tiempo real, botón "Copiar texto", botón "Limpiar", soporte completo del español (á, é, í, ó, ú, ñ).

---

### Ordenar lista (`ordenar-lista.html`)

Ordena cualquier lista de texto (un elemento por línea) con cuatro modos:

| Modo | Descripción |
|------|-------------|
| A → Z | Orden alfabético ascendente (respeta ñ y acentos del español) |
| Z → A | Orden alfabético descendente |
| Por longitud | De la línea más corta a la más larga |
| Aleatorio | Baraja el orden aleatoriamente |

Opciones adicionales: eliminar duplicados, ignorar mayúsculas al ordenar, eliminar líneas vacías. Botón "Copiar texto" y "Limpiar".

---

### Páginas legales

Todas las páginas legales están en español, siguen el diseño de `index.html` (azul `#1a73e8`, fuente `system-ui`) e incluyen cabecera con enlace al inicio y pie de página idéntico.

- **`aviso-legal.html`** — Identificación del titular (Siddharta Navarro Castellar, NIF 52917779T, Sant Climent de Llobregat), condiciones de uso, propiedad intelectual, limitación de responsabilidad, jurisdicción Barcelona.
- **`politica-privacidad.html`** — Responsable del tratamiento, servicios de terceros (Google Analytics 4, Google AdSense), base jurídica (consentimiento + interés legítimo), derechos RGPD (acceso, rectificación, supresión, portabilidad, oposición, limitación), contacto AEPD.
- **`politica-cookies.html`** — Explicación de cookies, tabla detallada de cookies usadas (`_ga`, `_gid`, `IDE`, `test_cookie`), instrucciones de gestión por Chrome/Firefox/Safari/Edge, mención al banner de consentimiento granular.

### ads.txt

Archivo requerido por Google AdSense para autorizar a Google como vendedor directo de publicidad en el dominio. Debe estar accesible en `https://minusculasmayusculas.com/ads.txt`.

### SEO

- **`sitemap.xml`** — Incluye todas las URLs públicas (11 herramientas, 6 páginas de guías, sobre, contacto y 3 páginas legales) con `lastmod`, `changefreq` y `priority`.
- **`robots.txt`** — Permite todos los crawlers (`User-agent: *`, `Allow: /`) y apunta al sitemap.

---

## Despliegue

El despliegue es automático vía **GitHub Actions** cada vez que se hace push a `main`.

**Flujo:**
1. Push a `main` → se activa el workflow `.github/workflows/deploy.yml`
2. Conexión SSH al servidor Hetzner
3. `git pull origin main` en el directorio `/var/www/minusculasmayusculas.com`

**Secrets de GitHub necesarios:**

| Secret | Descripción |
|--------|-------------|
| `SSH_HOST` | IP o dominio del servidor Hetzner |
| `SSH_USER` | Usuario SSH del servidor |
| `SSH_PRIVATE_KEY` | Clave privada SSH para autenticarse |

No hay paso de build: el proyecto es HTML/CSS/JS estático puro, no requiere compilación ni dependencias.

---

## Desarrollo local

```bash
git clone git@github.com:sidddi/minusculasmayusculas.git
cd minusculasmayusculas
# Abre index.html directamente en el navegador o usa un servidor local:
npx serve .
```

Para ejecutar los tests manuales, abre `tests.html` en el navegador.

---

## Tecnologías

- HTML5, CSS3, JavaScript (vanilla, sin dependencias)
- Google Analytics 4 (analítica)
- Google AdSense (publicidad)
- Cookiebot CMP (gestión de consentimiento de cookies)
- GitHub Actions (CI/CD)
- Hetzner (servidor de producción)
