# minusculasmayusculas.com

Eina online gratuïta per convertir text entre formats tipogràfics: majúscules, minúscules, capitalització per paraula i majúscules després de punt. Sense registre, sense servidor, sense cost.

**URL:** https://minusculasmayusculas.com

---

## Estructura del projecte

```
minusculasmayusculas.com/
├── index.html                  # Pàgina principal amb l'eina de conversió
├── converter.js                # Lògica de conversió de text (client-side)
├── tests.html                  # Tests manuals de les funcions de converter.js
├── aviso-legal.html            # Avís legal (LSSICE)
├── politica-privacidad.html    # Política de privacitat (RGPD)
├── politica-cookies.html       # Política de cookies
├── sitemap.xml                 # Sitemap per a cercadors
├── robots.txt                  # Directrius per a crawlers
└── .github/
    └── workflows/
        └── deploy.yml          # CI/CD: desplegament automàtic a Hetzner
```

---

## Funcionalitats

### Eina de conversió (`index.html` + `converter.js`)

Quatre modes de conversió, tots processats al navegador sense enviar dades a cap servidor:

| Botó | Funció | Exemple |
|------|--------|---------|
| Majúscules després de punt | Capitalitza l'inici de text i la primera lletra després de cada punt | `hola. com estàs` → `Hola. Com estàs` |
| tot minúscules | Converteix tot el text a minúscules | `HOLA MÓN` → `hola món` |
| TOT MAJÚSCULES | Converteix tot el text a majúscules | `hola món` → `HOLA MÓN` |
| Capitalitzar Cada Paraula | Primera lletra de cada paraula en majúscula | `hola món` → `Hola Món` |

Funcions addicionals:
- Comptador de caràcters i paraules en temps real
- Botó "Copiar text" amb feedback visual
- Botó "Netejar"
- Suport complet de caràcters espanyols (á, é, í, ó, ú, ñ, Á, É, Í, Ó, Ú, Ñ)

### Pàgines legals

Totes les pàgines legals estan en espanyol, segueixen el disseny de `index.html` (blau `#1a73e8`, font `system-ui`) i inclouen capçalera amb link a l'inici i peu de pàgina idèntic.

- **`aviso-legal.html`** — Identificació del titular (Siddharta Navarro Castellar, NIF 52917779T, Sant Climent de Llobregat), condicions d'ús, propietat intel·lectual, limitació de responsabilitat, jurisdicció Barcelona.
- **`politica-privacidad.html`** — Responsable del tractament, serveis de tercers (Google Analytics 4, Google AdSense), base jurídica (consentiment + interès legítim), drets RGPD (accés, rectificació, supressió, portabilitat, oposició, limitació), contacte AEPD.
- **`politica-cookies.html`** — Explicació de cookies, taula detallada de cookies usades (`_ga`, `_gid`, `IDE`, `test_cookie`), instruccions de gestió per Chrome/Firefox/Safari/Edge, menció al banner de consentiment granular.

### SEO

- **`sitemap.xml`** — Inclou totes les URLs públiques (`/`, `/aviso-legal.html`, `/politica-privacidad.html`, `/politica-cookies.html`) amb `lastmod`, `changefreq` i `priority`.
- **`robots.txt`** — Permet tots els crawlers (`User-agent: *`, `Allow: /`) i apunta al sitemap.

---

## Desplegament

El desplegament és automàtic via **GitHub Actions** cada vegada que es fa push a `main`.

**Flux:**
1. Push a `main` → s'activa el workflow `.github/workflows/deploy.yml`
2. Connexió SSH al servidor Hetzner
3. `git pull origin main` al directori `/var/www/minusculasmayusculas.com`

**Secrets de GitHub necessaris:**

| Secret | Descripció |
|--------|------------|
| `SSH_HOST` | IP o domini del servidor Hetzner |
| `SSH_USER` | Usuari SSH del servidor |
| `SSH_PRIVATE_KEY` | Clau privada SSH per autenticar-se |

No hi ha pas de build: el projecte és HTML/CSS/JS estàtic pur, no requereix compilació ni dependències.

---

## Desenvolupament local

```bash
git clone git@github.com:sidddi/minusculasmayusculas.git
cd minusculasmayusculas
# Obre index.html directament al navegador o usa un servidor local:
npx serve .
```

Per executar els tests manuals, obre `tests.html` al navegador.

---

## Tecnologies

- HTML5, CSS3, JavaScript (vanilla, sense dependències)
- Google Analytics 4 (analítica)
- Google AdSense (publicitat)
- GitHub Actions (CI/CD)
- Hetzner (servidor de producció)
