# common.py - pieces every page shares: styling, the research library,
# the "things to consider" box, and the footer.

import json
from pathlib import Path

import streamlit as st

HERE = Path(__file__).parent
REPO_URL = "https://github.com/audreypham2007-spec/cld-navigator"

# app.py fills this in, so pages can link to each other: PAGES["cases"], etc.
PAGES = {}

KIND_LABELS = {
    "language": "From language research",
    "exposure": "From the child's exposure",
    "general": "For every bilingual child",
}

# Colors. Teal always means "hears". Gold always means "speaks".
INK, MUTED, RULE, PANEL = "#1C2B33", "#5A6A70", "#DCE3E3", "#F2F5F5"
TEAL, GOLD, GOLD_TEXT = "#0E4F57", "#E5B12E", "#8A6508"
RASPBERRY, PURPLE, CHOCOLATE = "#B3205A", "#6B4E9B", "#5E3A26"
BERRY, LEAF, SKY = RASPBERRY, PURPLE, CHOCOLATE  # older names
DISPLAY = "'Lexend', sans-serif"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300..700&display=swap');

/* ---------- base ----------
   Spacing scale: 0.5, 1, 1.5, 2.5, 4 rem. Type scale: 0.875, 1, 1.125, 1.25,
   1.6, 2.4, 3.2 rem. Every margin and size below comes from these. */
.block-container {{max-width: 64rem; padding-top: 4rem; padding-bottom: 4rem;}}
[data-testid="stHeading"] {{margin: 0 !important;}}
h1, h2, h3 {{font-family: {DISPLAY} !important; color: {INK} !important;
             letter-spacing: -0.02em;}}
h1 {{font-weight: 600 !important; font-size: 2.4rem !important;}}
h2 {{font-weight: 600 !important; font-size: 1.6rem !important;
     padding: 0 !important; margin: 2.5rem 0 0.5rem !important;}}
h3 {{font-size: 1.25rem !important;}}
h3, h4 {{font-weight: 600 !important;}}
p, li {{line-height: 1.65;}}
a {{color: {TEAL};}}

/* Flat, quiet borders instead of floating cards */
[data-testid="stExpander"] details {{border: 1px solid {RULE}; border-radius: 8px;
                                     box-shadow: none;}}
[data-testid="stVerticalBlockBorderWrapper"] {{border-color: {RULE} !important;
                                               border-radius: 8px !important;}}
[data-testid="stMetric"] {{border-color: {RULE} !important; border-radius: 8px !important;}}
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {{
    border-radius: 999px !important; font-weight: 500 !important; padding: 0.55rem 1.3rem;}}
/* Gold means "click here". It appears on primary buttons and nowhere decorative. */
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {{
    background: {GOLD} !important; border-color: {GOLD} !important; color: {INK} !important;
    font-weight: 600 !important;}}
[data-testid="stBaseButton-primary"]:hover,
[data-testid="stBaseButton-primaryFormSubmit"]:hover {{filter: brightness(0.94);}}

/* ---------- home ---------- */
.st-key-hero {{background-color: {TEAL}; border-radius: 22px; padding: 2.5rem;
    background-image: radial-gradient(rgba(255,255,255,0.07) 1.2px, transparent 1.2px);
    background-size: 18px 18px;}}
