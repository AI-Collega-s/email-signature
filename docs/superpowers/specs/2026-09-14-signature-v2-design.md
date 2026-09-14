# E-mailhandtekening v2, Brandbook 2.1

Datum: 2026-09-14
Bron: `../aicollegas-design-system` (Brandbook 2.1, tokens en assets)

## Doel

Alle acht e-mailhandtekeningen omzetten naar de nieuwe huisstijl. De oude
handtekeningen blijven als v1 in de repo staan, zodat collega's die nog niet
zijn overgestapt werkende icon-URL's houden.

## Ontwerpbesluiten

Gekozen via de visual companion op 2026-09-14 (schermen in
`.superpowers/brainstorm/37673-1789397438/content/`).

- Richting C3: persoonsblok boven, daaronder een ink-plate met logo-lockup,
  tagline, witte pill-knop "Nu starten →" en vier stats.
- Contactregel met iconen (e-mail, telefoon, website, LinkedIn), nieuwe
  iconen in ink op 55% dekking, dunne lijn, geen oranje.
- Foto 64 x 64 px met radius 16, zonder rand.
- Foto-URL's blijven de Slack-URL's die nu in v1 staan. Verandert iemand zijn
  Slack-profielfoto, dan verandert de handtekening mee.
- Stats blijven 50+, 85%, 40u, 98%.

## Specificatie

Kleuren

| Rol | Waarde |
| --- | --- |
| Ink (tekst, plate) | `#0A0A0A` |
| Oranje (alleen stat-suffix) | `#F26522` |
| Knop | wit `#FFFFFF`, tekst ink |
| Tekst muted (contact) | `#676767` (rgba(10,10,10,.62) op wit, als hex omdat rgba niet overal werkt in mail) |
| Tekst faint (functie) | `#9D9D9D` (rgba(10,10,10,.40) op wit) |
| Stat-label (wit 50% op ink) | `#858585` |
| Tagline-subregel (wit 55% op ink) | `#919191` |

Typografie

| Element | Font | Gewicht | Grootte |
| --- | --- | --- | --- |
| Naam | Inter | 600 | 16 px, letterspacing -0.01em |
| Functie | JetBrains Mono | 400 | 11 px, letterspacing .04em |
| Contact | Inter | 400 | 13 px |
| Tagline | Inter | 600 | 14 px |
| Tagline-subregel | Inter | 400 | 12 px |
| Knop | Inter | 500 | 13 px |
| Stat-cijfer | JetBrains Mono | 400 | 20 px, letterspacing -0.03em |
| Stat-label | Inter | 400 | 11 px |

Font-stacks: `Inter, "Avenir Next", Avenir, Helvetica, Arial, sans-serif` en
`"JetBrains Mono", Menlo, "Courier New", monospace`. Nooit gewicht 700.

Vormen

- Foto 64 px, `border-radius:16px`.
- Ink-plate `border-radius:20px`, padding 18 px boven/onder, 20 px links/rechts,
  max-breedte 520 px.
- Knop pill (`border-radius:999px`), padding 9 px 16 px.
- Geen randen, geen schaduw, geen gradient, geen verticale lijn naast de foto.

Afbeeldingen (alle via `https://raw.githubusercontent.com/AI-Collega-s/email-signature/main/v2/assets/...`)

- `logo-dark.png`: lockup voor op ink, uit `aicollegas-design-system/assets/png/logo-dark.png`,
  geschaald naar 2x weergavehoogte (44 px hoog), weergegeven op 22 px.
- `icons/icon_email.png`, `icon_phone.png`, `icon_globe.png`, `icon_linkedin.png`:
  28 x 28 px PNG (2x), weergegeven op 14 px, ink op 55% dekking.

Links: `mailto:`, `tel:`, `https://aicollegas.nl`, LinkedIn-profiel, knop naar
`https://aicollegas.nl/contact`.

## Repo-structuur

```
email-signature/
├── v1/                     huidige HTML-bestanden, ongewijzigd (archief)
├── v2/
│   ├── template.html       template met <!-- ... aanpassen! --> markers
│   ├── aaron.html, david.html, jacco.html, jasper.html,
│   │   lars.html, maarten.html, max.html, niels.html
│   └── assets/
│       ├── logo-dark.png
│       └── icons/
├── icons/                  blijft in de root: v1-handtekeningen in mailclients verwijzen hierheen
├── docs/superpowers/specs/
├── README.md
└── .gitignore              .DS_Store, .superpowers/
```

`icons/` in de root blijft staan tot iedereen op v2 zit. Verwijderen is een
aparte, latere beslissing.

## Technische aanpak

- Tabel-gebaseerde HTML met inline styles, zoals v1. Geen `<style>`-blok, geen
  flexbox, geen `rgba()`.
- Alles wat per persoon verschilt staat tussen `<!-- X: aanpassen! -->` en
  `<!-- END -->` markers in `v2/template.html`, net als v1: foto-URL, naam,
  functie, e-mail, LinkedIn-URL en -handle, telefoon.
- Per persoon worden naam, functie, e-mail, telefoon, LinkedIn en foto-URL
  overgenomen uit het v1-bestand. Voor Lars gelden de niet-gecommitte
  wijzigingen (Slack-foto, LinkedIn `lars-nelissen`).
- CTA-pijl: `Nu&nbsp;starten&nbsp;&rarr;` met `white-space:nowrap`, zoals de
  fix in v1 voor Apple Mail.

## Verificatie

- Elke v2-handtekening rendert correct in een browser-preview (screenshot met
  Playwright of Chrome headless) op 600 px breed, licht.
- Alle `src`- en `href`-waarden zijn absoluut en wijzen naar bestaande paden.
- Eén handtekening (Lars) handmatig geplakt in Apple Mail en Gmail-web,
  gecontroleerd op: geen line-break in de knop, iconen zichtbaar, logo scherp.
