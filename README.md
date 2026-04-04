# minusculasmayusculas.com

Suite de herramientas online gratuitas para trabajar con texto: conversión de mayúsculas/minúsculas, contador de palabras y buscar y reemplazar. Sin registro, sin servidor, sin coste.

**URLs:**
- https://minusculasmayusculas.com — Convertidor de mayúsculas y minúsculas
- https://minusculasmayusculas.com/contador-palabras.html — Contador de palabras
- https://minusculasmayusculas.com/buscar-reemplazar.html — Buscar y reemplazar texto

---

## Estructura del proyecto

```
minusculasmayusculas.com/
├── index.html                  # Convertidor de mayúsculas y minúsculas
├── contador-palabras.html      # Contador de palabras, caracteres, frases y tiempo de lectura
├── buscar-reemplazar.html      # Buscar y reemplazar texto con opciones avanzadas
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

### Páginas legales

Todas las páginas legales están en español, siguen el diseño de `index.html` (azul `#1a73e8`, fuente `system-ui`) e incluyen cabecera con enlace al inicio y pie de página idéntico.

- **`aviso-legal.html`** — Identificación del titular (Siddharta Navarro Castellar, NIF 52917779T, Sant Climent de Llobregat), condiciones de uso, propiedad intelectual, limitación de responsabilidad, jurisdicción Barcelona.
- **`politica-privacidad.html`** — Responsable del tratamiento, servicios de terceros (Google Analytics 4, Google AdSense), base jurídica (consentimiento + interés legítimo), derechos RGPD (acceso, rectificación, supresión, portabilidad, oposición, limitación), contacto AEPD.
- **`politica-cookies.html`** — Explicación de cookies, tabla detallada de cookies usadas (`_ga`, `_gid`, `IDE`, `test_cookie`), instrucciones de gestión por Chrome/Firefox/Safari/Edge, mención al banner de consentimiento granular.

### ads.txt

Archivo requerido por Google AdSense para autorizar a Google como vendedor directo de publicidad en el dominio. Debe estar accesible en `https://minusculasmayusculas.com/ads.txt`.

### SEO

- **`sitemap.xml`** — Incluye todas las URLs públicas (`/`, `/contador-palabras.html`, `/buscar-reemplazar.html`, `/aviso-legal.html`, `/politica-privacidad.html`, `/politica-cookies.html`) con `lastmod`, `changefreq` y `priority`.
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
