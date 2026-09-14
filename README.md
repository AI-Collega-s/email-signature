# E-mailhandtekeningen AI Collega's

Twee versies naast elkaar:

- `v2/` De huidige handtekening in Brandbook 2.1-stijl (sinds september 2026). Gebruik deze.
- `v1/` De oude handtekening (april 2026). Alleen als archief; `icons/` in de root hoort bij v1 en blijft staan zolang collega's die versie nog in hun mailclient hebben.

Ontwerp en keuzes: `docs/superpowers/specs/2026-09-14-signature-v2-design.md`.

## Installeren

1. Open `v2/<jouw-naam>.html` in een browser. Het snelst: open het bestand op GitHub, klik "Raw", en open die URL.
2. Selecteer alles (Cmd+A) en kopieer (Cmd+C).
3. Plak in de handtekening-instellingen van je mailclient:
   - **Apple Mail**: Instellingen, Handtekeningen, nieuwe handtekening, plakken. Zet "Kies altijd mijn standaardlettertype" uit.
   - **Gmail (web)**: Instellingen, Alle instellingen, Handtekening, nieuwe handtekening, plakken.
   - **Outlook (Mac/web)**: Instellingen, Handtekeningen, nieuwe handtekening, plakken. Outlook kent Inter en JetBrains Mono niet en valt terug op Helvetica en Menlo, dat is bedoeld.
4. Stuur jezelf een testmail en controleer dat de knop "Nu starten" op één regel staat en de iconen zichtbaar zijn.

De afbeeldingen (zwarte kaart, iconen) worden geladen van `raw.githubusercontent.com` uit deze repo. De zwarte kaart is bewust één afbeelding: mailclients in dark mode (Apple Mail voorop) keren alle kleuren om, maar laten afbeeldingen staan. Zo blijft de kaart in elk thema zwart met wit logo. De profielfoto komt van Slack: verander je je Slack-profielfoto, dan verandert de handtekening mee.

## Nieuwe collega toevoegen of gegevens wijzigen

Bewerk nooit `v2/<naam>.html` direct, die bestanden worden gegenereerd.

1. Voeg een regel toe aan `PERSONEN` in `v2/generate.py` (of pas een bestaande aan). Geen telefoonnummer: `None, None`.
2. Draai `python3 v2/generate.py`.
3. Commit en push. De bestanden werken pas als ze op `main` staan.

De Slack-foto-URL vind je via je Slack-profiel: klik op je foto, "Openen in browser", kopieer de URL.

## Kaart wijzigen (tagline, stats, knop)

De zwarte kaart komt uit `v2/assets/plate.html`. Na een wijziging daarin de PNG opnieuw renderen:

```bash
npm install playwright && npx playwright install chromium   # eenmalig
node v2/render-plate.mjs
```

Commit `plate.html` en `plate.png` samen. De acht handtekeningen hoeven niet opnieuw gegenereerd te worden zolang de afmeting 520 x 184 blijft; verandert die, pas dan `width`/`height` van de kaart in `v2/template.html` aan en draai `generate.py`.

## Template wijzigen

`v2/template.html` is de bron. De blokken tussen `<!-- X: aanpassen! -->` en `<!-- END -->` worden per persoon ingevuld door `generate.py`. Na een wijziging aan de template altijd `python3 v2/generate.py` draaien en alle acht bestanden meecommitten.
