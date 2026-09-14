# E-mailhandtekening v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Acht e-mailhandtekeningen in Brandbook 2.1-stijl onder `v2/`, met de oude set bewaard onder `v1/`.

**Architecture:** Eén tabel-gebaseerde HTML-template met inline styles en `<!-- X: aanpassen! -->`-markers. Acht persoonlijke bestanden worden uit die template gegenereerd door één Python-script met een persoonstabel. Assets (logo, iconen) staan in de repo en worden via raw.githubusercontent.com geladen.

**Tech Stack:** HTML e-mailtabellen, Python 3 (generatie), Chrome headless of Playwright (iconen renderen en previews), git.

**Spec:** `docs/superpowers/specs/2026-09-14-signature-v2-design.md`

## Global Constraints

- Geen `<style>`-blok, geen flexbox, geen `rgba()`: alleen tabellen en inline styles.
- Inter nooit zwaarder dan 600. Font-stack `Inter, 'Avenir Next', Avenir, Helvetica, Arial, sans-serif`; mono `'JetBrains Mono', Menlo, 'Courier New', monospace`.
- Oranje `#F26522` uitsluitend in stat-suffixen. Geen randen, schaduw, gradient.
- Asset-URL's: `https://raw.githubusercontent.com/AI-Collega-s/email-signature/main/v2/assets/...`
- `icons/` in de root blijft staan; v1-bestanden verhuizen ongewijzigd.
- Commits zonder Feature ID: `<type>: <beschrijving>`, geen Co-Authored-By.
- Geen em-dashes in code, tekst of commits.

---

### Task 1: v1 archiveren

**Files:**
- Move: `aicollegas-signature-*.html` (9 bestanden) naar `v1/`

- [ ] **Step 1: Verplaats met git mv**

```bash
mkdir -p v1 && git mv aicollegas-signature-*.html v1/
```

- [ ] **Step 2: Verifieer**

