# report.py - builds printable reports as web pages (.html files).
# Open a downloaded report in any browser, then use Print > Save as PDF.

from datetime import date
from html import escape

STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&family=Literata:ital,opsz,wght@0,7..72,400;1,7..72,400&display=swap" rel="stylesheet">
<style>
  :root {--teal:#0E4F57; --gold:#E5B12E; --berry:#B3205A; --ink:#13303A; --slate:#56676D;
         --rule:#DCE3E3; --teal50:#F1F7F7; --gold50:#FCF5DE; --berry50:#FBEDF2;}
  * {-webkit-print-color-adjust: exact; print-color-adjust: exact;}
  body {font-family: 'Be Vietnam Pro', 'Segoe UI', Arial, sans-serif; color: var(--ink);
        max-width: 760px; margin: 32px auto; padding: 0 28px; line-height: 1.55; font-size: 15px;}
  .band {display: flex; justify-content: space-between; align-items: center;
         background: linear-gradient(160deg, #11606A, var(--teal) 55%, #0A3B41); color: #fff;
         border-radius: 18px; padding: 16px 22px; margin-bottom: 26px;}
  .band .brand {display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 17px;
                letter-spacing: -0.02em;}
  .band .mk {width: 22px; height: 15px; border-radius: 2px;
             background: linear-gradient(#FFFFFF 0 40%, transparent 40% 60%, var(--gold) 60% 100%);}
  .band .doc {font-size: 12.5px; color: #D6E8E6;}
  h1 {font-weight: 800; font-size: 30px; letter-spacing: -0.035em; line-height: 1.1; margin: 0;
      color: var(--ink);}
  h2 {font-weight: 700; font-size: 17px; letter-spacing: -0.015em; color: var(--teal);
      margin: 26px 0 8px; padding-bottom: 6px; border-bottom: 2px solid var(--teal50);}
  .meta {color: var(--slate); margin-top: 6px;}
  table {border-collapse: collapse; width: 100%;}
  th, td {text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--rule);}
  th {font-size: 12.5px; color: var(--slate);}
  .bar {background: var(--teal50); border-radius: 99px; height: 9px; width: 160px;}
  .fill {background: var(--teal); border-radius: 99px; height: 9px;}
  .fill.speak {background: var(--gold);}
  .source {color: var(--slate); font-size: 0.85em; font-family: 'Literata', Georgia, serif;
           font-style: italic;}
  .answer {border-bottom: 1px solid #B8C4C2; height: 26px; margin-bottom: 10px;}
  .note {background: var(--gold50); border-left: 4px solid var(--gold); padding: 10px 14px;
         margin-top: 28px; font-size: 0.9em; border-radius: 0 10px 10px 0;}
  .foot {display: flex; justify-content: space-between; margin-top: 18px; padding-top: 10px;
         border-top: 1px solid var(--rule); font-size: 11.5px; color: var(--slate);}
  li {margin-bottom: 4px;}
  @media print {body {margin: 0 auto;} .note, h2 {break-inside: avoid; break-after: avoid;}}
</style>
"""

DISCLAIMER = ("CLD Navigator offers support only. It does not diagnose and is not a "
              "test. The SLP makes all clinical decisions.")


SITE = "cld-navigator.streamlit.app"


def _page(title, body):
    band = (f"<div class='band'><div class='brand'><span class='mk'></span>CLD Navigator</div>"
            f"<div class='doc'>{escape(title)}</div></div>")
    foot = (f"<div class='foot'><span>{SITE}</span><span>Made {date.today():%B %d, %Y}"
            "</span></div>")
    return (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{escape(title)}</title>{STYLE}</head><body>{band}{body}"
            f"<div class='note'>{DISCLAIMER}</div>{foot}</body></html>")


def _bar(percent, speak=False):
    css = "fill speak" if speak else "fill"
    return (f"<div class='bar'><div class='{css}' style='width:{int(percent or 0)}%'>"
            "</div></div>")


def case_report_html(case, tips, years_months, sound_gaps=()):
    rows = "".join(
        f"<tr><td>{escape(l.name)}</td>"
        f"<td>{l.percent_hears}% {_bar(l.percent_hears)}</td>"
        f"<td>{l.percent_speaks}% {_bar(l.percent_speaks, speak=True)}</td></tr>"
        for l in case.languages)
    tip_items = "".join(
        f"<li>{escape(t['text'])}"
        + (f"<br><span class='source'>Source: {escape(t['source'])}</span>"
           if t.get("source") else "")
        + "</li>" for t in tips)
    body = f"""
<h1>Case summary: {escape(case.case_code)}</h1>
<p class="meta">Age {case.age_months} months ({years_months(case.age_months)}) ·
Report made {date.today():%B %d, %Y}</p>
<h2>Language exposure</h2>
<table><tr><th>Language</th><th>Hears</th><th>Speaks</th></tr>{rows}</table>
<h2>Concerns from family or teacher</h2><p>{escape(case.concerns or 'None')}</p>
<h2>Clinician notes</h2><p>{escape(case.notes or 'None')}</p>
<h2>Things to consider</h2><ul>{tip_items}</ul>
"""
    for language, sounds, source in sound_gaps:
        chips = "".join(f"<span>/{escape(ipa)}/ {escape(word)}</span>" for ipa, word in sounds)
        body += (f"<h2>English sounds not in {escape(language)}</h2>"
                 f"<p class='chips'>{chips}</p><p class='source'>Source: {escape(source)}</p>")
    return _page(f"{case.case_code} summary", (SHEET_STYLE if sound_gaps else "") + body)


def interview_html(sections, case_code, labels, code="en", with_english=False,
                   rtl=False):
    """A printable interview guide with space to write answers.

    sections comes from content.interview_lines(). labels is
    content.INTERVIEW_LABELS. code is the interview language code.
    """
    def label(key):
        main = labels[key][code]
        return f"{main} / {labels[key]['en']}" if with_english and code != "en" else main

    parts = [f"<h1>{escape(label('heading'))}</h1>"
             f"<p class='meta'>{escape(label('case'))}: "
             f"{escape(case_code or '__________')} &nbsp; {escape(label('date'))}: "
             f"____________<br>{escape(label('interpreter'))}</p>"]
    for title, lines in sections:
        parts.append(f"<h2>{escape(title)}</h2><ol>")
        for main, english in lines:
            text = escape(main)
            if english:
                text += f"<br><span class='source' dir='ltr'>{escape(english)}</span>"
            parts.append(f"<li>{text}<div class='answer'></div></li>")
        parts.append("</ol>")
    page = _page(labels["heading"][code], "".join(parts))
    if rtl:
        page = page.replace("<html>", "<html dir='rtl' lang='ar'>", 1)
    return page


SHEET_STYLE = """
<style>
  .grid {display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin: 8px 0 4px;}
  .tile {border: 1.5px solid #DCE3E3; border-radius: 8px; text-align: center; padding: 6px 2px;}
  .tile > b {display: block; font-size: 1.3em; font-family: Arial, sans-serif;}
  .tile span b {text-decoration: underline; color: inherit;}
  .tile span {font-size: 0.8em; color: #5D6E72;}
  .tile.miss {background: #B3205A; border-color: #B3205A; color: #FFFFFF;}
  .tile.miss span {color: #F6D3E0;}
  .group {font-weight: bold; margin-top: 10px; font-family: Arial, sans-serif; font-size: 0.85em;
          color: #0E4F57;}
  .key {font-family: Arial, sans-serif; font-size: 0.85em; color: #5D6E72;}
  .key i {display: inline-block; width: 12px; height: 12px; border-radius: 3px;
          vertical-align: -1px; margin: 0 4px 0 12px; border: 1.5px solid #DCE3E3;}
  .key i.m {background: #B3205A; border-color: #B3205A; margin-left: 0;}
  .chips span {display: inline-block; border: 1.5px solid #DCE3E3; border-radius: 6px;
               padding: 2px 10px; margin: 0 4px 4px 0; font-family: Arial, sans-serif;}
  @media print {.tile.miss, .key i.m {-webkit-print-color-adjust: exact; print-color-adjust: exact;}}
</style>
"""


def sound_sheet_html(language, data, groups, word_html):
    """A one-page printable sheet: English consonants the home language doesn't use."""
    missing = data["missing"]
    total = sum(len(g) for g in groups.values())
    blocks = ""
    for group, sounds in groups.items():
        tiles = "".join(
            f"<div class='tile{' miss' if ipa in missing else ''}'><b>{escape(ipa)}</b>"
            f"<span>{word_html(word, letters)}</span></div>" for ipa, word, letters in sounds)
        blocks += f"<div class='group'>{escape(group)}</div><div class='grid'>{tiles}</div>"
    extras = "".join(
        f"<h2>{escape(title)}</h2><p>{escape(lede)}</p><p class='chips'>"
        + "".join(f"<span>{escape(c)}</span>" for c in chips)
        + f"</p><p>{escape(text)}</p>" for title, lede, chips, text in data["extras"])
    sources = "".join(f"<li class='source'>{escape(s)}</li>" for s in data["sources"])
    body = f"""
<h1>English sounds and {escape(language)}</h1>
<p class="meta">{len(missing)} of {total} English consonants are not used in
{escape(language)}<br>Sheet made {date.today():%B %d, %Y}</p>
<p class="key"><i class="m"></i>Not in {escape(language)}<i></i>In both languages</p>
{blocks}
<p class="source">{escape(data['note'])}</p>
{extras}
<h2>How to use this sheet</h2>
<p>Compare the child's English errors with the highlighted sounds. Errors on sounds the
home language doesn't have may reflect the home language. Errors on sounds both languages
share, or errors in the home language too, deserve a closer look.</p>
<h2>Sources</h2><ul>{sources}</ul>
"""
    return _page(f"{language} sound sheet", SHEET_STYLE + body)


CARD_STYLE = """
<style>
  .hello svg {width: 100%; height: auto; display: block; margin: 4px 0 6px;}
  .cards {display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px;}
  .card {border: 1px solid var(--rule); border-radius: 14px; padding: 14px 16px; border-top: 5px solid var(--teal);
         break-inside: avoid;}
  .card:nth-child(2) {border-top-color: var(--gold);} .card:nth-child(3) {border-top-color: var(--berry);}
  .card:nth-child(4) {border-top-color: #6B4E9B;}
  .card .n {font-weight: 800; font-size: 26px; line-height: 1; color: var(--teal);}
  .card:nth-child(2) .n {color: #C9951A;} .card:nth-child(3) .n {color: var(--berry);}
  .card:nth-child(4) .n {color: #6B4E9B;}
  .card .t {font-weight: 700; font-size: 15.5px; margin: 6px 0 4px; letter-spacing: -0.01em;}
  .card p {margin: 0; font-family: 'Literata', Georgia, serif; font-size: 14px; line-height: 1.5;}
  .card .source {display: block; margin-top: 6px;}
  .ask {background: var(--teal50); border-radius: 14px; padding: 12px 18px; margin-top: 16px;}
  .ask h2 {border: 0; margin-top: 4px;}
  .tiles {display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px;}
  .tile2 {background: var(--teal50); border-radius: 12px; padding: 10px;}
  .tile2 b {display: block; font-size: 24px; font-weight: 800; color: var(--teal); letter-spacing: -0.04em;}
  .tile2 span {font-size: 11.5px; color: var(--slate);}
  .split {display: grid; grid-template-columns: 170px 1fr; gap: 18px; align-items: center;}
  .split svg {width: 100%; height: auto;}
  .big {font-size: 40px; font-weight: 800; color: var(--teal); letter-spacing: -0.05em; line-height: 1;}
</style>
"""


def family_handout_html(points, sources):
    """A one-page, plain-language handout for families raising bilingual children.

    points: [(heading, text, short source)].
    """
    from art import GREETING_SVG
    cards = "".join(f"<div class='card'><div class='n'>{i}</div><div class='t'>{escape(h)}</div>"
                    f"<p>{escape(t)}</p><span class='source'>{escape(s)}</span></div>"
                    for i, (h, t, s) in enumerate(points, 1))
    refs = "".join(f"<li class='source'>{escape(s)}</li>" for s in sources)
    body = f"""
<h1>Raising a bilingual child</h1>
<p class="meta">What research says, for families. Shared by your child's speech-language
pathologist.</p>
<div class="hello">{GREETING_SVG}</div>
<div class="cards">{cards}</div>
<div class="ask"><h2>Questions to bring to your child's SLP</h2>
<ul><li>Which languages will you test my child in?</li>
<li>Will an interpreter join the evaluation?</li>
<li>How can we keep using our home language at home?</li></ul></div>
<h2>Sources</h2><ul>{refs}</ul>
"""
    return _page("Family handout", CARD_STYLE + body)


def project_summary_html(stats, features, sources_count, url, repo, waffle_svg="",
                         coverage=None):
    """A one-page summary of CLD Navigator for portfolios and applications."""
    tiles = "".join(f"<div class='tile2'><b>{escape(str(n))}</b><span>{escape(label)}</span></div>"
                    for n, label in stats)
    feats = "".join(f"<li>{escape(f)}</li>" for f in features)
    reach = (f"<div class='split'><div>{waffle_svg}</div><div><div class='big'>{coverage:.0f}%"
             "</div><p>of California English learners speak one of the home languages the "
             "Knowledge Library covers. Each square is 1% (California Department of "
             "Education, 2022-23).</p></div></div>" if waffle_svg and coverage else "")
    body = f"""
<h1>CLD Navigator</h1>
<p class="meta">Assessment support for speech-language pathologists working with bilingual
children<br>Audrey Pham, Communication Sciences and Disorders, California State
University, Fullerton</p>
<h2>The problem</h2>
<p>Bilingual children who speak less-common languages often get misidentified with speech
disorders. Schools both over- and under-identify English learners with disabilities.</p>
<h2>By the numbers</h2>
<div class="tiles">{tiles}</div>
<h2>Reach</h2>{reach}
<h2>What it does</h2><ul>{feats}</ul>
<h2>How it was built</h2>
<p>Python, Streamlit, SQLAlchemy, SQLite, and pandas. Every prompt and chart names its
source ({sources_count} sources in total). Placeholder rules are labeled, not hidden.</p>
<h2>Links</h2>
<p>Live site: {escape(url)}<br>Source code: {escape(repo)}</p>
"""
    return _page("Project summary", CARD_STYLE + body)


def error_check_html(language, explained, closer, no_data, home_too, sources):
    """A printable Error Check result. Nothing about the child is included."""
    def rows(items, cls):
        return "".join(f"<div class='ec {cls}'><b>{escape(l)}</b><span>{escape(r)}</span></div>"
                       for l, r, _ in items) or "<p class='source'>None.</p>"
    refs = "".join(f"<li class='source'>{escape(s)}</li>" for s in sources)
    extra = ("<p class='note' style='margin-top:12px'>The child shows similar errors in the "
             "home language too. Errors in every language a child speaks deserve a closer "
             "look.</p>" if home_too else "")
    body = f"""
<style>
  .ec {{border-radius: 10px; padding: 8px 12px; margin: 6px 0; display: flex; gap: 12px;
        align-items: baseline; break-inside: avoid;}}
  .ec b {{min-width: 130px;}} .ec.ok {{background: var(--teal50);}}
  .ec.look {{background: var(--gold50);}} .ec.none {{background: #F5F7F7;}}
</style>
<h1>Error Check: {escape(language)}</h1>
<p class="meta">Which of a child's English errors the home language explains, and which
deserve a closer look. Support only.</p>
<h2>Consistent with {escape(language)}</h2>{rows(explained, 'ok')}
<h2>Look closer</h2>{rows(closer, 'look')}{extra}
<h2>No data on this site</h2>{rows(no_data, 'none')}
<h2>Sources</h2><ul>{refs}</ul>
"""
    return _page("Error Check", body)