.st-key-hero .home-title {{color: #FFFFFF;}}
.st-key-hero .home-lede {{color: #CFE3E1;}}
.st-key-hero [data-testid="stBaseButton-primary"] {{background: {GOLD} !important;
    border-color: {GOLD} !important; color: {INK} !important; font-weight: 600 !important;}}
.st-key-hero [data-testid="stBaseButton-secondary"] {{background: transparent !important;
    border-color: rgba(255,255,255,0.55) !important; color: #FFFFFF !important;}}
.st-key-story {{background: #F9E3EB; border-radius: 22px; padding: 2.5rem; margin-top: 2.5rem;}}
.st-key-story .quote .sign {{color: {RASPBERRY};}}
.home-title {{font-family: {DISPLAY}; font-weight: 600; font-size: clamp(2.2rem, 4.6vw, 3.3rem);
              line-height: 1.1; letter-spacing: -0.025em; color: {INK}; margin: 0 0 1rem;}}
.home-lede {{font-size: 1.125rem; line-height: 1.65; color: #44555B; max-width: 32rem;
             margin: 0 0 1.5rem; font-weight: 300;}}
.home-art svg {{width: 100%; height: auto; display: block;}}

.steps {{display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; position: relative;}}
.steps::before {{content: ""; position: absolute; top: 2.7rem; left: 3rem; right: 3rem;
                 border-top: 2px dashed #BFD8D8; z-index: 0;}}
.step {{position: relative; z-index: 1;}}
.step {{border-radius: 18px; padding: 1.5rem;}}
.step .num {{display: inline-flex; align-items: center; justify-content: center;
             width: 2.4rem; height: 2.4rem; border-radius: 50%; color: #FFFFFF;
             font-weight: 600; font-size: 1.05rem;}}
.step .title {{font-weight: 600; font-size: 1.06rem; margin: 1rem 0 0.5rem; color: {INK};}}
.step .text {{color: #44555B; font-size: 0.96rem; line-height: 1.6; font-weight: 300;}}
.step {{background: {PANEL};}} .step .num {{background: {TEAL};}}

.quote p {{font-size: clamp(1.2rem, 2.2vw, 1.5rem); line-height: 1.55; color: {INK};
           margin: 0 0 1rem; font-weight: 400;}}
.quote .sign {{color: {TEAL}; font-weight: 600;}}
.quote .role {{color: {MUTED}; font-size: 0.92rem; font-weight: 300;}}
.st-key-story h2 {{margin-top: 0 !important;}}

.langs {{display: flex; flex-wrap: wrap; gap: 1rem; margin: 0 0 1rem;}}
.lang {{border-radius: 16px; padding: 1rem 1.5rem; min-width: 8.5rem;}}
.lang .autonym {{display: block; font-size: 1.6rem; font-weight: 500; line-height: 1.25;}}
.lang .english {{display: block; font-size: 0.84rem; color: #44555B; font-weight: 300;}}
.lang.l0 {{background: #F9E3EB;}} .lang.l0 .autonym {{color: {BERRY};}}
.lang.l1 {{background: #E2EEEE;}} .lang.l1 .autonym {{color: {TEAL};}}
.lang.l2 {{background: #FCF3D6;}} .lang.l2 .autonym {{color: #B98A0E;}}
.lang.l3 {{background: #EEE8F5;}} .lang.l3 .autonym {{color: {LEAF};}}
.lang.l4 {{background: #F3EAE3;}} .lang.l4 .autonym {{color: {SKY};}}

.facts {{display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;}}
.facts span {{background: rgba(255,255,255,0.12); color: #FFFFFF !important; border-radius: 999px; padding: 0.3rem 0.85rem;
              font-size: 0.86rem; color: {INK};}}

.risks {{display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;}}
.risk {{border-radius: 18px; padding: 1.5rem; background: #FFFFFF;
        border: 2px solid;}}
.risk.r1 {{border-color: #EFC3D4;}} .risk.r1 .risk-title {{color: {BERRY};}}
.risk.r2 {{border-color: #BFD8D8;}} .risk.r2 .risk-title {{color: {TEAL};}}
.risk-title {{font-weight: 600; font-size: 1.15rem; margin-bottom: 0.5rem;}}
.risk p {{margin: 0; color: #44555B; font-weight: 300;}}
.risk-quote {{grid-column: 1 / -1; margin-top: 0.5rem; color: {INK}; font-size: 1rem;
               max-width: 46rem; line-height: 1.6;}}
.pv-src {{display: block; color: {MUTED}; font-size: 0.8rem; margin-top: 0.3rem;
          font-weight: 300;}}

.preview {{background: #FFFFFF; border: 1px solid {RULE}; border-radius: 18px;
           padding: 1.5rem; box-shadow: 0 18px 40px -24px rgba(31,111,120,0.45);}}
.pv-head {{display: flex; justify-content: space-between; align-items: baseline;
           margin-bottom: 0.6rem;}}
.pv-head span {{color: {MUTED}; font-size: 0.82rem;}}
.pv-key {{font-size: 0.8rem; color: {MUTED}; margin-bottom: 0.5rem;}}
.pv-key i {{display: inline-block; width: 0.65rem; height: 0.65rem; border-radius: 2px;
            margin: 0 0.3rem -0.05rem 0.5rem;}}
.pv-key i:first-child {{margin-left: 0;}}
.pv-row {{display: grid; grid-template-columns: 5.6rem 1fr 2.6rem; align-items: center;
          gap: 0.6rem; margin: 0.18rem 0;}}
.pv-lang {{font-size: 0.86rem; font-weight: 500;}}
.pv-bar {{background: {PANEL}; border-radius: 999px; height: 0.6rem; overflow: hidden;}}
.pv-bar span {{display: block; height: 100%; border-radius: 999px;}}
.pv-num {{font-size: 0.8rem; color: {MUTED}; text-align: right;}}
.pv-title {{font-weight: 600; margin: 0.9rem 0 0.2rem;}}
.preview ul {{margin: 0; padding-left: 1.1rem; font-size: 0.88rem; line-height: 1.55;}}
.preview li {{margin-bottom: 0.5rem;}}
.side-lede {{font-size: 1.2rem; font-weight: 500; line-height: 1.5; color: {INK};}}
.side-text {{color: #44555B; font-weight: 300; line-height: 1.7;}}

.cited {{margin-top: 2.5rem; padding: 1.5rem 0; border-top: 1px solid {RULE};
         border-bottom: 1px solid {RULE};}}
.cited-label {{color: {MUTED}; font-size: 0.875rem; margin-bottom: 0.5rem;}}
.cited-list {{display: flex; flex-wrap: wrap; gap: 0.5rem 1.6rem;}}
.cited-list span {{font-weight: 500; color: {INK}; font-size: 0.95rem;}}

.st-key-cta {{background: {TEAL}; border-radius: 22px; padding: 2.5rem; margin-top: 2.5rem;}}
.cta-title {{color: #FFFFFF; font-size: 1.4rem; font-weight: 600; line-height: 1.3;}}
.cta-text {{color: #CFE3E1; font-weight: 300; margin-top: 0.3rem;}}
.st-key-cta [data-testid="stBaseButton-primary"] {{background: {GOLD} !important;
    border-color: {GOLD} !important; color: {INK} !important; font-weight: 600 !important;}}

/* ---------- announcement bar (scrolls sideways, like rhode's) ---------- */
.ticker {{overflow: hidden; background: #E2EEEE; color: {TEAL}; border-radius: 999px;
          margin: -1.5rem 0 1.5rem; padding: 0.5rem 0; font-size: 0.875rem;}}
.ticker-track {{display: inline-flex; gap: 3rem; white-space: nowrap; padding-right: 3rem;
                animation: ticker 38s linear infinite;}}
.ticker-track span::before {{content: ""; display: inline-block; width: 0.45rem;
                             height: 0.45rem; border-radius: 50%; background: {GOLD};
                             margin: 0 0.75rem 0.1rem 0; background: {TEAL};}}
@keyframes ticker {{from {{transform: translateX(0);}} to {{transform: translateX(-50%);}}}}
@media (prefers-reduced-motion: reduce) {{
  .ticker-track {{animation: none; padding-left: 1.5rem;}}
}}

/* ---------- language carousel ---------- */
.section-sub {{color: {MUTED}; font-weight: 300; margin: 0 0 1rem;}}
.carousel {{display: flex; gap: 1rem; overflow-x: auto; scroll-snap-type: x mandatory;
            padding: 0.25rem 0.25rem 1rem; margin: 0 -0.25rem;
            scrollbar-width: thin;}}
.card {{flex: 0 0 15.5rem; scroll-snap-align: start; border-radius: 18px; padding: 1.5rem;
        text-decoration: none !important;
        display: flex; flex-direction: column; transition: transform 0.2s ease, box-shadow 0.2s ease;}}
.card {{box-shadow: 0 1px 0 rgba(28,43,51,0.04);}}
.card:hover {{transform: translateY(-4px); box-shadow: 0 16px 30px -18px rgba(28,43,51,0.45);}}
.card-top {{display: flex; justify-content: space-between; align-items: center;
            gap: 0.5rem; margin-bottom: 1rem;}}
.card-tag {{font-weight: 500; font-size: 0.875rem;}}
.card-badge {{background: #FFFFFF; border-radius: 999px; padding: 0.15rem 0.6rem;
              font-size: 0.75rem; color: {INK}; white-space: nowrap;}}
.card-autonym {{font-size: 2rem; font-weight: 500; line-height: 1.2; text-align: left;
                 unicode-bidi: plaintext;}}
.card-name {{font-weight: 600; margin: 0.25rem 0 0.5rem; color: inherit;}}
.card * {{color: inherit;}}
.card .card-name, .card .card-text {{color: {INK} !important;}}
.card .card-badge {{color: {INK} !important;}}
.card-text {{font-size: 0.875rem; font-weight: 300; line-height: 1.55; color: inherit; opacity: 0.88;
             flex: 1;}}
.card-link {{font-size: 0.875rem; font-weight: 600; margin-top: 1rem;}}
@media (prefers-reduced-motion: reduce) {{ .card {{transition: none;}} }}

/* ---------- big number ---------- */
.bigstat {{display: grid; grid-template-columns: auto 1fr; gap: 2rem; align-items: center;
           border-radius: 22px; background: #E2EEEE; color: {INK}; padding: 2.5rem;
           margin-top: 2.5rem;}}
.bigstat .n {{font-size: clamp(3.5rem, 9vw, 6rem); font-weight: 600; line-height: 1;
              letter-spacing: -0.04em; color: {TEAL};}}
.bigstat .t {{font-size: 1.25rem; font-weight: 500; line-height: 1.45;}}
.bigstat .s {{font-size: 0.875rem; font-weight: 300; color: {MUTED}; margin-top: 0.5rem;}}

/* ---------- built for ---------- */
.personas {{display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;}}
.persona {{border: 2px solid {RULE}; border-radius: 18px; padding: 1.5rem;}}
.persona .who {{font-weight: 600; font-size: 1.125rem; margin-bottom: 0.5rem;}}
.persona p {{margin: 0; color: #44555B; font-weight: 300;}}

/* ---------- FAQ ---------- */
.faq details {{border-bottom: 1px solid {RULE}; padding: 1rem 0;}}
.faq summary {{cursor: pointer; font-weight: 500; font-size: 1.125rem; list-style: none;
               display: flex; justify-content: space-between; gap: 1rem;}}
.faq summary::-webkit-details-marker {{display: none;}}
.faq summary::after {{content: "+"; color: {TEAL}; font-weight: 600;}}
.faq details[open] summary::after {{content: "\u2212";}}
.faq details p {{margin: 0.75rem 0 0; color: #44555B; font-weight: 300; max-width: 44rem;}}

/* ---------- page headers on every tab ---------- */
.page-head {{border-radius: 22px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
             display: grid; grid-template-columns: 1fr 12rem; gap: 2rem; align-items: center;}}
.ph-art svg {{width: 100%; height: auto; display: block;}}
.ph-chips {{display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;}}
.ph-chips span {{background: rgba(255,255,255,0.12); color: #FFFFFF; border-radius: 999px;
                 padding: 0.3rem 0.85rem; font-size: 0.875rem;}}
.page-head .ph-title {{font-size: 2.4rem; font-weight: 600; letter-spacing: -0.02em;
                       line-height: 1.15; color: {INK};}}
.page-head .ph-lede {{font-size: 1.125rem; font-weight: 300; color: #44555B;
                      max-width: 40rem; margin: 0.5rem 0 0; line-height: 1.6;}}
.page-head {{background: {TEAL};}}
.page-head .ph-title {{color: #FFFFFF;}}
.page-head .ph-lede {{color: rgba(255,255,255,0.82);}}

/* Numbered chunks on the New Assessment form */
.chunk {{display: flex; align-items: center; gap: 0.75rem; font-weight: 600;
         font-size: 1.25rem; margin: 1.5rem 0 0.5rem; color: {INK};}}
.chunk .n {{display: inline-flex; align-items: center; justify-content: center;
            width: 2rem; height: 2rem; border-radius: 50%; color: #FFFFFF;
            font-size: 0.95rem;}}
.chunk-hint {{color: {MUTED}; font-size: 0.875rem; font-weight: 300; margin: -0.25rem 0 0.5rem;}}

/* Knowledge Library language header */
.lib-head {{display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap;}}
.lib-head .autonym {{font-size: 2.4rem; font-weight: 500; line-height: 1.2;}}
.lib-head .english {{font-size: 1.25rem; font-weight: 600; color: {INK};}}
.lib-share {{color: {MUTED}; font-size: 0.875rem; font-weight: 300; margin: 0.25rem 0 1rem;}}
.lib-summary {{font-size: 1.125rem; line-height: 1.6; margin: 0 0 1rem; color: {INK};}}

/* Two side-by-side panels (About page) */
.duo {{display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem;}}
.duo > div {{border-radius: 18px; padding: 1.5rem;}}
.duo .t {{font-weight: 600; font-size: 1.125rem; margin-bottom: 0.5rem;}}
.duo p {{margin: 0; color: #44555B; font-weight: 300;}}

/* Family Interview questions */
.q-title {{font-weight: 600; font-size: 1.125rem; margin-bottom: 0.5rem;}}
.q-block ol {{margin: 0; padding-inline-start: 1.5rem;}}
.q-block li {{margin-bottom: 0.5rem; line-height: 1.6;}}
.q-en {{color: {MUTED}; font-size: 0.875rem; font-weight: 300; text-align: left;}}

/* ---------- Knowledge Library: Vietnamese tones ---------- */
.tones {{display: flex; flex-wrap: wrap; gap: 0.4rem 1.6rem; margin: 0.2rem 0 0.4rem;}}
.tone .syl {{display: block; font-size: 1.7rem; font-weight: 500; color: {TEAL};
             line-height: 1.2;}}
.tone .gloss {{display: block; font-size: 0.8rem; color: {MUTED};}}

/* Hears / speaks key */
.key {{color: {MUTED}; font-size: 0.88rem;}}
.key .dot {{display: inline-block; width: 0.7rem; height: 0.7rem; border-radius: 2px;
            margin: 0 0.3rem -0.05rem 0;}}

/* Things to consider */
.tip-group {{font-weight: 600; margin: 0.9rem 0 0.2rem; color: {INK};}}
.tip-source {{color: {MUTED}; font-size: 0.82rem; margin: -0.35rem 0 0.4rem 1.6rem;}}

.footer {{margin-top: 4rem; background: #F4F7F7; border-radius: 22px; padding: 2.5rem;
          display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 2rem;}}
.footer .brand {{font-weight: 600; font-size: 1.25rem; color: {TEAL};}}
.footer p {{color: {MUTED}; font-size: 0.875rem; font-weight: 300; margin: 0.5rem 0 0;
            line-height: 1.6;}}
.footer .col-title {{font-weight: 600; font-size: 0.875rem; color: {INK}; margin-bottom: 0.5rem;}}
.footer a {{display: block; color: {INK} !important; text-decoration: none;
            font-size: 0.875rem; padding: 0.2rem 0;}}
.footer a:hover {{color: {TEAL} !important; text-decoration: underline;}}

@media (max-width: 720px) {{
  .steps {{grid-template-columns: 1fr; gap: 0.9rem;}}
  .st-key-hero, .st-key-story, .st-key-cta {{padding: 1.4rem 1.3rem; border-radius: 16px;}}
  .risks, .duo, .personas, .footer {{grid-template-columns: 1fr;}}
  .steps::before {{display: none;}}
  .bigstat {{grid-template-columns: 1fr; gap: 1rem; padding: 1.5rem;}}
  .page-head {{padding: 1.5rem; grid-template-columns: 1fr;}}
  .ph-art {{display: none;}}
  .page-head .ph-title {{font-size: 1.9rem;}}
  .lang {{min-width: 0; flex: 1 1 40%;}}
}}
</style>
"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)


TINTS = {"mint": TEAL, "butter": TEAL, "pink": TEAL, "sky": TEAL, "leaf": TEAL}


TICKER_ITEMS = [
    "Now covering Spanish, Vietnamese, Mandarin, Arabic, and Cantonese",
    "The home languages of 88% of California English learners",
    "Every prompt cites its source",
    "Free, no account needed",
    "Built by a California State University, Fullerton Communication Sciences and "
    "Disorders student",
]


def announcement_bar():
    """The slim scrolling bar at the top of every page."""
    items = "".join(f"<span>{t}</span>" for t in TICKER_ITEMS * 2)
    st.markdown(f'<div class="ticker" aria-label="Announcements"><div class="ticker-track">'
                f'{items}</div></div>', unsafe_allow_html=True)


def page_header(title, lede, tint="mint", art="", chips=()):
    """The colored header at the top of every tab: title, one-line benefit,
    short tags, and a small hand-drawn illustration."""
    tags = "".join(f"<span>{c}</span>" for c in chips)
    st.markdown(f'<div class="page-head ph-{tint}"><div><div class="ph-title">{title}</div>'
                f'<p class="ph-lede">{lede}</p>'
                + (f'<div class="ph-chips">{tags}</div>' if tags else "")
                + f'</div><div class="ph-art">{art}</div></div>', unsafe_allow_html=True)


def chunk(number, title, tint="mint", hint=None):
    """A numbered section label, so a long form reads as a few short steps."""
    st.markdown(f'<div class="chunk"><span class="n" style="background:{TINTS[tint]}">'
                f'{number}</span>{title}</div>'
                + (f'<div class="chunk-hint">{hint}</div>' if hint else ""),
                unsafe_allow_html=True)


def exposure_key():
    """The small hears/speaks color key shown above exposure charts."""
    st.markdown(f'<div class="key"><span class="dot" style="background:{TEAL}"></span>'
                f'Hears &nbsp;&nbsp;<span class="dot" style="background:{GOLD}"></span>'
                'Speaks</div>', unsafe_allow_html=True)


def _library_mtime():
    path = HERE / "language_notes.json"
    return path.stat().st_mtime if path.exists() else 0


@st.cache_data
def _read_library(mtime):
    try:
        with open(HERE / "language_notes.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_library():
    """Research notes from language_notes.json. Reloads when the file changes."""
    return _read_library(_library_mtime())


def years_months(months):
    years, rest = divmod(int(months), 12)
    return f"{years} yr {rest} mo"


def show_considerations(tips):
    """Show the 'things to consider', grouped by where they come from."""
    with st.container(border=True):
        st.markdown("#### Things to consider")
        for kind, label in KIND_LABELS.items():
            group = [t for t in tips if t["kind"] == kind]
            if not group:
                continue
            st.markdown(f'<div class="tip-group">{label}</div>', unsafe_allow_html=True)
            for t in group:
                st.markdown(f"- {t['text']}")
                if t.get("source"):
                    st.markdown(f'<div class="tip-source">Source: {t["source"]}</div>',
                                unsafe_allow_html=True)
        st.caption("Support only. The SLP makes all clinical decisions.")


def case_summary_text(case, tips):
    """Plain-text version of a case, for the download button."""
    lines = [f"CLD Navigator case summary: {case.case_code}",
             f"Age: {case.age_months} months ({years_months(case.age_months)})",
             "", "Languages:"]
    for lang in case.languages:
        lines.append(f"- {lang.name}: hears {lang.percent_hears}%, "
                     f"speaks {lang.percent_speaks}%")
    lines += ["", f"Concerns: {case.concerns or 'None'}",
              f"Notes: {case.notes or 'None'}", "", "Things to consider:"]
    for t in tips:
        lines.append(f"- {t['text']}")
        if t.get("source"):
            lines.append(f"  Source: {t['source']}")
    lines += ["", "This summary offers support only. "
              "The SLP makes all clinical decisions."]
    return "\n".join(lines)


def footer():
    st.markdown(f"""
<div class="footer">
  <div><div class="brand">CLD Navigator</div>
  <p>Assessment support for speech-language pathologists working with bilingual
  children. Built by Audrey Pham, Communication Sciences and Disorders, California
  State University, Fullerton.</p>
  <p>Support only. Not a diagnostic test.</p></div>
  <div><div class="col-title">Use it</div>
  <a href="new-assessment" target="_self">New Assessment</a>
  <a href="saved-cases" target="_self">Saved Cases</a>
  <a href="family-interview" target="_self">Family Interview</a>
  <a href="insights" target="_self">Insights</a></div>
  <div><div class="col-title">Learn</div>
  <a href="knowledge-library" target="_self">Knowledge Library</a>
  <a href="about" target="_self">About and limitations</a>
  <a href="{REPO_URL}" target="_blank">Source code on GitHub</a></div>
</div>""", unsafe_allow_html=True)