Run: `ls v1 | wc -l && ls icons`
Expected: `9` en de vijf icon-PNG's staan nog in `icons/`.

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: verplaats handtekeningen v1 naar v1/"
```

### Task 2: Assets voor v2

**Files:**
- Create: `v2/assets/logo-dark.png` (2x, 44 px hoog)
- Create: `v2/assets/icons/icon_email.png`, `icon_phone.png`, `icon_globe.png`, `icon_linkedin.png` (28 x 28 px)
- Create: `v2/assets/icons/src/*.svg` (bron, 24-grid, stroke 1.8, ink, opacity .55)

**Produces:** de vier icon-bestandsnamen en `logo-dark.png`, exact zoals de template ze in Task 3 refereert.

- [ ] **Step 1: Schaal het logo**

```bash
mkdir -p v2/assets/icons/src
sips -Z 44 --resampleHeight 44 ../aicollegas-design-system/assets/png/logo-dark.png --out v2/assets/logo-dark.png
```
Controleer: `sips -g pixelHeight v2/assets/logo-dark.png` geeft 44.

- [ ] **Step 2: Schrijf de vier SVG's** (viewBox 0 0 24 24, `stroke="#0A0A0A" stroke-width="1.8" fill="none" opacity=".55"`, LinkedIn als fill). Paden gelijk aan die in `.superpowers/brainstorm/37673-1789397438/content/04-eindontwerp.html`.

- [ ] **Step 3: Render naar 28 px PNG** met Chrome headless, transparant:

```bash
for n in email phone globe linkedin; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
    --default-background-color=00000000 --window-size=28,28 --hide-scrollbars \
    --screenshot="v2/assets/icons/icon_$n.png" "file://$PWD/v2/assets/icons/src/$n.svg"
done
```
Controleer: elk bestand is 28 x 28 en heeft een transparante achtergrond (open met Read).

- [ ] **Step 4: Commit**

```bash
git add v2/assets && git commit -m "feat: voeg logo en iconen voor handtekening v2 toe"
```

### Task 3: Template

**Files:**
- Create: `v2/template.html`

**Produces:** markers `<!-- FOTO: src aanpassen! -->`, `<!-- NAAM & FUNCTIE: text aanpassen! -->`, `<!-- EMAIL LINK: href aanpassen! -->`, `<!-- EMAIL TEXT: text aanpassen! -->`, `<!-- LINKEDIN LINK: href aanpassen! -->`, `<!-- LINKEDIN TAG: text aanpassen! -->`, `<!-- TELEFOON LINK: href aanpassen! -->`, `<!-- TELEFOON TEXT: text aanpassen! -->`, elk gesloten met `<!-- END -->`. Task 4 vervangt de inhoud tussen deze markers.

- [ ] **Step 1: Schrijf de template** volgens de spec: buitenste tabel, persoonsblok (foto-td 64 px radius 16, rechts naam 16/600, functie mono 11 px `#9D9D9D`, contacttabel 2 x 2 met iconen 14 px en tekst 13 px `#676767`), ink-plate tabel max 520 px `background:#0A0A0A;border-radius:20px;padding:18px 20px` met logo `height=22`, tagline-rij (links 14/600 wit + 12 px `#919191`, rechts witte pill `Nu&nbsp;starten&nbsp;&rarr;` met `white-space:nowrap`), stats-rij 4 cellen (mono 20 px wit, suffix `<span style="color:#F26522">`, label 11 px `#858585`). Voorbeeldpersoon: Lars.

- [ ] **Step 2: Preview** in de visual companion: kopieer naar `.superpowers/brainstorm/37673-1789397438/content/05-template-check.html` gewikkeld in een `.mail`-achtergrond `#FAF7F2`. Vergelijk met scherm 04. Controleer specifiek: knop op één regel, geen 700-gewicht, logo scherp op 22 px.

- [ ] **Step 3: Commit**

```bash
git add v2/template.html && git commit -m "feat: voeg template voor handtekening v2 toe"
```

### Task 4: Acht persoonlijke handtekeningen

**Files:**
- Create: `v2/generate.py`
- Create: `v2/aaron.html`, `david.html`, `jacco.html`, `jasper.html`, `lars.html`, `maarten.html`, `max.html`, `niels.html`

**Consumes:** markers uit Task 3.

- [ ] **Step 1: Verzamel de persoonsdata** uit `v1/aicollegas-signature-<naam>.html`: foto-src, naam, functie, mailto, e-mailtekst, LinkedIn-href, LinkedIn-tag, tel-href, telefoontekst. Zet ze als lijst van dicts in `v2/generate.py`.

- [ ] **Step 2: Schrijf generate.py**: leest `template.html`, vervangt per marker-paar de regels tussen `<!-- X -->` en `<!-- END -->` via regex met de persoonswaarde, schrijft `v2/<naam>.html`. Draai: `python3 v2/generate.py`.

- [ ] **Step 3: Verifieer**

```bash
for f in v2/[a-z]*.html; do echo "$f: $(grep -c 'raw.githubusercontent.com/AI-Collega-s/email-signature/main/v2/assets' $f) asset-refs"; done
grep -l 'font-weight:700' v2/*.html || echo "geen 700"
grep -L 'Nu&nbsp;starten' v2/[a-z]*.html || echo "CTA overal"
```
Expected: elk bestand 5 asset-refs, "geen 700", "CTA overal". Naam en functie per bestand controleren tegen v1 met `grep -h 'font-size:16px' v2/*.html`.

- [ ] **Step 4: Previews**: render alle acht met Chrome headless op 640 px breed naar `.superpowers/brainstorm/37673-1789397438/content/preview-<naam>.png` en toon ze in één companion-scherm `06-alle-acht.html`. Bekijk elke PNG met Read.

- [ ] **Step 5: Commit**

```bash
git add v2 && git commit -m "feat: genereer acht handtekeningen in brandbook 2.1-stijl"
```

### Task 5: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Schrijf README**: wat v1 en v2 zijn, hoe je een handtekening installeert in Apple Mail, Gmail en Outlook (kopieer de gerenderde HTML uit de browser, plak in de handtekening-instellingen), hoe je een nieuwe persoon toevoegt (regel in `generate.py`, draaien, committen), en dat `icons/` in de root pas weg mag als iedereen op v2 zit.

- [ ] **Step 2: Commit en push**

```bash
git add README.md && git commit -m "docs: beschrijf v1 en v2 en installatie van de handtekening"
git push
```
Push is nodig: de asset-URL's werken pas als `main` op GitHub staat.

### Task 6: Handmatige controle in mailclient

- [ ] Lars plakt `v2/lars.html` in Apple Mail en Gmail-web en controleert: knop op één regel, iconen zichtbaar, logo scherp, geen rand om de foto.
