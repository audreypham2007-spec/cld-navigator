# report.py - builds printable reports as web pages (.html files).
# Open a downloaded report in any browser, then use Print > Save as PDF.

from datetime import date
from html import escape

STYLE = """
<style>
  body {font-family: Georgia, 'Times New Roman', serif; color: #1E2A2E;
        max-width: 720px; margin: 40px auto; padding: 0 24px; line-height: 1.5;}
  h1 {color: #0E4F57; margin-bottom: 0;}
  h2 {color: #0E4F57; border-bottom: 2px solid #E2EEEE; padding-bottom: 4px;
      margin-top: 28px;}
  .meta {color: #5D6E72; margin-top: 4px;}
  table {border-collapse: collapse; width: 100%;}
  th, td {text-align: left; padding: 6px 10px; border-bottom: 1px solid #E2E8E7;}
  .bar {background: #E2EEEE; border-radius: 4px; height: 10px; width: 160px;}
  .fill {background: #0E4F57; border-radius: 4px; height: 10px;}
  .fill.speak {background: #E5B12E;}
  .source {color: #5D6E72; font-size: 0.85em;}
  .answer {border-bottom: 1px solid #B8C4C2; height: 26px; margin-bottom: 10px;}
  .note {background: #FFF7E8; border-left: 4px solid #E5B12E; padding: 10px 14px;
         margin-top: 28px; font-size: 0.92em;}
  @media print {body {margin: 0;} .note {break-inside: avoid;}}
</style>
"""

DISCLAIMER = ("CLD Navigator offers support only. It does not diagnose and is not a "
              "test. The SLP makes all clinical decisions.")


def _page(title, body):
    return (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{escape(title)}</title>{STYLE}</head><body>{body}"
            f"<div class='note'>{DISCLAIMER}</div></body></html>")


def _bar(percent, speak=False):
    css = "fill speak" if speak else "fill"
    return (f"<div class='bar'><div class='{css}' style='width:{int(percent or 0)}%'>"
            "</div></div>")


def case_report_html(case, tips, years_months):
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
    return _page(f"{case.case_code} summary", body)


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
