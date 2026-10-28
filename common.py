# common.py - pieces every page shares: styling, the research library,
# the "things to consider" box, and the footer.

import json
from datetime import date
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
INK, MUTED, RULE, PANEL = "#13303A", "#56676D", "#DCE3E3", "#F2F5F5"
TEAL, GOLD, GOLD_TEXT = "#0E4F57", "#E5B12E", "#8A6508"
RASPBERRY, PURPLE, CHOCOLATE = "#B3205A", "#6B4E9B", "#5E3A26"
BERRY, LEAF, SKY = RASPBERRY, PURPLE, CHOCOLATE  # older names
DISPLAY = "'Be Vietnam Pro', 'Noto Sans', system-ui, sans-serif"

# The design system. Every color and size on the site comes from these tokens.
#
# Color roles
#   Teal   #0E4F57  primary. Means "hears". Headers, links, the brand.
#   Gold   #E5B12E  secondary. Means "speaks", and marks the one action to take.
#   Berry  #B3205A  accent. Warnings, the personal story, the first risk.
#   Ink    #13303A  text. Slate #56676D for secondary text.
#   Rule   #DCE3E3  hairlines. Fog #F5F7F7 for quiet panels. Paper #FFFFFF.
#   Tints  (teal-50, gold-50, berry-50, plum-50, cocoa-50) fill large areas so
#          strong colors stay small and meaningful.
# Type
#   Be Vietnam Pro: headings, interface, body. Drawn by Vietnamese designers.
#   Literata: quotes and research summaries, the "reading voice" of the site.
#   Scale (rem): 0.8125, 0.875, 1, 1.0625, 1.1875, 1.375, 1.75, 2.5, 3.75
# Space (rem): 0.5, 1, 1.5, 2, 3, 5. Sections sit 5rem apart, 3.5rem on phones.
# Radius: 28px bands, 16px panels, 10px inputs, 999px pills.
CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;1,7..72,400;1,7..72,500&display=swap');

:root {
  --teal-900: #0A3B41; --teal: #0E4F57; --teal-600: #2E6B72; --teal-100: #DCEBEB; --teal-50: #F1F7F7;
  --gold: #E5B12E; --gold-600: #C9951A; --gold-100: #F8E7B0; --gold-50: #FCF5DE;
  --berry: #B3205A; --berry-100: #F4D3E0; --berry-50: #FBEDF2;
  --plum: #6B4E9B; --plum-50: #F1ECF7; --cocoa: #5E3A26; --cocoa-50: #F5EDE7;
  --ink: #13303A; --slate: #56676D; --rule: #DCE3E3; --fog: #F5F7F7; --paper: #FFFFFF;
  --on-teal: #D6E8E6;
  --sans: 'Be Vietnam Pro', 'Segoe UI', system-ui, sans-serif;
  --serif: 'Literata', Georgia, serif;
  --section: 5rem;
  --shadow-soft: 0 1px 2px rgba(19,48,58,0.06), 0 14px 34px -18px rgba(19,48,58,0.28);
  --shadow-lift: 0 2px 4px rgba(19,48,58,0.06), 0 22px 44px -20px rgba(19,48,58,0.34);
}

