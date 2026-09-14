#!/usr/bin/env python3
"""Genereer de persoonlijke handtekeningen uit template.html.

Draaien vanuit de repo-root of vanuit v2/: `python3 v2/generate.py`.
Nieuwe collega: regel toevoegen aan PERSONEN, script draaien, committen.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent

PERSONEN = [
    # bestand, foto-URL, naam, functie, e-mail, LinkedIn-URL, LinkedIn-tag, tel-href, tel-tekst (None = geen nummer)
    ("aaron", "https://ca.slack-edge.com/T08LLV5FSUW-U0ACM13F8SE-709732ccf54b-192", "Aaron Peeters", "Business Development Representative", "aaron@aicollegas.nl", "https://www.linkedin.com/in/aaron-peeters-9404a4389/", "@aaron-peeters", None, None),
    ("david", "https://ca.slack-edge.com/T08LLV5FSUW-U0AARF84MQB-eac78edcfaca-192", "David Nienhuis", "AI Implementatiespecialist", "david@aicollegas.nl", "https://www.linkedin.com/in/david-nienhuis-3761a0266/", "@david-nienhuis", None, None),
    ("jacco", "https://ca.slack-edge.com/T08LLV5FSUW-U08MGDQ902U-b9e64a863500-192", "Jacco Boonstra", "Sales Lead", "jacco@aicollegas.nl", "https://www.linkedin.com/in/jacco-boonstra-50114414a/", "@jacco-boonstra", "+31634222965", "+31 6 3422 2965"),
    ("jasper", "https://ca.slack-edge.com/T08LLV5FSUW-U0BTR93K36H-4d198e80467f-192", "Jasper van Til", "Business Development Representative", "jasper@aicollegas.nl", "https://www.linkedin.com/in/jasper-van-til-41b347291/", "@jasper-van-til", "+31642392164", "+31 6 4239 2164"),
    ("lars", "https://ca.slack-edge.com/T08LLV5FSUW-U0AJRU74QFJ-10552f7c1e45-512", "Lars Nelissen", "AI Software Architect / Developer", "lars@aicollegas.nl", "https://linkedin.com/in/lars-nelissen", "@lars-nelissen", "+31648623550", "+31 6 4862 3550"),
    ("maarten", "https://ca.slack-edge.com/T08LLV5FSUW-U08LW4XPRM2-22a636418de9-192", "Maarten van Milligen", "AI Strategy Lead", "maarten@aicollegas.nl", "https://www.linkedin.com/in/maarten-van-milligen-993840162/", "@maarten-van-milligen", "+31621343266", "+31 6 2134 3266"),
    ("max", "https://ca.slack-edge.com/T08LLV5FSUW-U0BSCEK11S7-g153ce35703c-192", "Max Singh", "AI Software Developer", "max@aicollegas.nl", "https://www.linkedin.com/in/max-singh-225659383/", "@max-singh", None, None),
    ("niels", "https://ca.slack-edge.com/T08LLV5FSUW-U08LLV5FUDU-5556e401d74c-192", "Niels Engelman", "AI Product Lead", "niels@aicollegas.nl", "https://www.linkedin.com/in/niels-engelman-513a77104/", "@niels-engelman", "+31619947619", "+31 6 1994 7619"),
]


def blok(html, marker):
    """Geef (match, inhoud) van het blok tussen `<!-- marker -->` en de eerstvolgende `<!-- END -->`."""
    m = re.search(rf"<!-- {re.escape(marker)} -->\n(.*?)<!-- END -->\n", html, re.S)
    if not m:
        raise SystemExit(f"marker niet gevonden: {marker}")
    return m


def vervang(html, marker, fn):
    """Pas fn toe op de inhoud van het blok en laat de markers zelf weg in de output."""
    m = blok(html, marker)
    return html[: m.start()] + fn(m.group(1)) + html[m.end():]


def sub1(pattern, repl):
    def fn(s):
        nieuw, n = re.subn(pattern, repl, s, count=1)
        if n != 1:
            raise SystemExit(f"patroon niet gevonden: {pattern}")
        return nieuw
    return fn


def naam_en_functie(naam, functie):
    def fn(s):
        regels = s.split("\n")
        regels[0] = re.sub(r">[^<]*</div>", f">{naam}</div>", regels[0], count=1)
        regels[1] = re.sub(r">[^<]*</div>", f">{functie}</div>", regels[1], count=1)
        return "\n".join(regels)
    return fn


def genereer(template, p):
    bestand, foto, naam, functie, email, li_url, li_tag, tel_href, tel_tekst = p
    html = template
    if tel_href is None:
        html = re.sub(r"<!-- TELEFOON CEL[^>]*-->\n.*?<!-- END CEL -->\n", "", html, count=1, flags=re.S)
    else:
        html = html.replace("<!-- TELEFOON CEL: hele cel verwijderen als er geen nummer is -->\n", "", 1).replace("<!-- END CEL -->\n", "", 1)
        html = vervang(html, "TELEFOON LINK: href aanpassen!", sub1(r'href="tel:[^"]*"', f'href="tel:{tel_href}"'))
        html = vervang(html, "TELEFOON TEXT: text aanpassen!", sub1(r">[^<]*</td>", f">{tel_tekst}</td>"))
    html = vervang(html, "FOTO: src aanpassen!", sub1(r'src="[^"]*"', f'src="{foto}"'))
    html = vervang(html, "NAAM & FUNCTIE: text aanpassen!", naam_en_functie(naam, functie))
    html = re.sub(r'alt="[^"]*"( style="display:block;border:0;border-radius:16px)', f'alt="{naam}"\\1', html, count=1)
    html = vervang(html, "EMAIL LINK: href aanpassen!", sub1(r'href="mailto:[^"]*"', f'href="mailto:{email}"'))
    html = vervang(html, "EMAIL TEXT: text aanpassen!", sub1(r">[^<]*</td>", f">{email}</td>"))
    html = vervang(html, "LINKEDIN LINK: href aanpassen!", sub1(r'href="[^"]*"', f'href="{li_url}"'))
    html = vervang(html, "LINKEDIN TAG: text aanpassen!", sub1(r">[^<]*</td>", f">{li_tag}</td>"))
    return html


def main():
    template = (HERE / "template.html").read_text()
    for p in PERSONEN:
        uit = HERE / f"{p[0]}.html"
        uit.write_text(genereer(template, p))
        print("geschreven:", uit.relative_to(HERE.parent))


if __name__ == "__main__":
    main()