/* ---------- base ---------- */
html, body, .stMarkdown, input, textarea { font-family: var(--sans); }
body { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
.block-container { max-width: 68rem; padding: 3rem 2rem 4rem; }
:where(.stMarkdown) :where(p, li) { font-size: 1.0625rem; line-height: 1.7; }
[data-testid="stHeading"] { margin: 0 !important; }
h1, h2, h3, h4 { font-family: var(--sans) !important; color: var(--ink) !important; }
h1 { font-weight: 800 !important; font-size: 2.5rem !important; letter-spacing: -0.035em; }
h2 { font-weight: 700 !important; font-size: 1.75rem !important; letter-spacing: -0.03em;
     line-height: 1.2 !important; padding: 0 !important; margin: var(--section) 0 1.25rem !important; }
h3 { font-size: 1.375rem !important; letter-spacing: -0.02em; }
h3, h4 { font-weight: 700 !important; }
a { color: var(--teal); text-underline-offset: 3px; text-decoration-thickness: 1px; }
::selection { background: var(--gold-100); color: var(--ink); }
.serif { font-family: var(--serif); }

/* ---------- header and menu ---------- */
header[data-testid="stHeader"] { background: rgba(255,255,255,0.86);
  backdrop-filter: saturate(1.4) blur(12px); -webkit-backdrop-filter: saturate(1.4) blur(12px);
  border-bottom: 1px solid rgba(220,227,227,0.9); }
[data-testid="stTopNavLink"] { border-radius: 999px !important; padding: 0.35rem 0.85rem !important;
  transition: background 0.15s ease; }
[data-testid="stTopNavLink"] span { font-size: 0.9rem !important; font-weight: 500; color: var(--slate) !important; }
[data-testid="stTopNavLink"]:hover { background: var(--teal-50) !important; }
[data-testid="stTopNavLink"]:hover span { color: var(--ink) !important; }
[data-testid="stTopNavLink"][aria-current="page"] { background: var(--teal-100) !important; }
[data-testid="stTopNavLink"][aria-current="page"] span { color: var(--teal) !important; font-weight: 700 !important; }
[data-testid="stTopNavLink"] [data-testid="stIconMaterial"] { color: inherit; opacity: 0.7; }
[data-testid="stHeaderLogo"], [data-testid="stLogo"] { height: 1.9rem !important; max-height: 1.9rem; }
[data-testid="stDecoration"] { display: none; }

/* Keyboard focus always shows, in gold */
a:focus-visible, button:focus-visible, summary:focus-visible, [tabindex]:focus-visible {
  outline: 3px solid var(--gold) !important; outline-offset: 2px; border-radius: 8px; }

/* ---------- panels, inputs, buttons ---------- */
[data-testid="stExpander"] details { border: 1px solid var(--rule); border-radius: 16px;
  background: var(--paper); transition: box-shadow 0.2s ease, border-color 0.2s ease; }
[data-testid="stExpander"] details:hover { border-color: #C9D4D4; }
[data-testid="stExpander"] details[open] { box-shadow: var(--shadow-soft); border-color: #C9D4D4; }
[data-testid="stExpander"] summary { padding: 1rem 1.25rem; }
[data-testid="stExpander"] summary p { font-size: 1.0625rem; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--rule) !important;
  border-radius: 16px !important; }
[data-testid="stMetric"] { border: 0 !important; border-radius: 16px !important;
  background: var(--teal-50); padding: 1.1rem 1.25rem !important; }
[data-testid="stMetricLabel"] p { color: var(--slate) !important; font-size: 0.875rem !important; }
[data-testid="stMetricValue"] { font-weight: 800; letter-spacing: -0.04em; color: var(--teal); }
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  border-radius: 10px !important; }
[data-testid="stWidgetLabel"] p { font-weight: 500; }
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primaryFormSubmit"], [data-testid="stBaseButton-secondaryFormSubmit"],
[data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a {
  border-radius: 999px !important; font-weight: 600 !important; padding: 0.65rem 1.4rem !important;
  min-height: 2.9rem; transition: background 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease; }
/* Gold means "do this". Only primary buttons use it. */
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {
  background: var(--gold) !important; border: 1px solid var(--gold-600) !important; color: var(--ink) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.45), 0 10px 22px -12px rgba(201,149,26,0.9); }
[data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover {
  background: #EDBD3F !important; transform: translateY(-1px); }
[data-testid="stBaseButton-primary"]:active, [data-testid="stBaseButton-primaryFormSubmit"]:active {
  transform: translateY(0); box-shadow: inset 0 1px 0 rgba(255,255,255,0.3); }
[data-testid="stBaseButton-secondary"], [data-testid="stDownloadButton"] button {
  border: 1.5px solid var(--ink) !important; background: transparent !important; color: var(--ink) !important; }
[data-testid="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover {
  background: var(--ink) !important; color: #FFFFFF !important; }
[data-testid="stCaptionContainer"] { color: var(--slate); }
[data-testid="stAlert"] { border-radius: 14px; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after {
  animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }

/* ---------- home: hero ---------- */
.st-key-hero { position: relative; overflow: hidden; border-radius: 28px;
  padding: 4rem 3.5rem 3.5rem;
  background:
    radial-gradient(60% 75% at 82% 42%, rgba(220,235,235,0.16), transparent 70%),
    linear-gradient(160deg, #11606A 0%, var(--teal) 45%, var(--teal-900) 100%); }
.home-title { font-weight: 800; font-size: clamp(2.5rem, 5.4vw, 3.75rem); line-height: 1.02;
  letter-spacing: -0.045em; color: #FFFFFF; margin: 0 0 1.25rem; text-wrap: balance; }
.home-lede { font-size: 1.1875rem; line-height: 1.6; color: var(--on-teal); max-width: 29rem;
  margin: 0 0 2rem; }
.st-key-hero [data-testid="stBaseButton-secondary"] { background: rgba(255,255,255,0.06) !important;
  border-color: rgba(255,255,255,0.55) !important; color: #FFFFFF !important; }
.st-key-hero [data-testid="stBaseButton-secondary"]:hover { background: #FFFFFF !important;
  color: var(--teal) !important; }
.home-art svg { width: 100%; height: auto; display: block; overflow: visible;
  filter: drop-shadow(0 18px 22px rgba(6,40,44,0.35)); }
/* One orchestrated moment: the six bubbles pop in, English last. */
.home-art .bub { transform-box: fill-box; transform-origin: center;
  animation: pop 0.55s cubic-bezier(.2,1.4,.4,1) both; }
.home-art .bub.b0 { animation-delay: 0.10s; } .home-art .bub.b1 { animation-delay: 0.22s; }
.home-art .bub.b3 { animation-delay: 0.34s; } .home-art .bub.b4 { animation-delay: 0.46s; }
.home-art .bub.b5 { animation-delay: 0.58s; } .home-art .bub.b2 { animation-delay: 0.78s; }
@keyframes pop { from { opacity: 0; transform: scale(0.6); } to { opacity: 1; transform: scale(1); } }
.facts { display: flex; flex-wrap: wrap; gap: 0.5rem 1.5rem; margin-top: 1.75rem; }
.facts span { color: var(--on-teal) !important; font-size: 0.9rem; display: inline-flex;
  align-items: center; gap: 0.5rem; }
.facts span::before { content: ""; width: 0.45rem; height: 0.45rem; border-radius: 50%;
  background: var(--gold); }

/* ---------- two mistakes ---------- */
.risks { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--rule);
  border-radius: 16px; overflow: hidden; background: var(--paper); }
.risk { padding: 2.25rem 2.25rem 2rem; }
.risk + .risk { border-left: 1px solid var(--rule); }
.risk.r1 { background: var(--berry-50); } .risk.r1 .risk-title { color: var(--berry); }
.risk.r2 { background: var(--teal-50); } .risk.r2 .risk-title { color: var(--teal); }
.risk-title { font-weight: 700; font-size: 1.375rem; letter-spacing: -0.025em; margin-bottom: 0.5rem; }
.risk p { margin: 0; color: #44555B; font-size: 1.0625rem; line-height: 1.6; max-width: 26rem; }
.risk-quote { grid-column: 1 / -1; border-top: 1px solid var(--rule); padding: 1.75rem 2.25rem;
  color: var(--ink); font-family: var(--serif); font-style: italic; font-size: 1.1875rem;
  line-height: 1.6; }
.pv-src { display: block; color: var(--slate); font-size: 0.8125rem; margin-top: 0.4rem;
  font-family: var(--sans); font-style: normal; }

/* ---------- big number ---------- */
.bigstat { display: grid; grid-template-columns: auto 1fr; gap: 3.5rem; align-items: center;
  border-radius: 28px; background: var(--gold-50); color: var(--ink); padding: 3rem 3.5rem;
  margin-top: var(--section); border: 1px solid #F3E4B4; }
.bigstat .t { font-size: 1.5rem; font-weight: 700; line-height: 1.35; letter-spacing: -0.025em;
  max-width: 30rem; text-wrap: balance; }
.bigstat .s { font-size: 0.875rem; color: var(--slate); margin-top: 1.25rem; }
.donut-wrap { position: relative; width: 220px; height: 220px; }
.donut-center { position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center; font-size: 2.9rem; font-weight: 800; color: var(--teal);
  letter-spacing: -0.05em; }
.legend { list-style: none; padding: 0; margin: 1.5rem 0 0; display: grid;
  grid-template-columns: 1fr 1fr; gap: 0.5rem 2.5rem; font-size: 0.9375rem; }
.legend li { display: flex; align-items: center; gap: 0.6rem; padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(19,48,58,0.08); }
.legend i { width: 0.7rem; height: 0.7rem; border-radius: 3px; flex: none; }
.legend b { margin-left: auto; font-weight: 600; font-variant-numeric: tabular-nums; }

/* ---------- how it works (a real sequence, so it is numbered) ---------- */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5rem; position: relative; }
.steps::before { content: ""; position: absolute; top: 1.4rem; left: 1.5rem;
  right: calc((100% - 5rem) / 3 - 1.4rem); border-top: 2px dashed #BFD8D8; z-index: 0; }
.step { position: relative; z-index: 1; }
.step-top { display: flex; }
.step .num { display: inline-flex; align-items: center; justify-content: center;
  width: 2.8rem; height: 2.8rem; border-radius: 50%; color: #FFFFFF; background: var(--teal);
  font-weight: 700; font-size: 1.125rem; box-shadow: 0 0 0 7px var(--paper); }
.step .icon { display: none; }
.step .title { font-weight: 700; font-size: 1.1875rem; letter-spacing: -0.02em;
  margin: 1.25rem 0 0.5rem; color: var(--ink); }
.step .text { color: #44555B; font-size: 1rem; line-height: 1.65; }

/* ---------- see it in action ---------- */
.preview { background: var(--paper); border: 1px solid var(--rule); border-radius: 16px;
  padding: 1.75rem; box-shadow: var(--shadow-lift); }
.pv-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem; }
.pv-head span { color: var(--slate); font-size: 0.8125rem; }
.pv-key { font-size: 0.8125rem; color: var(--slate); margin-bottom: 0.6rem; }
.pv-key i { display: inline-block; width: 0.65rem; height: 0.65rem; border-radius: 2px;
  margin: 0 0.3rem -0.05rem 0.75rem; }
.pv-key i:first-child { margin-left: 0; }
.pv-row { display: grid; grid-template-columns: 5.6rem 1fr 2.6rem; align-items: center; gap: 0.6rem; margin: 0.22rem 0; }
.pv-lang { font-size: 0.875rem; font-weight: 600; }
.pv-bar { background: var(--fog); border-radius: 999px; height: 0.6rem; overflow: hidden; }
.pv-bar span { display: block; height: 100%; border-radius: 999px; }
.pv-num { font-size: 0.8125rem; color: var(--slate); text-align: right; font-variant-numeric: tabular-nums; }
.pv-title { font-weight: 700; margin: 1.1rem 0 0.35rem; }
.preview ul { margin: 0; padding-left: 1.1rem; font-size: 0.9375rem; line-height: 1.55; }
.preview li { margin-bottom: 0.6rem; font-size: 0.9375rem; line-height: 1.55; }
.side-lede { font-family: var(--serif); font-size: 1.5rem; font-weight: 400; line-height: 1.4;
  color: var(--ink); letter-spacing: -0.01em; text-wrap: pretty; }
.side-text { color: #44555B; line-height: 1.7; max-width: 28rem; }

.cited { margin-top: var(--section); padding: 1.75rem 0; border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule); }
.cited-label { color: var(--slate); font-size: 0.875rem; margin-bottom: 0.75rem; }
.cited-list { display: flex; flex-wrap: wrap; gap: 0.5rem 2.25rem; }
.cited-list span { font-family: var(--serif); font-style: italic; color: var(--ink); font-size: 1rem; }

/* ---------- why I built this ---------- */
.st-key-story { background: var(--berry-50); border-radius: 28px; padding: 3.5rem;
  margin-top: var(--section); border: 1px solid var(--berry-100); }
.st-key-story h2 { margin: 0 !important; color: var(--berry) !important;
  font-size: 1rem !important; letter-spacing: 0; font-weight: 700 !important; }
.quote p { font-family: var(--serif); font-size: clamp(1.4rem, 2.6vw, 2rem); line-height: 1.42;
  color: var(--ink); margin: 1rem 0 2rem; font-weight: 400; letter-spacing: -0.015em;
  max-width: 44rem; text-wrap: pretty; text-indent: -0.42em; }
.quote .who { display: flex; align-items: center; gap: 0.9rem; }
.quote .mono { width: 2.9rem; height: 2.9rem; border-radius: 50%; background: var(--berry);
  color: #FFFFFF; display: inline-flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 1rem; letter-spacing: 0.02em; flex: none; }
.quote .sign { color: var(--ink); font-weight: 700; }
.quote .role { color: #6B4C57; font-size: 0.9rem; }

/* ---------- language carousel ---------- */
.section-sub { color: var(--slate); margin: -0.5rem 0 1.5rem; max-width: 38rem; line-height: 1.6; }
.carousel { display: flex; gap: 1rem; overflow-x: auto; scroll-snap-type: x mandatory;
  padding: 0.5rem 0.5rem 1.5rem; margin: 0 -0.5rem; scrollbar-width: thin;
  scroll-padding-left: 0.5rem; }
.card { flex: 0 0 15.5rem; scroll-snap-align: start; border-radius: 18px; padding: 1.5rem;
  text-decoration: none !important; display: flex; flex-direction: column;
  border: 1px solid rgba(19,48,58,0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease; }
.card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lift); }
.card-top { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem; }
.card-tag { font-weight: 600; font-size: 0.875rem; }
.card-badge { background: rgba(255,255,255,0.85); border-radius: 999px; padding: 0.2rem 0.65rem;
  font-size: 0.75rem; white-space: nowrap; }
.card-autonym { font-size: 2.25rem; font-weight: 600; line-height: 1.15; text-align: left;
  letter-spacing: -0.02em; unicode-bidi: plaintext; }
.card-name { font-weight: 700; margin: 0.35rem 0 0.6rem; }
.card .card-name, .card .card-text, .card .card-badge { color: var(--ink) !important; }
.card-text { font-size: 0.9375rem; line-height: 1.55; opacity: 0.9; flex: 1; }
.card-link { font-size: 0.875rem; font-weight: 700; margin-top: 1.5rem;
  text-decoration: underline; text-underline-offset: 3px; }

/* ---------- built for ---------- */
.personas { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5rem; }
.persona { border-top: 3px solid var(--rule); padding-top: 1.5rem; }
.persona:nth-child(1) { border-color: var(--teal); }
.persona:nth-child(2) { border-color: var(--berry); }
.persona:nth-child(3) { border-color: var(--plum); }
.persona .icon { display: none; }
.persona .who { font-weight: 700; font-size: 1.25rem; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.persona p { margin: 0; color: #44555B; line-height: 1.65; }

/* ---------- FAQ ---------- */
.faq { border-top: 1px solid var(--rule); max-width: 50rem; }
.faq details { border-bottom: 1px solid var(--rule); }
.faq summary { cursor: pointer; font-weight: 600; font-size: 1.125rem; list-style: none;
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
  padding: 1.25rem 0; transition: color 0.15s ease; }
.faq summary:hover { color: var(--teal); }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: "+"; flex: none; width: 2rem; height: 2rem; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center; background: var(--teal-50);
  color: var(--teal); font-weight: 600; font-size: 1.25rem; transition: transform 0.2s ease, background 0.2s ease; }
.faq details[open] summary::after { transform: rotate(45deg); background: var(--teal-100); }
.faq details p { margin: 0 0 1.25rem; color: #44555B; max-width: 42rem; line-height: 1.7; }

/* ---------- closing call to action ---------- */
.st-key-cta { border-radius: 28px; padding: 3rem 3.5rem; margin-top: var(--section);
  background: radial-gradient(70% 120% at 100% 0%, rgba(229,177,46,0.16), transparent 60%), var(--ink); }
.cta-icon { display: none; }
.cta-title { color: #FFFFFF; font-size: 1.875rem; font-weight: 700; line-height: 1.2;
  letter-spacing: -0.03em; text-wrap: balance; }
.cta-text { color: #B9CCCC; margin-top: 0.6rem; }

/* ---------- announcement bar ---------- */
.ticker { overflow: hidden; color: var(--teal); margin: -1rem 0 1.75rem; padding: 0.55rem 0;
  font-size: 0.875rem; font-weight: 500;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent); }
.ticker-track { display: inline-flex; gap: 3rem; white-space: nowrap; padding-right: 3rem;
  animation: ticker 48s linear infinite; }
.ticker:hover .ticker-track { animation-play-state: paused; }
.ticker-track span::before { content: ""; display: inline-block; width: 0.4rem; height: 0.4rem;
  border-radius: 50%; background: var(--gold); margin: 0 0.75rem 0.12rem 0; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .ticker-track { animation: none; } }

/* ---------- page headers on every tab ---------- */
.page-head { border-radius: 28px; padding: 3rem 3.5rem; margin-bottom: 2.5rem;
  display: grid; grid-template-columns: 1fr 11rem; gap: 2.5rem; align-items: center;
  background:
    radial-gradient(55% 90% at 88% 50%, rgba(220,235,235,0.14), transparent 70%),
    linear-gradient(160deg, #11606A 0%, var(--teal) 50%, var(--teal-900) 100%); }
.ph-art svg { width: 100%; height: auto; display: block; filter: drop-shadow(0 12px 16px rgba(6,40,44,0.3)); }
.ph-chips { display: flex; flex-wrap: wrap; gap: 0.5rem 1.5rem; margin-top: 1.5rem; }
.ph-chips span { color: var(--on-teal); font-size: 0.9rem; display: inline-flex; align-items: center; gap: 0.5rem; }
.ph-chips span::before { content: ""; width: 0.45rem; height: 0.45rem; border-radius: 50%; background: var(--gold); }
.page-head .ph-title { font-size: 2.75rem; font-weight: 800; letter-spacing: -0.04em;
  line-height: 1.05; color: #FFFFFF; }
.page-head .ph-lede { font-size: 1.125rem; color: var(--on-teal); max-width: 36rem;
  margin: 0.85rem 0 0; line-height: 1.6; }

/* New Assessment steps */
.chunk { display: flex; align-items: center; gap: 0.85rem; font-weight: 700; font-size: 1.375rem;
  letter-spacing: -0.02em; margin: 3rem 0 0.5rem; color: var(--ink); }
.chunk .n { display: inline-flex; align-items: center; justify-content: center; width: 2.2rem;
  height: 2.2rem; border-radius: 50%; color: #FFFFFF; font-size: 1rem; flex: none; }
.chunk-hint { color: var(--slate); font-size: 0.9375rem; margin: 0 0 1.25rem 3.05rem; max-width: 40rem; line-height: 1.6; }

/* Knowledge Library */
.lib-head { display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; }
.lib-head .autonym { font-size: 3rem; font-weight: 700; line-height: 1.1; letter-spacing: -0.03em; }
.lib-head .english { font-size: 1.25rem; font-weight: 600; color: var(--slate); }
.lib-share { color: var(--slate); font-size: 0.875rem; margin: 0.4rem 0 1.25rem; }
.lib-summary { font-family: var(--serif); font-size: 1.25rem; line-height: 1.6; margin: 0 0 1.25rem;
  color: var(--ink); max-width: 44rem; }

/* About page */
.hello { display: grid; grid-template-columns: 12rem 1fr; gap: 3rem; align-items: start;
  margin: 0.5rem 0 1rem; }
.hello-mark { position: relative; }
.hello-mark svg { width: 100%; height: auto; display: block; }
.hello h2 { margin: 0 0 1rem !important; }
.hello .hi { font-family: var(--serif); font-size: 1.5rem; line-height: 1.45; color: var(--ink);
  margin: 0 0 1rem; max-width: 38rem; }
.hello p { color: #44555B; line-height: 1.75; max-width: 38rem; margin: 0 0 1rem; }
.hello .sig { color: var(--berry); font-weight: 700; margin-top: 1.25rem; }
.duo { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem; }
.duo > div { border-radius: 16px; padding: 2rem; }
.duo .t { font-weight: 700; font-size: 1.25rem; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.duo p { margin: 0; color: #44555B; line-height: 1.65; }
.lists { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; }
.lists h3 { margin: 0 0 0.75rem !important; font-size: 1.1875rem !important; }
.lists ul { margin: 0; padding: 0; list-style: none; }
.lists li { position: relative; padding: 0.7rem 0 0.7rem 1.5rem; border-top: 1px solid var(--rule);
  color: #44555B; line-height: 1.55; }
.lists li::before { content: ""; position: absolute; left: 0.1rem; top: 1.25rem; width: 0.5rem;
  height: 0.5rem; border-radius: 50%; background: var(--teal); }
.lists .warn li::before { background: var(--berry); }
.stack { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.25rem 0 1.25rem; }
.stack span { background: var(--fog); border: 1px solid var(--rule); border-radius: 999px;
  padding: 0.3rem 0.85rem; font-size: 0.875rem; font-weight: 500; }

/* Family Interview */
.q-title { display: flex; align-items: center; gap: 0.75rem; font-weight: 700; font-size: 1.1875rem; margin-bottom: 0.75rem; }
.q-block ol { margin: 0; padding-inline-start: 1.5rem; }
.q-block li { margin-bottom: 0.65rem; line-height: 1.6; }
.q-block li::marker { color: var(--teal); font-weight: 700; }
.q-en { color: var(--slate); font-size: 0.875rem; text-align: left; }

/* Icons and empty states */
.icon { display: block; }
.risk .icon, .duo .icon { margin-bottom: 1rem; }
.icon-head { display: flex; align-items: center; gap: 0.75rem; margin-top: var(--section); }
.icon-head h2 { margin: 0 !important; }
.empty { text-align: center; padding: 4rem 1.5rem; border: 2px dashed var(--rule);
  border-radius: 28px; margin-top: 1rem; background: var(--fog); }
.empty .icon { margin: 0 auto 1rem; }
.empty-t { font-weight: 700; font-size: 1.375rem; letter-spacing: -0.02em; }
.empty p { color: var(--slate); max-width: 26rem; margin: 0.5rem auto 0; }

/* Vietnamese tones */
.tones { display: flex; flex-wrap: wrap; gap: 0.5rem 2rem; margin: 0.25rem 0 0.5rem; }
.tone .syl { display: block; font-size: 2rem; font-weight: 600; color: var(--teal); line-height: 1.2; }
.tone .gloss { display: block; font-size: 0.8125rem; color: var(--slate); }

/* Hears / speaks key */
.key { color: var(--slate); font-size: 0.875rem; }
.key .dot { display: inline-block; width: 0.7rem; height: 0.7rem; border-radius: 2px; margin: 0 0.3rem -0.05rem 0; }

/* Things to consider */
.tip-group { font-weight: 700; margin: 1.1rem 0 0.25rem; color: var(--teal); }
.tip-source { color: var(--slate); font-size: 0.8125rem; margin: -0.35rem 0 0.5rem 1.6rem; }

/* ---------- footer ---------- */
.footer { margin-top: 6rem; padding: 3rem 0 0; border-top: 1px solid var(--rule);
  display: grid; grid-template-columns: 1.7fr 1fr 1fr; gap: 3rem; }
.footer .brand { font-weight: 800; font-size: 1.375rem; letter-spacing: -0.03em; color: var(--ink);
  display: flex; align-items: center; gap: 0.6rem; }
.footer .mark { width: 1.5rem; height: 1rem; flex: none; border-radius: 2px;
  background: linear-gradient(var(--teal) 0 40%, transparent 40% 60%, var(--gold) 60% 100%); }
.footer p { color: var(--slate); font-size: 0.9375rem; margin: 0.9rem 0 0; line-height: 1.65; max-width: 25rem; }
.footer .col-title { font-weight: 700; font-size: 0.875rem; color: var(--ink); margin-bottom: 0.75rem; }
.footer a { display: block; color: var(--slate) !important; text-decoration: none; font-size: 0.9375rem;
  padding: 0.3rem 0; transition: color 0.15s ease; }
.footer a:hover { color: var(--teal) !important; }
.footer-base { grid-column: 1 / -1; display: flex; justify-content: space-between; flex-wrap: wrap;
  gap: 0.5rem 2rem; border-top: 1px solid var(--rule); margin-top: 0.5rem; padding-top: 1.5rem;
  color: var(--slate); font-size: 0.8125rem; }

/* ---------- Sound Explorer ---------- */
.snd-sum { display: flex; align-items: center; gap: 2rem; margin: 1.5rem 0 2rem;
  padding: 1.75rem 2rem; border-radius: 16px; background: var(--berry-50); border: 1px solid var(--berry-100); }
.snd-big { font-size: 4rem; font-weight: 800; letter-spacing: -0.05em; line-height: 0.9;
  color: var(--berry); display: flex; flex-direction: column; }
.snd-big span { font-size: 0.875rem; font-weight: 600; letter-spacing: 0; color: var(--slate);
  margin-top: 0.5rem; }
.snd-sum-t { font-size: 1.375rem; font-weight: 700; letter-spacing: -0.02em; line-height: 1.35; }
.snd-key { display: flex; flex-wrap: wrap; gap: 0.5rem 1.5rem; margin-top: 0.75rem;
  font-size: 0.875rem; color: var(--slate); }
.snd-key span { display: inline-flex; align-items: center; gap: 0.5rem; }
.snd-key i { width: 1rem; height: 1rem; border-radius: 4px; }
.snd-key .k-miss { background: var(--berry); }
.snd-key .k-both { background: var(--paper); border: 1.5px solid var(--rule); }
.snd-group { display: grid; grid-template-columns: 9rem 1fr; gap: 1rem; align-items: start;
  padding: 1rem 0; border-top: 1px solid var(--rule); }
.snd-group:last-child { border-bottom: 1px solid var(--rule); }
.snd-label { font-weight: 700; font-size: 0.9375rem; padding-top: 0.6rem; }
.snd-row { display: flex; flex-wrap: wrap; gap: 0.6rem; }
.snd { width: 5.5rem; height: 5.5rem; border-radius: 14px; background: var(--paper);
  border: 1.5px solid var(--rule); display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 0.15rem; transition: transform 0.15s ease, box-shadow 0.15s ease; }
.snd:hover { transform: translateY(-2px); box-shadow: var(--shadow-soft); }
.snd .ipa { font-size: 1.75rem; font-weight: 600; line-height: 1.1; color: var(--ink); }
.snd .w { font-size: 0.8125rem; color: var(--slate); }
.snd .w b { color: var(--ink); font-weight: 700; text-decoration: underline;
  text-decoration-color: var(--gold); text-decoration-thickness: 2px; text-underline-offset: 3px; }
.snd.miss { background: var(--berry); border-color: var(--berry); }
.snd.miss .ipa { color: #FFFFFF; }
.snd.miss .w { color: #F6D3E0; }
.snd.miss .w b { color: #FFFFFF; }
.snd-grid.compact { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.45rem; }
.snd-grid.compact .snd { width: auto; height: auto; aspect-ratio: 1; border-radius: 12px; }
.snd-grid.compact .ipa { font-size: 1.25rem; }
.snd-grid.compact .w { font-size: 0.6875rem; }
.snd-extras { display: grid; grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); gap: 1rem; }
.snd-extra { border-radius: 16px; padding: 1.75rem; background: var(--teal-50); }
.snd-extra .t { font-weight: 700; font-size: 1.1875rem; letter-spacing: -0.02em; color: var(--teal); }
.snd-extra .lede { font-family: var(--serif); font-size: 1.125rem; margin: 0.4rem 0 1rem; color: var(--ink); }
.snd-extra p { color: #44555B; line-height: 1.6; margin: 0; }
.snd-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
.snd-chips span { min-width: 3rem; padding: 0.45rem 0.75rem; border-radius: 12px; background: var(--paper);
  border: 1.5px solid var(--teal-100); text-align: center; font-size: 1.375rem; font-weight: 600; color: var(--teal); }
.snd-how { margin-top: 2.5rem; padding: 1.75rem 2rem; border-left: 4px solid var(--gold);
  background: var(--gold-50); border-radius: 0 16px 16px 0; }
.snd-how .t { font-weight: 700; font-size: 1.125rem; margin-bottom: 0.4rem; }
.snd-how p { margin: 0; color: #44555B; line-height: 1.7; max-width: 46rem; }
.st-key-snd_teaser { margin-top: var(--section); padding: 3rem 3.5rem; border-radius: 28px;
  background: var(--fog); border: 1px solid var(--rule); }
.snd-teaser-t { font-size: 1.875rem; font-weight: 800; letter-spacing: -0.035em; line-height: 1.15;
  text-wrap: balance; }
.snd-teaser-p { color: #44555B; line-height: 1.7; margin: 0.75rem 0 1.5rem; max-width: 28rem; }

/* ---------- myths ---------- */
.myths { border-top: 2px solid var(--ink); }
.myth-head { display: grid; grid-template-columns: 1fr 1.25fr; gap: 3rem; padding: 0.75rem 0;
  font-size: 0.875rem; font-weight: 700; color: var(--slate); border-bottom: 1px solid var(--rule); }
.myth { display: grid; grid-template-columns: 1fr 1.25fr; gap: 3rem; padding: 1.75rem 0;
  border-bottom: 1px solid var(--rule); }
.m-left { display: flex; gap: 1rem; align-items: flex-start; }
.m-n { flex: none; width: 2rem; height: 2rem; border-radius: 50%; background: var(--berry-50);
  color: var(--berry); font-weight: 700; font-size: 0.9375rem; display: inline-flex;
  align-items: center; justify-content: center; }
.m-myth { margin: 0; font-size: 1.1875rem; font-weight: 600; line-height: 1.4; letter-spacing: -0.015em;
  color: var(--ink); text-decoration: line-through; text-decoration-color: rgba(179,32,90,0.55);
  text-decoration-thickness: 2px; }
.m-fact { margin: 0; font-family: var(--serif); font-size: 1.125rem; line-height: 1.6; color: var(--ink); }
.m-src { display: inline-block; margin-top: 0.6rem; font-size: 0.8125rem; font-weight: 600; color: var(--teal);
  background: var(--teal-50); border-radius: 999px; padding: 0.2rem 0.7rem; }

/* ---------- tone charts ---------- */
.tone-intro { font-family: var(--serif); font-size: 1.1875rem; margin: 0.25rem 0 1rem; color: var(--ink); }
.tone-chart { display: grid; grid-template-columns: repeat(var(--n, 4), minmax(0, 1fr)); gap: 0.75rem; max-width: calc(var(--n, 4) * 11rem); }
.tone-how { font-size: 0.875rem; color: var(--slate); margin: -0.5rem 0 1rem; }
.tone-cell { margin: 0; background: var(--paper); border: 1px solid var(--rule); border-radius: 16px;
  padding: 0.9rem 0.9rem 1rem; }
.tone-svg svg { width: 100%; height: auto; display: block; }
.tone-cell figcaption { display: flex; flex-direction: column; align-items: flex-start; margin-top: 0.5rem; }
.tone-w { font-size: 1.75rem; font-weight: 700; line-height: 1.15; letter-spacing: -0.01em; }
.tone-syl { font-size: 0.9375rem; font-weight: 600; color: var(--ink); }
.tone-m { font-family: var(--serif); font-style: italic; color: var(--ink); font-size: 1rem; }
.tone-l { margin-top: 0.5rem; font-size: 0.8125rem; font-weight: 700; color: var(--ink); }
.tone-n { font-size: 0.8125rem; color: var(--slate); }
.tone-key { display: none; }
.snd-soon { display: flex; gap: 1rem; align-items: center; margin: 1.5rem 0 2rem; padding: 1.25rem 1.5rem;
  border-radius: 16px; background: var(--fog); border: 1px dashed #C9D4D4; color: #44555B; line-height: 1.55; }
.snd-soon b { color: var(--ink); }
.snd-soon .icon { flex: none; }

/* ---------- Arabic diglossia ---------- */
.digl { display: grid; grid-template-columns: 1fr 13rem 1fr; gap: 0; align-items: stretch; margin: 0.5rem 0 0.75rem; }
.digl-side { border-radius: 18px; padding: 1.75rem; }
.digl-side.home { background: var(--plum-50); }
.digl-side.school { background: var(--teal-50); }
.digl-side .t { font-weight: 800; font-size: 1.375rem; letter-spacing: -0.025em; margin: 0.75rem 0 0.4rem; }
.digl-side.home .t { color: var(--plum); } .digl-side.school .t { color: var(--teal); }
.digl-side p { color: #44555B; line-height: 1.6; margin: 0 0 1rem; }
.digl-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.digl-tags span { background: rgba(255,255,255,0.8); border-radius: 999px; padding: 0.2rem 0.7rem;
  font-size: 0.8125rem; font-weight: 600; }
.digl-mid { display: flex; flex-direction: column; justify-content: center; align-items: center;
  padding: 0 1rem; text-align: center; }
.digl-arrow { width: 100%; height: 2px; background: var(--gold); position: relative; margin-bottom: 1rem; }
.digl-arrow::before, .digl-arrow::after { content: ""; position: absolute; top: -5px; border: 6px solid transparent; }
.digl-arrow::before { left: -2px; border-right-color: var(--gold); border-left: 0; }
.digl-arrow::after { right: -2px; border-left-color: var(--gold); border-right: 0; }
.digl-mid p { font-family: var(--serif); font-style: italic; font-size: 0.9375rem; line-height: 1.5;
  color: var(--ink); margin: 0; }

/* ---------- References ---------- */
.std { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 2.5rem; }
.std > div { border-top: 3px solid var(--teal); padding-top: 1.25rem; }
.std > div:nth-child(2) { border-color: var(--gold); }
.std > div:nth-child(3) { border-color: var(--berry); }
.std .n { font-family: var(--serif); font-size: 2.25rem; line-height: 1; color: var(--gold-600); }
.std .t { font-weight: 700; font-size: 1.125rem; letter-spacing: -0.015em; margin: 0 0 0.35rem; }
.std p { margin: 0; color: #44555B; line-height: 1.6; }
.ref-count { color: var(--slate); font-size: 0.875rem; margin: 0.75rem 0 0.5rem; }
.refs { list-style: none; counter-reset: ref; margin: 0; padding: 0; border-top: 1px solid var(--rule); }
.refs li { counter-increment: ref; position: relative; padding: 1.1rem 0 1.1rem 3rem;
  border-bottom: 1px solid var(--rule); }
.refs li::before { content: counter(ref); position: absolute; left: 0; top: 1.15rem; width: 2rem;
  font-family: var(--serif); font-size: 1rem; color: var(--slate); text-align: right; }
.refs li p { margin: 0; font-family: var(--serif); font-size: 1rem !important; line-height: 1.6;
  padding-left: 1.5rem; text-indent: -1.5rem; overflow-wrap: anywhere; }
.refs li a { color: var(--teal); }
.ref-tags { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.ref-tags span { font-size: 0.75rem; font-weight: 600; color: var(--teal); background: var(--teal-50);
  border-radius: 999px; padding: 0.15rem 0.6rem; }
[data-testid="stCode"] pre, [data-testid="stCodeBlock"] pre { border-radius: 14px !important; }

/* top menu dropdowns */
[data-testid="stTopNavSection"] { border-radius: 999px !important; }
[data-testid="stTopNavSection"] span { font-size: 0.9rem !important; font-weight: 500; color: var(--slate); }
[data-testid="stTopNavSection"]:hover { background: var(--teal-50) !important; }

/* ---------- waffle ---------- */
.waffle { width: 240px; flex: none; }
.waffle svg { width: 100%; height: auto; display: block; }
.big-n { font-size: 4.5rem; font-weight: 800; letter-spacing: -0.06em; line-height: 0.9;
  color: var(--teal); margin-bottom: 0.5rem; }

/* ---------- fun fact ---------- */
.st-key-factbox { margin-top: 1.5rem; padding: 1.75rem 2.5rem; border-radius: 28px;
  border: 1px solid var(--rule); background:
  radial-gradient(40% 120% at 0% 50%, var(--teal-50), transparent 70%), var(--paper); }
.fact-glyph { font-family: var(--serif); font-size: 4.5rem; line-height: 1; color: var(--berry);
  text-align: center; letter-spacing: -0.03em; overflow-wrap: anywhere; }
.fact-text { font-family: var(--serif); font-size: 1.375rem !important; line-height: 1.45;
  color: var(--ink); margin: 0 0 0.6rem; text-wrap: pretty; }
.fact-src { font-size: 0.8125rem; font-weight: 600; color: var(--teal); background: var(--teal-50);
  border-radius: 999px; padding: 0.2rem 0.7rem; }
.fact-n { margin-left: 0.75rem; font-size: 0.8125rem; color: var(--slate); font-variant-numeric: tabular-nums; }
.st-key-factbox [data-testid="stBaseButton-secondary"] { border-width: 1px !important; min-height: 2.4rem;
  padding: 0.4rem 1rem !important; font-size: 0.875rem; margin-top: 0.75rem; }

/* ---------- greeting on language cards ---------- */
.card-hi { font-size: 0.875rem; margin-top: 1rem; padding-top: 0.75rem;
  border-top: 1px dashed rgba(19,48,58,0.18); color: var(--slate) !important; }
.card-hi b { font-size: 1.125rem; color: var(--ink) !important; font-weight: 700; }
.card-hi span { color: var(--slate) !important; font-style: italic; }
.card-hi + .card-link { margin-top: 0.75rem; }

/* ---------- consonant matrix ---------- */
.matrix-wrap { overflow-x: auto; margin: 0 -0.25rem; padding: 0.25rem; }
.matrix { border-collapse: separate; border-spacing: 4px; font-size: 0.875rem; }
.matrix th { font-weight: 600; color: var(--ink); white-space: nowrap; }
.matrix thead th span { display: block; font-size: 1.0625rem; font-weight: 600; text-align: center; min-width: 1.6rem; }
.matrix tbody th { text-align: left; padding-right: 0.75rem; }
.matrix tbody th small { margin-left: 0.4rem; color: var(--slate); font-weight: 500; }
.matrix td { width: 1.6rem; height: 1.6rem; border-radius: 6px; background: var(--fog); }
.matrix td.x { background: var(--berry); }
.matrix tr:hover td { outline: 1px solid rgba(19,48,58,0.08); }
.matrix.has-pick tr:not(.on) td.x { background: var(--berry-100); }
.matrix tr.on th { color: var(--berry); }
.matrix .cnt-row th { color: var(--slate); font-weight: 500; }
.matrix td.cnt { background: transparent; text-align: center; font-weight: 700; color: var(--berry);
  font-variant-numeric: tabular-nums; }
.fact { display: flex; gap: 1rem; align-items: flex-start; margin-top: 1.25rem; padding: 1.25rem 1.5rem;
  border-radius: 16px; background: var(--gold-50); }
.fact .icon { flex: none; }
.fact p { margin: 0; line-height: 1.65; color: var(--ink); }

/* ---------- reading progress (browsers that support scroll timelines) ---------- */
@supports (animation-timeline: scroll()) {
  body::after { content: ""; position: fixed; top: 0; left: 0; right: 0; height: 3px; z-index: 999999;
    background: linear-gradient(90deg, var(--teal), var(--gold)); transform-origin: 0 50%;
    transform: scaleX(0); animation: read-progress linear both; animation-timeline: scroll(root); }
  @keyframes read-progress { to { transform: scaleX(1); } }
}

/* ---------- printing: clean pages for case files ---------- */
@media print {
  header[data-testid="stHeader"], .ticker, .footer, .st-key-cta, .st-key-snd_teaser,
  .st-key-factbox, [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"],
  .carousel, .home-art, .ph-art { display: none !important; }
  .page-head, .st-key-hero { background: none !important; padding: 0 !important; }
  .page-head .ph-title, .home-title { color: var(--ink) !important; }
  .page-head .ph-lede, .home-lede, .ph-chips span { color: var(--slate) !important; }
  .snd.miss, .matrix td.x { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .block-container { padding: 0 !important; max-width: none !important; }
}

/* ---------- mouth map ---------- */
.mm { margin: 0.5rem 0 1rem; padding: 2rem 1.5rem 1.25rem; border-radius: 22px; background: var(--fog);
  border: 1px solid var(--rule); }
.mm-row { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 0.4rem; }
.mm-col { display: flex; flex-wrap: wrap; justify-content: center; align-content: flex-end; gap: 0.3rem; }
.mm-t { display: inline-flex; align-items: center; justify-content: center; min-width: 2.3rem; height: 2.3rem;
  padding: 0 0.3rem; border-radius: 10px; background: var(--paper); border: 1.5px solid var(--rule);
  font-size: 1.125rem; font-weight: 600; color: var(--ink); }
.mm-t.miss { background: var(--berry); border-color: var(--berry); color: #FFFFFF; }
.mm-band { position: relative; height: 92px; margin: 0.75rem 0 0.5rem; }
.mm-band svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.mm-dot { position: absolute; width: 14px; height: 14px; margin: -7px 0 0 -7px; border-radius: 50%;
  background: var(--paper); border: 2.5px solid var(--ink); }
.mm-dot.hit { background: var(--berry); border-color: var(--berry); box-shadow: 0 0 0 5px var(--berry-100); }
.mm-lab { text-align: center; font-size: 0.8125rem; font-weight: 600; color: var(--ink); line-height: 1.3; }
.mm-ends { display: flex; justify-content: space-between; margin-top: 0.9rem; padding-top: 0.75rem;
  border-top: 1px dashed #C9D4D4; font-size: 0.8125rem; color: var(--slate); }
.mm-ends span:first-child::before { content: "\2190  "; }
.mm-ends span:last-child::after { content: "  \2192"; }

/* ---------- development timeline ---------- */
.tl { position: relative; height: 25rem; margin: 0.5rem 0 0.5rem; }
.tl-axis { position: absolute; left: 0; right: 0; top: 50%; height: 4px; margin-top: -2px; border-radius: 4px;
  background: linear-gradient(90deg, var(--teal-100), var(--teal)); }
.tl-ticks span { position: absolute; top: 50%; transform: translate(-50%, 0.9rem); font-size: 0.8125rem;
  font-weight: 600; color: var(--slate); white-space: nowrap; }
.tl-ticks span::before { content: ""; position: absolute; left: 50%; top: -1.15rem; width: 2px; height: 0.6rem;
  background: var(--teal); margin-left: -1px; }
.tl-item { position: absolute; left: var(--x); top: 50%; width: var(--w); }
.tl-mark { position: absolute; left: 0; top: -9px; height: 18px; width: calc(100% + 18px);
  margin-left: -9px; border-radius: 999px; background: var(--c); box-shadow: 0 0 0 4px var(--paper); }
.tl-card { position: absolute; left: -1.25rem; width: 11.25rem; padding: 0.85rem 1rem; border-radius: 14px;
  background: var(--paper); border: 1px solid var(--rule); border-top: 4px solid var(--c);
  box-shadow: var(--shadow-soft); }
.tl-item.up .tl-card { bottom: 1.6rem; }
.tl-item.down .tl-card { top: 2.6rem; }
.tl-item.up::before, .tl-item.down::before { content: ""; position: absolute; left: -1px; width: 2px;
  background: var(--c); opacity: 0.5; }
.tl-item.up::before { bottom: 9px; height: 0.9rem; }
.tl-item.down::before { top: 9px; height: 1.7rem; }
.tl-card b { display: block; color: var(--c); font-size: 0.9375rem; }
.tl-age { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.03em; color: var(--ink); }
.tl-card p { margin: 0.25rem 0 0.35rem; font-size: 0.875rem !important; line-height: 1.45; color: #44555B; }
.tl-src { font-size: 0.75rem; color: var(--slate); font-style: italic; }
.tl-item:last-child .tl-card { left: auto; right: -1.5rem; }

/* ---------- tools grid ---------- */
.tools { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.tool { display: block; border-radius: 20px; overflow: hidden; border: 1px solid var(--rule);
  background: var(--paper); text-decoration: none !important; color: var(--ink) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease; }
.tool:hover { transform: translateY(-3px); box-shadow: var(--shadow-lift); }
.tool-art { background: linear-gradient(160deg, #11606A, var(--teal) 55%, var(--teal-900));
  padding: 1rem 2.5rem 0.75rem; }
.tool-art svg { display: block; width: 100%; max-height: 7.5rem; filter: drop-shadow(0 8px 10px rgba(6,40,44,0.3)); }
.tool-t { font-weight: 700; font-size: 1.125rem; letter-spacing: -0.02em; padding: 1.1rem 1.25rem 0; }
.tool p { margin: 0.3rem 0 0; padding: 0 1.25rem 1.25rem; color: #44555B; font-size: 0.9375rem !important; line-height: 1.5; }

/* ---------- sounds to watch (cases) ---------- */
.stw { margin: 1rem 0 0.5rem; padding: 1.25rem 1.4rem; border-radius: 16px; background: var(--berry-50);
  border: 1px solid var(--berry-100); }
.stw-t { font-weight: 700; display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem; }
.stw-t span { background: var(--berry); color: #FFFFFF; border-radius: 999px; font-size: 0.8125rem;
  padding: 0.05rem 0.55rem; }
.stw-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.stw-chip { display: inline-flex; align-items: baseline; gap: 0.4rem; background: var(--paper);
  border: 1px solid var(--berry-100); border-radius: 10px; padding: 0.3rem 0.65rem; font-size: 0.875rem;
  color: var(--slate); }
.stw-chip b { font-size: 1.0625rem; color: var(--berry); }
.stw-src { margin-top: 0.75rem; font-size: 0.8125rem; color: var(--slate); }

.sc { display: grid; gap: 0.35rem; margin-top: 0.5rem; }
.sc-row { display: grid; grid-template-columns: 3.2rem 5.5rem 1fr 2rem; align-items: center; gap: 0.6rem; }
.sc-ipa { font-weight: 700; color: var(--berry); font-size: 1.0625rem; }
.sc-w { color: var(--slate); font-size: 0.875rem; }
.sc-bar { background: var(--fog); border-radius: 999px; height: 0.7rem; overflow: hidden; }
.sc-bar span { display: block; height: 100%; border-radius: 999px; background: var(--berry); }
.sc-n { text-align: right; font-weight: 700; font-variant-numeric: tabular-nums; }

/* ---------- word pairs ---------- */
.wps { display: grid; grid-template-columns: repeat(auto-fill, minmax(12.5rem, 1fr)); gap: 0.75rem; }
.wp { border-radius: 16px; border: 1px solid var(--rule); background: var(--paper); padding: 1rem 1.15rem; }
.wp-ipa { font-size: 1.5rem; font-weight: 700; color: var(--berry); margin-bottom: 0.35rem; }
.wp-pair { display: flex; align-items: baseline; gap: 0.5rem; padding: 0.35rem 0;
  border-top: 1px dashed var(--rule); font-family: var(--serif); font-size: 1.125rem; }
.wp-pair .a { font-weight: 600; color: var(--ink); }
.wp-pair .vs { font-family: var(--sans); font-size: 0.75rem; color: var(--slate); }
.wp-pair .b { color: #44555B; }

/* ---------- quick check ---------- */
.st-key-quizbox { padding: 1.75rem 2rem; border-radius: 22px; background: var(--plum-50);
  border: 1px solid #E3D9F0; }
.quiz-q { font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.75rem; }
.st-key-quizbox [data-testid="stButtonGroup"] button { font-size: 1.25rem !important; min-width: 3.5rem; }

/* ---------- finishing touches ---------- */
/* A fine paper grain on the colored panels, so they read as printed, not flat. */
.st-key-hero, .page-head, .st-key-cta, .st-key-story, .tool-art, .bigstat {
  position: relative; isolation: isolate; }
.page-head, .tool-art { overflow: hidden; }
.st-key-hero::after, .page-head::after, .st-key-cta::after, .st-key-story::after,
.tool-art::after, .bigstat::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; border-radius: inherit;
  opacity: 0.22; mix-blend-mode: soft-light; z-index: 1;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.9 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E"); }
.bigstat::after, .st-key-story::after { opacity: 0.12; mix-blend-mode: multiply; }

/* Greeting strip above the footer */
.hello-strip { margin: 6rem auto -3rem; max-width: 58rem; }
.hello-strip svg { width: 100%; height: auto; display: block; overflow: visible; }
.hello-strip .gb { transform-box: fill-box; transform-origin: center bottom; transition: transform 0.25s ease; }
.hello-strip .gb:hover { transform: translateY(-4px) rotate(-2deg); }

/* Links underline from the left on hover */
.stMarkdown a:not(.card):not(.tool) { text-decoration-color: rgba(14,79,87,0.35); transition: text-decoration-color 0.15s ease; }
.stMarkdown a:not(.card):not(.tool):hover { text-decoration-color: var(--gold); }

/* Quiet scrollbars */
* { scrollbar-width: thin; scrollbar-color: #C9D4D4 transparent; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #C9D4D4; border-radius: 999px; border: 3px solid transparent;
  background-clip: content-box; }
::-webkit-scrollbar-thumb:hover { background-color: var(--teal-600); }

/* ---------- interpreter steps ---------- */
.bid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; position: relative; }
.bid-card { border-radius: 18px; padding: 1.5rem; background: var(--paper); border: 1px solid var(--rule);
  border-top: 4px solid var(--teal); }
.bid-card:nth-child(2) { border-top-color: var(--gold); }
.bid-card:nth-child(3) { border-top-color: var(--berry); }
.bid-when { margin-top: 0.75rem; font-size: 0.8125rem; font-weight: 600; color: var(--slate); }
.bid-t { font-weight: 800; font-size: 1.25rem; letter-spacing: -0.02em; margin: 0.1rem 0 0.4rem; }
.bid-card p { margin: 0; color: #44555B; line-height: 1.6; }

/* ---------- About: by the numbers ---------- */
.numbers { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.75rem; margin: 2rem 0 1rem; }
.numbers > div { border-radius: 16px; background: var(--teal-50); padding: 1.1rem 1rem; }
.numbers .icon { margin-bottom: 0.6rem; }
.interp-art { max-width: 46rem; margin: 0.5rem auto 1.5rem; }
.interp-art svg { width: 100%; height: auto; display: block; overflow: visible; }
.numbers b { display: block; font-size: 2.25rem; font-weight: 800; letter-spacing: -0.05em; color: var(--teal); line-height: 1; }
.numbers span { display: block; margin-top: 0.4rem; font-size: 0.8125rem; color: var(--slate); }

/* ---------- people illustrations ---------- */
.persona-art { width: 7.5rem; margin: -0.5rem 0 0.75rem; }
.empty .empty-art { width: 8.5rem; margin: 0 auto 0.75rem; }
.empty .empty-art svg { width: 100%; height: auto; display: block; }
.persona-art svg, .story-art svg { width: 100%; height: auto; display: block; overflow: visible; }
.story-grid { display: grid; grid-template-columns: 1fr 19rem; gap: 2rem; align-items: center; }
.story-art { align-self: end; }

/* ---------- privacy notice ---------- */
.privacy { display: flex; gap: 1rem; align-items: flex-start; padding: 1.1rem 1.4rem; margin: -0.5rem 0 1rem;
  border-radius: 16px; background: var(--teal-50); border: 1px solid var(--teal-100); line-height: 1.6;
  color: #44555B; }
.privacy b { color: var(--ink); }
.privacy .icon { flex: none; }

/* ---------- review status ---------- */
.rv { border: 1px solid var(--rule); border-radius: 16px; overflow: hidden; max-width: 44rem; }
.rv-row { display: flex; justify-content: space-between; gap: 1rem; padding: 0.85rem 1.25rem;
  border-bottom: 1px solid var(--rule); }
.rv-row:last-child { border-bottom: 0; }
.rv-row b { font-size: 0.8125rem; border-radius: 999px; padding: 0.15rem 0.7rem; white-space: nowrap; }
.rv-row b.no { background: var(--gold-50); color: #8A6508; }
.rv-row b.yes { background: var(--teal-50); color: var(--teal); }

/* ---------- session phrases ---------- */
.ph-title { font-weight: 700; font-size: 1.125rem; margin: 1.5rem 0 0.75rem; }
.phs { display: grid; grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr)); gap: 0.6rem; }
.ph { border-radius: 14px; background: var(--teal-50); padding: 0.8rem 1rem; display: flex;
  flex-direction: column; gap: 0.15rem; }
.ph-v { font-weight: 700; font-size: 1.125rem; color: var(--teal); }
.ph-e { font-family: var(--serif); font-style: italic; color: #44555B; font-size: 0.9375rem; }

/* ---------- phones ---------- */
@media (max-width: 720px) {
  :root { --section: 3.5rem; }
  .block-container { padding: 2rem 1.1rem 3rem; }
  h2 { font-size: 1.5rem !important; }
  .st-key-hero { padding: 1.75rem 1.4rem 2.25rem; border-radius: 22px; }
  /* Art first, small, then the headline: the bubbles set the scene on a phone. */
  .st-key-hero [data-testid="stHorizontalBlock"] { flex-direction: column-reverse; gap: 0.5rem; }
  .st-key-hero [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] {
    flex-direction: column; gap: 0.75rem; }
  .home-art { max-width: 15rem; margin: 0 auto 0.5rem; }
  .home-title { font-size: 2.35rem; }
  .home-lede { font-size: 1.0625rem; margin-bottom: 1.5rem; }
  .facts { gap: 0.4rem 1.1rem; }
  .st-key-story { padding: 2rem 1.4rem; border-radius: 22px; }
  .st-key-cta { padding: 2rem 1.4rem; border-radius: 22px; }
  .cta-title { font-size: 1.5rem; }
  .steps, .risks, .duo, .personas, .lists, .hello { grid-template-columns: 1fr; }
  .steps { gap: 0; border-left: 2px dashed #BFD8D8; margin-left: 1.4rem; }
  .steps::before { display: none; }
  .step { padding: 0 0 2rem 2rem; }
  .step .num { position: absolute; left: -1.45rem; top: 0; width: 2.6rem; height: 2.6rem; }
  .step .title { margin-top: 0.4rem; }
  .personas { gap: 2rem; }
  .risk + .risk { border-left: 0; border-top: 1px solid var(--rule); }
  .risk, .risk-quote { padding: 1.5rem; }
  .risk-title { font-size: 1.25rem; }
  .bigstat { grid-template-columns: 1fr; gap: 1.5rem; padding: 2rem 1.4rem; justify-items: center;
    border-radius: 22px; text-align: left; }
  .bigstat .t { font-size: 1.25rem; }
  .donut-wrap { width: 190px; height: 190px; }
  .donut-wrap svg { width: 190px; height: 190px; }
  .donut-center { font-size: 2.4rem; }
  .legend { grid-template-columns: 1fr; width: 100%; }
  .preview { padding: 1.25rem; }
  .side-lede { font-size: 1.25rem; margin-top: 1rem; }
  .card { flex-basis: 78%; }
  .cited-list { flex-direction: column; gap: 0.45rem; }
  .snd-sum { flex-direction: column; align-items: flex-start; gap: 1rem; padding: 1.5rem; }
  .snd-big { flex-direction: row; align-items: baseline; gap: 0.6rem; font-size: 3.25rem; }
  .snd-sum-t { font-size: 1.1875rem; }
  .snd-group { grid-template-columns: 1fr; gap: 0.6rem; }
  .snd-label { padding-top: 0; }
  .snd-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; }
  .snd { width: auto; height: auto; aspect-ratio: 1; }
  .snd .ipa { font-size: 1.5rem; }
  .snd-grid.compact { grid-template-columns: repeat(6, 1fr); gap: 0.35rem; }
  .snd-grid.compact .w { display: none; }
  .st-key-snd_teaser { padding: 2rem 1.4rem; border-radius: 22px; }
  .snd-teaser-t { font-size: 1.5rem; }
  .myth-head { display: none; }
  .myth { grid-template-columns: 1fr; gap: 0.75rem; padding: 1.5rem 0; }
  .m-right { padding-left: 3rem; }
  .snd-how { padding: 1.5rem; }
  .waffle { width: 210px; margin: 0 auto; }
  .story-grid { grid-template-columns: 1fr; gap: 0.5rem; }
  .story-art { max-width: 12rem; margin: 0 auto; order: -1; }
  .persona-art { width: 6rem; }
  .bid { grid-template-columns: 1fr; }
  .numbers { grid-template-columns: repeat(3, 1fr); }
  .hello-strip { margin: 4rem -0.5rem -2rem; }
  .st-key-quizbox { padding: 1.25rem; }
  .wps { grid-template-columns: 1fr 1fr; }
  .mm { padding: 1.25rem 0.6rem 1rem; }
  .mm-row { gap: 0.15rem; }
  .mm-t { min-width: 1.6rem; height: 1.6rem; font-size: 0.8125rem; border-radius: 7px; padding: 0 0.15rem; }
  .mm-band { height: 64px; }
  .mm-lab { font-size: 0.625rem; }
  .tl { height: auto; padding-left: 1.5rem; border-left: 3px solid var(--teal-100); margin-left: 0.5rem; }
  .tl-axis, .tl-ticks { display: none; }
  .tl-item { position: relative; left: 0; top: 0; width: auto !important; margin-bottom: 1rem; }
  .tl-mark { left: -1.5rem; top: 1.1rem; width: 14px !important; height: 14px; margin-left: -8px; }
  .tl-item::before { display: none; }
  .tl-item.up .tl-card, .tl-item.down .tl-card, .tl-item:last-child .tl-card {
    position: relative; left: 0; right: auto; top: 0; bottom: auto; width: auto; }
  .tools { grid-template-columns: 1fr 1fr; gap: 0.6rem; }
  .tool-art { padding: 0.75rem 1rem 0.5rem; }
  .tool-t { font-size: 1rem; padding: 0.8rem 0.9rem 0; }
  .tool p { padding: 0 0.9rem 0.9rem; font-size: 0.8125rem !important; }
  .big-n { font-size: 3.5rem; }
  .st-key-factbox { padding: 1.5rem 1.4rem; border-radius: 22px; }
  .fact-glyph { font-size: 3.25rem; text-align: left; }
  .fact-text { font-size: 1.1875rem !important; }
  .tone-chart { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.5rem; max-width: none; }
  .tone-w { font-size: 1.5rem; }
  .digl { grid-template-columns: 1fr; gap: 0.75rem; }
  .digl-mid { padding: 0.25rem 1rem; }
  .digl-arrow { width: 2px; height: 2.5rem; margin: 0 0 0.75rem; }
  .digl-arrow::before { left: -5px; top: -2px; border: 6px solid transparent; border-bottom-color: var(--gold); border-top: 0; }
  .digl-arrow::after { left: -5px; right: auto; top: auto; bottom: -2px; border: 6px solid transparent; border-top-color: var(--gold); border-bottom: 0; }
  .std { grid-template-columns: 1fr; gap: 1.5rem; }
  .refs li { padding-left: 2.25rem; }
  .refs li::before { width: 1.5rem; }
  .quote p { font-size: 1.35rem; }
  .page-head { padding: 2rem 1.4rem; grid-template-columns: 1fr; border-radius: 22px; }
  .ph-art { display: none; }
  .page-head .ph-title { font-size: 2.1rem; }
  .chunk { margin-top: 2.25rem; font-size: 1.25rem; }
  .chunk-hint { margin-left: 0; }
  .lib-head .autonym { font-size: 2.4rem; }
  .hello-mark { max-width: 8rem; }
  .footer { grid-template-columns: 1fr 1fr; gap: 2rem 1.5rem; margin-top: 4rem; }
  .footer > div:first-child { grid-column: 1 / -1; }
  .footer-base { flex-direction: column; }
}
</style>
"""


LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 236 40" width="236" height="40">
<rect x="0" y="9" width="30" height="9" rx="2" fill="#0E4F57"/>
<rect x="0" y="22" width="22" height="9" rx="2" fill="#E5B12E"/>
<text x="40" y="28.5" font-family="Be Vietnam Pro, Segoe UI, Helvetica, Arial, sans-serif"
 font-size="21" font-weight="800" letter-spacing="-0.6" fill="#13303A">CLD Navigator</text></svg>"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)
    st.logo(LOGO_SVG, size="large")


TINTS = {"mint": TEAL, "butter": TEAL, "pink": TEAL, "sky": TEAL, "leaf": TEAL}


TICKER_ITEMS = [
    "Now covering the top 10 home languages of California English learners",
    "Russian, Farsi, Filipino, Punjabi, and Korean just joined the Knowledge Library",
    "The Sound Explorer compares English consonants with seven home languages",
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
    from art import GREETING_SVG
    st.markdown(f"""
<div class="hello-strip">{GREETING_SVG}</div>
<div class="footer">
  <div><div class="brand"><span class="mark"></span>CLD Navigator</div>
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
  <a href="sound-explorer" target="_self">Sound Explorer</a>
  <a href="references" target="_self">References</a>
  <a href="feedback" target="_self">Give feedback</a>
  <a href="about" target="_self">About and limitations</a>
  <a href="{REPO_URL}" target="_blank">Source code on GitHub</a></div>
  <div class="footer-base"><span>&copy; {date.today().year} Audrey Pham. Made in Fullerton, California.</span>
  <span>Teal is what a child hears. Gold is what a child speaks.</span></div>
</div>""", unsafe_allow_html=True)
