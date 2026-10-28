# views.py - one function per page of the website.

import re
from datetime import date

import pandas as pd
import streamlit as st

from common import (GOLD, PAGES, REPO_URL, TEAL, case_summary_text, chunk, exposure_key,
                    load_library, page_header, show_considerations, years_months)
from content import (GLOSSARY, INTERVIEW_LABELS, INTERVIEW_LANGUAGES, PHRASES, RTL_CODES,
                     interview_lines)
from art import (BUBBLES_SVG, CHILD_SVG, HELLO_SVG, PAGE_ART, PERSONA_SVGS, SESSION_SVG, donut,
                 icon, tone_chart, waffle)
from database import Case, Feedback, Language, Session
from report import (case_report_html, family_handout_html, interview_html,
                    project_summary_html, sound_sheet_html)
from rules import RULE_TABLE, check_percentages, get_considerations
from sample_data import load_demo_cases
from sounds import (ASHA_INTERPRETERS, GENESEE, PENA as PENA_FULL, PARADIS, PEARSON, PHAM_TIPTON, ALIASES, ENGLISH_CONSONANTS, FACTS, MANDARIN_READING, MILESTONES, PAIRS,
                    PENDING_SOURCES, PLACES, MYTHS, SCHIFF_FULL, SOUND_GAPS,
                    SOUND_PENDING, TONES, TOTAL_CONSONANTS, short_cite)

MAX_LANGUAGES = 4

# The six Vietnamese tones on the syllable "ma", with common meanings.
TONE_WORDS = [("ma", "ghost"), ("má", "mother"), ("mà", "but"),
              ("mả", "grave"), ("mã", "horse"), ("mạ", "rice seedling")]

# Each language's name in its own writing system.
RTL = ' dir="rtl"'
RTL_LANGS = {"Arabic", "Farsi"}
LANG_COLORS = ["#B3205A", "#0E4F57", "#B98A0E", "#6B4E9B", "#5E3A26",
               "#2E6B72", "#8A3B6E", "#3E7A4C", "#B0602A", "#3F5E9C"]

# Carousel: (one-word tag, badge) for each language, rhode-style.
CAROUSEL = {
    "Spanish": ("Consonants", "#1 in California",
                "Dropped final consonants in English can come from Spanish."),
    "Vietnamese": ("Tones", "#2 in California",
                   "Six tones and three dialects. Ask which one the family speaks."),
    "Mandarin": ("Tones first", "#3 in California",
                 "Children learn tones first and initial consonants last."),
    "Arabic": ("Diglossia", "#4 in California",
               "A spoken dialect at home, Standard Arabic at school."),
    "Cantonese": ("Early tones", "#5 in California",
                  "Tones and vowels are mastered by about age 2."),
    "Russian": ("Articles", "#6 in California",
                "No articles and no present-tense “to be” in Russian."),
    "Farsi": ("Four sounds", "#7 in California",
              "English /w/, /ð/, /θ/, and /ŋ/ don't occur in Farsi."),
    "Filipino": ("f and v", "#8 in California",
                 "No English /f/ or /v/, so vase may sound like base."),
    "Punjabi": ("Verb last", "#9 in California",
                "The verb comes at the end, and there are no articles."),
    "Korean": ("Word endings", "#10 in California",
               "Consonants at the ends of words are unreleased."),
}
# Card backgrounds and text colors (dark cards get white text).
TINT_BG = ["#F9E3EB", "#E2EEEE", "#F3EAE3", "#EEE8F5", "#EEF1F4",
           "#E4F0EF", "#F6E6F0", "#E6F1E8", "#F8EADF", "#E7ECF6"]
CARD_INK = ["#B3205A", "#0E4F57", "#5E3A26", "#6B4E9B", "#1C2B33",
            "#2E6B72", "#8A3B6E", "#3E7A4C", "#9A4F1E", "#3F5E9C"]
GREETINGS = {"Spanish": ("Hola", ""), "Vietnamese": ("Xin chào", ""),
             "Mandarin": ("你好", "nǐ hǎo"), "Arabic": ("مرحبا", "marḥaban"),
             "Cantonese": ("你好", "nei5 hou2"), "Russian": ("Здравствуйте", "zdravstvuyte"),
             "Farsi": ("سلام", "salâm"), "Filipino": ("Kumusta", ""),
             "Punjabi": ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "sat srī akāl"), "Korean": ("안녕하세요", "annyeonghaseyo")}
AUTONYMS = {"Spanish": "Español", "Vietnamese": "Tiếng Việt", "Mandarin": "普通话",
            "Arabic": "العربية", "Cantonese": "廣東話", "Russian": "Русский",
            "Farsi": "فارسی", "Filipino": "Wikang Filipino", "Punjabi": "ਪੰਜਾਬੀ", "Korean": "한국어"}

STEPS = [
    ("Look up the home language",
     "The Knowledge Library and Sound Explorer show what's typical in the child's "
     "home language and which English sounds it doesn't use."),
    ("Run a quick check",
     "Enter the child's languages and age. Get cited things to consider, with nothing "
     "stored unless you choose to save a practice case."),
    ("Bring in the family",
     "Print the family interview in six languages, plan with an interpreter, and share "
     "a plain-language handout on raising a bilingual child."),
]


def tone_strip():
    """The six Vietnamese tone words, shown in the Knowledge Library."""
    cells = "".join(f'<div class="tone"><span class="syl">{w}</span>'
                    f'<span class="gloss">{g}</span></div>' for w, g in TONE_WORDS)
    st.markdown(f'<div class="tones">{cells}</div>', unsafe_allow_html=True)
    st.caption("Six different Vietnamese words. Only the tone changes.")


# Journals and organizations the Knowledge Library actually cites.
CITED_IN = ["Journal of Child Language", "Journal of Speech, Language, and Hearing Research",
            "American Journal of Speech-Language Pathology",
            "Language, Speech, and Hearing Services in Schools", "Child Development",
            "Frontiers in Psychology", "ASHA"]
NEW_AMERICA = ("New America. English learners with disabilities: Shining a light on "
               "dual-identified students.")


# Made-up preview cases for "See it in action": (age in months, languages, who).
PREVIEWS = {
    "Spanish": (60, [("Spanish", 65, 55), ("English", 35, 45)],
                "a 5-year-old who hears mostly Spanish at home and English at school"),
    "Vietnamese": (54, [("Vietnamese", 70, 40), ("English", 30, 60)],
                   "a 4-year-old who hears Vietnamese at home and English at preschool"),
    "Mandarin": (50, [("Mandarin", 70, 60), ("English", 30, 40)],
                 "a 4-year-old who hears Mandarin at home and English at preschool"),
    "Arabic": (60, [("Arabic", 60, 70), ("English", 40, 30)],
               "a 5-year-old who speaks Arabic at home and is starting English at school"),
    "Cantonese": (66, [("Cantonese", 55, 50), ("English", 45, 50)],
                  "a 5-year-old who hears Cantonese and English about equally"),
}


def preview_card(language):
    """Real 'things to consider' output for a made-up preview case."""
    from types import SimpleNamespace as Fake
    age, pairs, _ = PREVIEWS[language]
    langs = [Fake(name=n, percent_hears=h, percent_speaks=sp) for n, h, sp in pairs]
    tips = get_considerations(Fake(age_months=age, languages=langs), load_library().keys())
    bars = "".join(
        f'<div class="pv-row"><span class="pv-lang">{l.name}</span>'
        f'<span class="pv-bar"><span style="width:{l.percent_hears}%;background:{TEAL}">'
        f'</span></span><span class="pv-num">{l.percent_hears}%</span></div>'
        f'<div class="pv-row"><span class="pv-lang"></span>'
        f'<span class="pv-bar"><span style="width:{l.percent_speaks}%;background:{GOLD}">'
        f'</span></span><span class="pv-num">{l.percent_speaks}%</span></div>'
        for l in langs)
    shown = [t for t in tips if t["kind"] == "language" and t.get("source")][:2]
    items = "".join(f'<li>{t["text"]}<span class="pv-src">{t["source"]}</span></li>'
                    for t in shown)
    return f"""
<div class="preview">
  <div class="pv-head"><b>Preview case</b><span>Age {years_months(age)}, made up</span></div>
  <div class="pv-key"><i style="background:{TEAL}"></i>Hears <i style="background:{GOLD}"></i>Speaks</div>
  {bars}
  <div class="pv-title">Things to consider</div>
  <ul>{items}</ul>
</div>"""


def _next_fact():
    st.session_state["fact_i"] = (st.session_state.get("fact_i", 0) + 1) % len(FACTS)


def fact_card():
    """One sourced fun fact, with a button for the next one."""
    i = st.session_state.get("fact_i", 0) % len(FACTS)
    glyph, text, source = FACTS[i]
    box = st.container(key="factbox")
    a, b = box.columns([1, 3.2], vertical_alignment="center", gap="large")
    a.markdown(f'<div class="fact-glyph">{glyph}</div>', unsafe_allow_html=True)
    b.markdown(f'<p class="fact-text">{text}</p><span class="fact-src">{source}</span>'
               f'<span class="fact-n">{i + 1} of {len(FACTS)}</span>', unsafe_allow_html=True)
    b.button("Another fact", on_click=_next_fact, key="fact_btn",
             icon=":material/autorenew:")


# ---------------------------------------------------------------- Home
def home():
    library = load_library()
    sources = len(all_references())
    coverage = sum(info.get("california_share", 0) for info in library.values())

    hero = st.container(key="hero")
    left, right = hero.columns([1.15, 0.85], gap="large", vertical_alignment="center")
    with left:
        st.markdown("""
<div class="home-title">Is it a language difference, or a disorder?</div>
<p class="home-lede">A free reference for SLPs working with bilingual children: research
on 10 home languages, side-by-side sound comparisons, and family resources. Every claim
cites its source.</p>
""", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        if b1.button("Open the Sound Explorer", type="primary", width="stretch"):
            st.switch_page(PAGES["sounds"])
        if b2.button("Run a quick check", width="stretch"):
            st.switch_page(PAGES["assess"])
        st.markdown(f"""
<div class="facts"><span>Free, no account</span><span>{len(library)} languages</span>
<span>{sources} cited sources</span><span>{coverage:.0f}% of CA English learners</span></div>""", unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="home-art">{BUBBLES_SVG}</div>', unsafe_allow_html=True)

    st.header("Two mistakes, both costly")
    st.markdown(f"""
<div class="risks">
  <div class="risk r1">{icon("tag", 44)}<div class="risk-title">A difference called a disorder</div>
  <p>A child still learning English gets placed in services they don't need.</p></div>
  <div class="risk r2">{icon("clock", 44)}<div class="risk-title">A disorder called a difference</div>
  <p>A child with a real disorder waits for help because the struggle gets blamed
  on learning English.</p></div>
  <div class="risk-quote">“Schools across the nation both over- and under-identify ELs
  with disabilities,” partly because “several features of language learning mimic
  those associated with certain disabilities.”<span class="pv-src">{NEW_AMERICA}</span></div>
</div>
""", unsafe_allow_html=True)

    shares = [(name, info.get("california_share", 0)) for name, info in library.items()]
    shares.sort(key=lambda x: -x[1])
    donut_colors = ["#0E4F57", "#B3205A", "#6B4E9B", "#5E3A26", "#3E8A8A",
                    "#C9951A", "#8A3B6E", "#3E7A4C", "#B0602A", "#3F5E9C"]
    legend = "".join(f'<li><i style="background:{donut_colors[k]}"></i>{n}'
                     f'<b>{p:.2f}%</b></li>' for k, (n, p) in enumerate(shares))
    st.markdown(f"""
<div class="bigstat"><div class="waffle">{waffle(shares, donut_colors[:len(shares)])}</div>
<div><div class="big-n">{coverage:.0f}%</div>
<div class="t">of California English learners speak one of the {len(library)} home
languages in the Knowledge Library. Each square is 1%.</div>
<ul class="legend">{legend}<li><i style="background:#DCE3E3"></i>All other languages
<b>{100 - coverage:.2f}%</b></li></ul>
<div class="s">California Department of Education, 2022-23.</div></div></div>""",
                unsafe_allow_html=True)

    fact_card()

    st.header("How it works")
    step_icons = ["book", "bulb", "chat"]
    steps = "".join(f'<div class="step c{i}"><div class="step-top"><div class="num">{i}</div>'
                    f'{icon(step_icons[i - 1], 44)}</div>'
                    f'<div class="title">{t}</div><div class="text">{d}</div></div>'
                    for i, (t, d) in enumerate(STEPS, 1))
    st.markdown(f'<div class="steps">{steps}</div>', unsafe_allow_html=True)

    st.header("See it in action")
    picked = st.segmented_control("Pick a home language", list(PREVIEWS),
                                  default="Spanish", key="preview_lang") or "Spanish"
    a, b = st.columns([0.95, 1.05], gap="large", vertical_alignment="center")
    a.markdown(preview_card(picked), unsafe_allow_html=True)
    b.markdown(f"""
<p class="side-lede">This is real output for {PREVIEWS[picked][2]}.</p>
<p class="side-text">The prompts change with the child's languages and age. Each one
names the study behind it, so the SLP can judge how much weight to give it. Switch
languages above to compare.</p>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="cited"><div class="cited-label">The Knowledge Library cites research from</div>
<div class="cited-list">{"".join(f"<span>{j}</span>" for j in CITED_IN)}</div></div>
""", unsafe_allow_html=True)

    st.header("Five myths about bilingual children")
    st.markdown('<p class="section-sub">Each one can push a child toward the wrong '
                'services, or away from the right ones. Here is what the research says.'
                '</p>', unsafe_allow_html=True)
    rows = ""
    for k, (myth, fact, sources) in enumerate(MYTHS, 1):
        cites = ", ".join(dict.fromkeys(short_cite(src) for src in sources))
        rows += (f'<div class="myth"><div class="m-left"><span class="m-n">{k}</span>'
                 f'<p class="m-myth">{myth}</p></div>'
                 f'<div class="m-right"><p class="m-fact">{fact}</p>'
                 f'<span class="m-src">{cites}</span></div></div>')
    st.markdown(f'<div class="myths"><div class="myth-head"><span>The myth</span>'
                f'<span>What research says</span></div>{rows}</div>', unsafe_allow_html=True)
    with st.expander("Full citations"):
        for src in dict.fromkeys(s for _, _, srcs in MYTHS for s in srcs):
            st.markdown(f"- {src}")

    story = st.container(key="story")
    story.header("Why I built this")
    story.markdown(f"""
<div class="story-grid"><div class="quote">
<p>“Bilingual children who speak less-common languages often get misidentified with
speech disorders. I know, because I was one of them. I spoke Vietnamese only at home,
and when I started going to an American public school, my words were jumbled up.”</p>
<div class="who"><span class="mono">AP</span><div><div class="sign">Audrey Pham</div>
<div class="role">Communication Sciences and Disorders, California State University, Fullerton</div></div></div>
</div><div class="story-art">{CHILD_SVG}</div></div>
""", unsafe_allow_html=True)

    if library:
        st.header("Explore by language")
        st.markdown('<p class="section-sub">Researched, cited, and written for the SLP '
                    'in the room. Ranked by share of California English learners. Swipe '
                    'to see all of them.</p>', unsafe_allow_html=True)
        cards = []
        for i, (name, info) in enumerate(library.items()):
            tag, badge, first = CAROUSEL.get(name, ("", "", info.get("summary", "")))
            color = CARD_INK[i % len(CARD_INK)]
            cards.append(
                f'<a class="card" href="knowledge-library" target="_self" '
                f'style="background:{TINT_BG[i % len(TINT_BG)]};'
                f'color:{CARD_INK[i % len(CARD_INK)]} !important">'
                f'<div class="card-top"><span class="card-tag" style="color:{color}">{tag}'
                f'</span>{f"<span class=card-badge>{badge}</span>" if badge else ""}</div>'
                f'<div class="card-autonym" style="color:{color}"'
                f'{RTL if name in RTL_LANGS else ""}>{AUTONYMS.get(name, name)}</div>'
                f'<div class="card-name">{name}</div>'
                f'<div class="card-text">{first}</div>'
                + (f'<div class="card-hi">Hello: <b{RTL if name in RTL_LANGS else ""}>'
                   f'{GREETINGS[name][0]}</b>'
                   + (f' <span>{GREETINGS[name][1]}</span>' if GREETINGS[name][1] else "")
                   + '</div>' if name in GREETINGS else "")
                + f'<div class="card-link" style="color:{color}">Read the research</div></a>')
        st.markdown(f'<div class="carousel">{"".join(cards)}</div>', unsafe_allow_html=True)
        st.caption("Spanish alone is the home language of 81.9% of California English "
                   "learners (California Department of Education, 2022-23).")

    teaser = st.container(key="snd_teaser")
    t1, t2 = teaser.columns([1.05, 1], gap="large", vertical_alignment="center")
    t1.markdown(f"""
<div class="snd-teaser-t">Hear the difference before you score it.</div>
<p class="snd-teaser-p">The Sound Explorer shows which English consonants a home language
doesn't use. Highlighted below: the {len(SOUND_GAPS["Spanish"]["missing"])} English
consonants that aren't in Spanish.</p>""", unsafe_allow_html=True)
    if t1.button("Open the Sound Explorer", type="primary", key="snd_btn"):
        st.switch_page(PAGES["sounds"])
    t2.markdown(consonant_grid(SOUND_GAPS["Spanish"]["missing"], "Spanish", compact=True),
                unsafe_allow_html=True)

    st.header("Everything in CLD Navigator")
    tools_grid()

    st.header("Built for")
    st.markdown(f"""
<div class="personas">
  <div class="persona"><div class="persona-art">{PERSONA_SVGS[0]}</div><div class="who" style="color:#0E4F57">School SLPs</div>
  <p>Sort out a referral for a bilingual student before the IEP meeting, with sources
  you can cite.</p></div>
  <div class="persona"><div class="persona-art">{PERSONA_SVGS[1]}</div><div class="who" style="color:#B3205A">Clinic SLPs</div>
  <p>Walk into an evaluation knowing what's typical for the child's home language and
  age.</p></div>
  <div class="persona"><div class="persona-art">{PERSONA_SVGS[2]}</div><div class="who" style="color:#6B4E9B">SLP grad students</div>
  <p>Learn how language exposure and home-language research change an assessment.</p></div>
</div>""", unsafe_allow_html=True)

    st.header("Questions")
    st.markdown("""
<div class="faq">
<details><summary>Does CLD Navigator diagnose children?</summary>
<p>No. It is not a test and has not been validated with real clinicians or cases. It
gives prompts to consider, and the SLP makes every clinical decision.</p></details>
<details><summary>Is it free?</summary>
<p>Yes. There's no account and no sign-up. Open a page and start.</p></details>
<details><summary>Where does my data go?</summary>
<p>Cases are saved under a code, never a name, and codes must include a number. The
online demo clears saved cases whenever the site restarts. Don't enter identifying
information about real children.</p></details>
<details><summary>Where does the research come from?</summary>
<p>Peer-reviewed journals and professional sources, listed under every language in the
Knowledge Library. The About page lists every check with its source, and marks the
two cutoffs this site set itself.</p></details>
<details><summary>How do I cite CLD Navigator?</summary>
<p>The References page has a ready-to-copy APA citation, plus every source the site
uses, filterable by language and topic.</p></details>
<details><summary>Which languages are covered?</summary>
<p>The ten most common home languages of California English learners: Spanish,
Vietnamese, Mandarin, Arabic, Cantonese, Russian, Farsi, Filipino, Punjabi, and Korean.
The last five start as shorter starter notes.</p></details>
</div>""", unsafe_allow_html=True)

    cta = st.container(key="cta")
    c1, c2 = cta.columns([1.6, 1], vertical_alignment="center")
    c1.markdown(f'<div class="cta-icon">{icon("folders", 56)}</div><div class="cta-title">See what CLD Navigator finds for a real-looking '
                'case.</div><div class="cta-text">Five made-up demo cases load in one '
                'click. No account needed.</div>', unsafe_allow_html=True)
    if c2.button("Load the demo cases", type="primary", width="stretch", key="cta_btn"):
        with Session() as s:
            load_demo_cases(s)
        st.switch_page(PAGES["cases"])

    st.caption("CLD Navigator does not diagnose and is not a test. It has not been "
               "validated with real clinicians or cases.")


# ---------------------------------------------------------------- New Assessment
CODE_PATTERN = re.compile(r"^[A-Z0-9-]+$")
ROUTINE_EXAMPLE = pd.DataFrame([
    {"Who or where": "Mom", "Language": "Spanish",
     "Hours child hears it per week": 25, "Hours child speaks it per week": 10},
    {"Who or where": "Grandma", "Language": "Spanish",
     "Hours child hears it per week": 15, "Hours child speaks it per week": 5},
    {"Who or where": "Preschool", "Language": "English",
     "Hours child hears it per week": 20, "Hours child speaks it per week": 10},
])


def form_defaults():
    defaults = {"lang_count": 2, "code": "", "age": 48, "concerns": "", "notes": ""}
    for i in range(MAX_LANGUAGES):
        defaults.update({f"lang{i}": "", f"h{i}": 50, f"s{i}": 50})
    return defaults


def reset_form():
    for key, value in form_defaults().items():
        st.session_state[key] = value


def to_percents(values):
    """Turn hours into whole percentages that add up to exactly 100."""
    total = sum(values)
    if total <= 0:
        return [0] * len(values)
    raw = [v * 100 / total for v in values]
    result = [int(r) for r in raw]
    by_remainder = sorted(range(len(raw)), key=lambda i: raw[i] - result[i], reverse=True)
    for i in by_remainder[:100 - sum(result)]:
        result[i] += 1
    return result


def routine_to_languages(df):
    """Add up the routine table by language. Returns [(name, hears%, speaks%)]."""
    df = df.copy()
    df["Language"] = df["Language"].fillna("").astype(str).str.strip().str.title()
    df = df[df["Language"] != ""]
    if df.empty:
        return []
    hours = (df.groupby("Language")[["Hours child hears it per week",
                                     "Hours child speaks it per week"]]
             .sum(min_count=1).fillna(0)
             .sort_values("Hours child hears it per week", ascending=False)
             .head(MAX_LANGUAGES))
    hears = to_percents(hours.iloc[:, 0].tolist())
    speaks = to_percents(hours.iloc[:, 1].tolist())
    return list(zip(hours.index.tolist(), hears, speaks))


def apply_routine(results):
    """Copy the calculator's numbers into the form (runs before the page redraws)."""
    reset_form()
    st.session_state["lang_count"] = max(1, len(results))
    for i, (name, hears, speaks) in enumerate(results):
        st.session_state[f"lang{i}"] = name
        st.session_state[f"h{i}"] = hears
        st.session_state[f"s{i}"] = speaks


def exposure_calculator():
    with st.expander("Estimate the percentages from a weekly routine"):
        st.write("List each person or place in the child's week, the language used, "
                 "and roughly how many hours. Add or delete rows as needed.")
        routine = st.data_editor(
            ROUTINE_EXAMPLE, num_rows="dynamic", hide_index=True, width="stretch",
            key="routine",
            column_config={
                "Hours child hears it per week": st.column_config.NumberColumn(
                    min_value=0, max_value=112, step=1),
                "Hours child speaks it per week": st.column_config.NumberColumn(
                    min_value=0, max_value=112, step=1),
            })
        results = routine_to_languages(routine)
        if not results:
            st.caption("Enter at least one language to see percentages.")
            return
        st.dataframe(pd.DataFrame(results, columns=["Language", "Hears %", "Speaks %"]),
                     hide_index=True, width="stretch")
        st.button("Fill the form with these numbers", on_click=apply_routine,
                  args=(results,), type="primary")


def assess():
    page_header("New Assessment",
                "Enter a child's languages and get research-backed things to consider. "
                "Check without saving, or save a practice case under a code.", "mint",
                PAGE_ART["assess"],
                ["Nothing stored unless you save", "A few minutes", "Every prompt cited"])
    st.markdown(f'<div class="privacy">{icon("shield", 40)}<div><b>Keep it anonymous.</b> '
                'Don\'t enter names, birthdays, schools, or other details that could identify '
                'a real child. <b>Check without saving</b> keeps nothing after you leave the '
                'page. Saved cases are meant for practice and demos.</div></div>',
                unsafe_allow_html=True)

    if st.session_state.pop("reset_pending", False):
        reset_form()
    for key, value in form_defaults().items():
        st.session_state.setdefault(key, value)

    chunk(1, "Languages the child hears", "mint",
          "Pick how many, then fill in each one below. Not sure of the percentages? "
          "Use the calculator. Other names like Tagalog, Persian, or Tiếng Việt are "
          "recognized too.")
    count = st.segmented_control("How many languages does the child hear?",
                                 list(range(1, MAX_LANGUAGES + 1)),
                                 key="lang_count") or 1
    exposure_calculator()

    with st.form("new_case", border=False):
        chunk(2, "About the child", "butter",
              "A code is only needed if you save. Use one like CASE-001. Codes need at "
              "least one number, so a real name can't be saved by mistake.")
        col_code, col_age = st.columns(2)
        col_code.text_input("Case code", placeholder="CASE-001", key="code")
        col_age.number_input("Child's age in months", min_value=0, max_value=216,
                             key="age", help="48 months = 4 years. 72 months = 6 years.")

        chunk(3, "Each language", "pink", "Teal is how much the child hears it. "
              "Gold is how much the child speaks it.")
        cols = st.columns(2)
        for i in range(count):
            with cols[i % 2].container(border=True):
                st.markdown(f"**Language {i + 1}**")
                st.text_input("Language name", key=f"lang{i}",
                              placeholder="e.g. Spanish" if i == 0 else "e.g. English")
                st.slider("% of the time the child HEARS it", 0, 100, key=f"h{i}")
                st.slider("% of the time the child SPEAKS it", 0, 100, key=f"s{i}")

        chunk(4, "Concerns and notes", "sky")
        st.text_area("Concerns from family or teacher", key="concerns")
        st.text_area("Clinician notes", key="notes")
        f1, f2 = st.columns(2)
        quick = f1.form_submit_button("Check without saving", type="primary",
                                      icon=":material/bolt:", width="stretch")
        submitted = f2.form_submit_button("Save as a practice case", icon=":material/save:",
                                          width="stretch")

    if quick:
        quick_check(count)
    if submitted:
        save_new_case(count)

    just_saved = st.session_state.pop("just_saved", None)
    if just_saved:
        with Session() as s:
            case = s.query(Case).filter_by(case_code=just_saved).first()
            if case:
                st.success(f"Saved {just_saved}. The form is ready for the next case.")
                show_considerations(get_considerations(case, load_library().keys()))
                sounds_to_watch(case)
        st.page_link(PAGES["cases"], label="See all saved cases", icon=":material/folder_open:")


def case_sound_gaps(case):
    """[(language, [(ipa, example word)], source)] for each case language with sound data."""
    order = [(ipa, w) for group in ENGLISH_CONSONANTS.values() for ipa, w, _ in group]
    gaps = []
    for lang in case.languages:
        typed = lang.name.strip().lower()
        typed = ALIASES.get(typed, typed).lower()
        name = next((k for k in SOUND_GAPS if typed in
                     (k.lower(), AUTONYMS.get(k, "").lower())), None)
        if name:
            data = SOUND_GAPS[name]
            gaps.append((name, [(i, w) for i, w in order if i in data["missing"]],
                         data["sources"][0]))
    return gaps


def sounds_to_watch(case):
    """Chips for English consonants each of the child's home languages doesn't use."""
    for language, sounds, source in case_sound_gaps(case):
        chips = "".join(f'<span class="stw-chip"><b>{ipa}</b>{w}</span>' for ipa, w in sounds)
        st.markdown(f'<div class="stw"><div class="stw-t">English sounds not in {language}'
                    f'<span>{len(sounds)}</span></div><div class="stw-chips">{chips}</div>'
                    f'<div class="stw-src">Errors on these may reflect {language}. '
                    f'Source: {short_cite(source)}.</div></div>', unsafe_allow_html=True)


def quick_check(count):
    """Run every check on the form's values without storing anything."""
    from types import SimpleNamespace
    state = st.session_state
    filled = [(state[f"lang{i}"].strip(), state[f"h{i}"], state[f"s{i}"])
              for i in range(count) if state[f"lang{i}"].strip()]
    langs = [SimpleNamespace(name=n.title() if n.islower() else n, percent_hears=h,
                             percent_speaks=s) for n, h, s in filled]
    problems = []
    if not filled:
        problems.append("Please enter at least one language.")
    if len({n.lower() for n, _, _ in filled}) < len(filled):
        problems.append("The same language was entered twice.")
    problems += check_percentages(langs)
    if problems:
        for p in problems:
            st.error(p)
        return
    case = SimpleNamespace(case_code="Quick check", age_months=state["age"],
                           concerns=state["concerns"], notes=state["notes"], languages=langs)
    tips = get_considerations(case, load_library().keys())
    st.success("Here are the results. Nothing was saved.")
    show_considerations(tips)
    sounds_to_watch(case)
    st.download_button("Download these results as a printable report",
                       case_report_html(case, tips, years_months, case_sound_gaps(case)),
                       file_name="quick-check-report.html", mime="text/html",
                       icon=":material/print:", help="Open the file, then Print > Save as PDF.")


def save_new_case(count):
    state = st.session_state
    case_code = state["code"].strip().upper().replace(" ", "-")
    filled = [(state[f"lang{i}"].strip(), state[f"h{i}"], state[f"s{i}"])
              for i in range(count) if state[f"lang{i}"].strip()]
    names_lower = [name.lower() for name, _, _ in filled]
    languages = [Language(name=n.title() if n.islower() else n,
                          percent_hears=h, percent_speaks=s) for n, h, s in filled]

    problems = []
    if not case_code:
        problems.append("Please enter a case code.")
    elif not CODE_PATTERN.match(case_code) or not any(ch.isdigit() for ch in case_code):
        problems.append("Case codes use letters, numbers, and dashes, with at least "
                        "one number, like CASE-001.")
    if not filled:
        problems.append("Please enter at least one language.")
    if len(set(names_lower)) < len(names_lower):
        problems.append("The same language was entered twice.")
    problems += check_percentages(languages)

    with Session() as s:
        if case_code and s.query(Case).filter_by(case_code=case_code).first():
            problems.append(f"{case_code} already exists. Use a different code.")
        if problems:
            for p in problems:
                st.error(p)
            return
        case = Case(case_code=case_code, age_months=state["age"],
                    concerns=state["concerns"], notes=state["notes"])
        case.languages.extend(languages)
        s.add(case)
        s.commit()

    state["just_saved"] = case_code
    state["reset_pending"] = True
    st.rerun()


# ---------------------------------------------------------------- Saved Cases
def exposure_chart(case):
    df = pd.DataFrame(
        {"Hears %": [lang.percent_hears for lang in case.languages],
         "Speaks %": [lang.percent_speaks for lang in case.languages]},
        index=[lang.name for lang in case.languages])
    st.bar_chart(df, horizontal=True, stack=False, color=[TEAL, GOLD],
                 height=110 + 50 * len(case.languages))


def cases_csv(cases):
    rows = [{"case_code": c.case_code,
             "age_months": c.age_months,
             "languages": "; ".join(f"{l.name} (hears {l.percent_hears}%, "
                                    f"speaks {l.percent_speaks}%)" for l in c.languages),
             "concerns": c.concerns or "",
             "notes": c.notes or "",
             "saved": c.created_at.strftime("%Y-%m-%d %H:%M")} for c in cases]
    return pd.DataFrame(rows).to_csv(index=False)


def save_edit(case_id):
    """Runs when 'Save changes' is clicked, before the page redraws."""
    state = st.session_state
    with Session() as s:
        case = s.get(Case, case_id)
        if case:
            case.age_months = state[f"eage{case_id}"]
            case.concerns = state[f"econcerns{case_id}"]
            case.notes = state[f"enotes{case_id}"]
            s.commit()
    state[f"editing{case_id}"] = False
    st.toast("Changes saved.")


def edit_case_form(case):
    with st.form(f"edit{case.id}"):
        st.number_input("Child's age in months", 0, 216, case.age_months,
                        key=f"eage{case.id}")
        st.text_area("Concerns from family or teacher", case.concerns or "",
                     key=f"econcerns{case.id}")
        st.text_area("Clinician notes", case.notes or "", key=f"enotes{case.id}")
        st.form_submit_button("Save changes", type="primary",
                              on_click=save_edit, args=(case.id,))


def saved_cases():
    page_header("Saved Cases", "Practice and demo cases, each with its exposure chart, "
                "things to consider, and printable report.", "butter", PAGE_ART["cases"],
                ["For practice, not real records", "Print or save as PDF", "Search and sort"])
    library_names = load_library().keys()

    with Session() as s:
        if st.button("Load demo cases", help="Adds five made-up cases to try the site."):
            added = load_demo_cases(s)
            st.toast(f"Added {added} demo cases." if added
                     else "Demo cases are already loaded.")

        cases = s.query(Case).all()
        if not cases:
            st.markdown(f'<div class="empty"><div class="empty-art">{PERSONA_SVGS[1]}</div>'
                        '<div class="empty-t">No cases yet</div><p>Add one on the New Assessment page, or '
                        'select Load demo cases above to try five made-up cases.</p></div>',
                        unsafe_allow_html=True)
            return

        all_languages = {lang.name.title() for c in cases for lang in c.languages}
        m1, m2, m3 = st.columns(3)
        m1.metric("Cases", len(cases), border=True)
        m2.metric("Languages represented", len(all_languages), border=True)
        m3.metric("Average age", years_months(sum(c.age_months for c in cases)
                                              / len(cases)), border=True)

        col_search, col_sort = st.columns([2, 1])
        search = col_search.text_input("Search by case code or language",
                                       placeholder="e.g. Vietnamese").strip().lower()
        order = col_sort.selectbox("Sort by", ["Newest first", "Oldest first",
                                               "Youngest first", "Oldest child first"])

        sort_keys = {"Newest first": (lambda c: c.created_at, True),
                     "Oldest first": (lambda c: c.created_at, False),
                     "Youngest first": (lambda c: c.age_months, False),
                     "Oldest child first": (lambda c: c.age_months, True)}
        key, reverse = sort_keys[order]
        shown = sorted((c for c in cases
                        if not search
                        or search in c.case_code.lower()
                        or any(search in l.name.lower() for l in c.languages)),
                       key=key, reverse=reverse)

        st.download_button("Download all cases (.csv)", cases_csv(shown),
                           file_name="cld_navigator_cases.csv", mime="text/csv")
        with st.expander("Delete all saved cases"):
            sure_all = st.checkbox("I understand this deletes every saved case.",
                                   key="sure_all")
            if st.button("Delete all cases", disabled=not sure_all, key="del_all"):
                for c in cases:
                    s.delete(c)
                s.commit()
                st.rerun()

        if not shown:
            st.warning("No cases match that search.")

        for case in shown:
            tips = get_considerations(case, library_names)
            langs = ", ".join(l.name for l in case.languages)
            label = f"**{case.case_code}**, age {years_months(case.age_months)}, {langs}"
            with st.expander(label):
                left, right = st.columns([3, 2])
                with left:
                    st.markdown("**Language exposure**")
                    exposure_chart(case)
                with right:
                    st.markdown(f"**Age:** {case.age_months} months "
                                f"({years_months(case.age_months)})")
                    st.markdown(f"**Concerns:** {case.concerns or 'None'}")
                    st.markdown(f"**Notes:** {case.notes or 'None'}")
                    st.caption(f"Saved {case.created_at.strftime('%b %d, %Y')}")
                    st.toggle("Edit age, concerns, and notes", key=f"editing{case.id}")

                if st.session_state.get(f"editing{case.id}"):
                    edit_case_form(case)

                show_considerations(tips)
                sounds_to_watch(case)

                b1, b2, b3 = st.columns(3)
                b1.download_button("Printable report",
                                   case_report_html(case, tips, years_months,
                                                    case_sound_gaps(case)),
                                   file_name=f"{case.case_code}-report.html",
                                   mime="text/html", key=f"html{case.id}",
                                   help="Open the file, then Print > Save as PDF.")
                b2.download_button("Plain text (.txt)",
                                   case_summary_text(case, tips),
                                   file_name=f"{case.case_code}.txt",
                                   key=f"dl{case.id}")
                b3.page_link(PAGES["interview"], label="Family interview", icon=":material/family_restroom:")

                sure = st.checkbox("I want to delete this case", key=f"sure{case.id}")
                if st.button("Delete this case", key=f"del{case.id}", disabled=not sure):
                    s.delete(case)
                    s.commit()
                    st.rerun()


# ---------------------------------------------------------------- Family Interview
def interview():
    page_header("Family Interview", "Questions to build a child's language history "
                "with the family. Pick a case to fill in its languages, then print the "
                "guide and write answers by hand.", "pink", PAGE_ART["interview"],
                ["16 questions", "6 languages", "Printable"])

    with Session() as s:
        cases = {c.case_code: [l.name for l in c.languages]
                 for c in s.query(Case).order_by(Case.case_code).all()}

    blank = "No case (blank guide)"
    choice = st.selectbox("Case", [blank] + list(cases.keys()))
    if choice == blank:
        typed = st.text_input("Languages the child hears (separate with commas)",
                              placeholder="e.g. Vietnamese, English")
        languages = [t.strip() for t in typed.split(",") if t.strip()]
        code = ""
    else:
        languages, code = cases[choice], choice

    choice_lang = st.segmented_control(
        "Interview language", list(INTERVIEW_LANGUAGES), default="English",
        key="interview_lang") or "English"
    code_lang = INTERVIEW_LANGUAGES[choice_lang]
    rtl = code_lang in RTL_CODES
    with_english = False
    if code_lang != "en":
        with_english = st.toggle("Show English under each question",
                                 help="For an SLP and family who don't share a language.")
        st.caption(f"The {choice_lang} wording is a draft. Have a native speaker review "
                   "it before using it with families.")

    sections = interview_lines(languages, code_lang, with_english)
    st.download_button("Download printable interview", type="primary",
                       data=interview_html(sections, code, INTERVIEW_LABELS, code_lang,
                                           with_english, rtl),
                       file_name=f"{code or 'family'}-interview-{code_lang}.html",
                       mime="text/html", help="Open the file, then Print > Save as PDF.")

    number = 1
    direction = ' dir="rtl" style="text-align:right"' if rtl else ""
    section_icons = ["clock", "calendar", "chat", "globe"]
    for s_index, (title, lines) in enumerate(sections):
        with st.container(border=True):
            items = ""
            for main, english in lines:
                eng = (f'<div class="q-en" dir="ltr">{english}</div>' if english else "")
                items += f'<li value="{number}">{main}{eng}</li>'
                number += 1
            st.markdown(f'<div class="q-block"{direction}><div class="q-title">'
                        f'{icon(section_icons[s_index % 4], 36)}<span>{title}</span>'
                        f'</div><ol>{items}</ol></div>', unsafe_allow_html=True)

    st.header("Working with an interpreter")
    st.markdown('<p class="section-sub" style="margin-top:0">ASHA recommends a '
                'briefing, interaction, and debriefing process. The SLP leads the '
                'session the whole time.</p>', unsafe_allow_html=True)
    bid = [("calendar", "Briefing", "Before",
            "Meet with the interpreter ahead of time so they can prepare, and provide "
            "any training they need before the session."),
           ("chat", "Interaction", "During",
            "The SLP is responsible for the session and stays actively engaged with the "
            "family and the interpreter."),
           ("form", "Debriefing", "After",
            "Talk with the interpreter about how the session went, to be sure no issues "
            "came up.")]
    st.markdown(f'<div class="interp-art">{SESSION_SVG}</div>', unsafe_allow_html=True)
    cards = "".join(f'<div class="bid-card">{icon(ic, 44)}<div class="bid-when">{when}</div>'
                    f'<div class="bid-t">{t}</div><p>{p}</p></div>'
                    for ic, t, when, p in bid)
    st.markdown(f'<div class="bid">{cards}</div><div class="fact" style="margin-top:1rem">'
                f'{icon("shield", 40)}<p>Family or friends acting as interpreters may '
                'present conflicts, and untrained interpreters may unintentionally change '
                'a meaning or influence answers. Be especially careful in evaluations.</p>'
                '</div>', unsafe_allow_html=True)
    st.caption("From ASHA's Practice Portal: Collaborating with interpreters, "
               "transliterators, and translators.")

    st.header("A handout for families")
    st.markdown('<p class="section-sub" style="margin-top:0">One page, in plain language: '
                'what research says about raising a bilingual child, with sources. Print it '
                'for the family interview or an IEP meeting.</p>', unsafe_allow_html=True)
    points = [
        ("Two languages don't cause a delay",
         "In a study of toddlers, bilingual children were not slower to build early "
         "vocabulary when words in both languages were counted.", "Pearson et al., 1993"),
        ("Mixing languages is normal",
         "Mixing two languages in one sentence is a normal part of bilingual development, "
         "not a sign of confusion.", "Genesee, 2009"),
        ("Keep your home language",
         "Families are encouraged to keep using the home language. In one study, parents' "
         "use of Vietnamese supported their children's Vietnamese vocabulary and was not "
         "related to their English vocabulary.", "Genesee, 2009; Pham & Tipton, 2018"),
        ("Children with language disorders can learn two languages",
         "Learning two languages did not appear to add risk for children with a language "
         "impairment. The studies are small, so researchers are still learning.",
         "Paradis et al., 2003; Genesee, 2009"),
    ]
    st.download_button("Download the family handout", type="primary",
                       data=family_handout_html(points, [PEARSON, GENESEE, PHAM_TIPTON,
                                                         PARADIS]),
                       file_name="raising-a-bilingual-child.html", mime="text/html",
                       icon=":material/print:", help="Open the file, then Print > Save as PDF.")


# ---------------------------------------------------------------- Insights
def insights():
    page_header("Insights", "Patterns across every saved case: which languages, which "
                "ages, and where children hear a language more than they speak it.",
                "sky", PAGE_ART["insights"], ["Updates as you save", "Caseload view"])

    with Session() as s:
        cases = s.query(Case).all()
        if not cases:
            st.markdown(f'<div class="empty"><div class="empty-art">{PERSONA_SVGS[2]}</div>'
                        '<div class="empty-t">Nothing to chart yet</div><p>Insights fill in as you save cases. '
                        'Load the demo cases to see a sample caseload.</p></div>',
                        unsafe_allow_html=True)
            st.page_link(PAGES["cases"], label="Open Saved Cases", icon=":material/folder_open:")
            return
        rows = [{"case": c.case_code, "age_months": c.age_months,
                 "language": l.name.title(), "hears": l.percent_hears or 0,
                 "speaks": l.percent_speaks or 0, "languages_on_case": len(c.languages)}
                for c in cases for l in c.languages]
        tips = {c.case_code: get_considerations(c, load_library().keys())
                for c in cases}
        sound_counts = {}
        for c in cases:
            for ipa in {i for _, sounds, _ in case_sound_gaps(c) for i, _ in sounds}:
                sound_counts[ipa] = sound_counts.get(ipa, 0) + 1

    df = pd.DataFrame(rows)
    per_case = df.drop_duplicates("case")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Cases", len(per_case), border=True)
    m2.metric("Languages", df["language"].nunique(), border=True)
    m3.metric("Bilingual cases", int((per_case["languages_on_case"] > 1).sum()),
              border=True)
    flagged = sum(1 for t in tips.values()
                  if any(x["kind"] == "language" and x.get("source") for x in t))
    m4.metric("Cases with cited checks", flagged, border=True)

    left, right = st.columns(2)
    with left.container(border=True):
        st.markdown("**Cases per language**")
        st.bar_chart(df.groupby("language")["case"].nunique().rename("Cases"),
                     color=TEAL, height=260)
    with right.container(border=True):
        st.markdown("**Ages (years)**")
        ages = (per_case["age_months"] // 12).value_counts().sort_index()
        ages.index = [f"{int(a)} yr" for a in ages.index]
        st.bar_chart(ages.rename("Cases"), color=GOLD, height=260)

    with st.container(border=True):
        st.markdown("**Average exposure by language**")
        avg = df.groupby("language")[["hears", "speaks"]].mean().round(0)
        avg.columns = ["Hears %", "Speaks %"]
        st.bar_chart(avg, horizontal=True, stack=False, color=[TEAL, GOLD],
                     height=120 + 45 * len(avg))
        st.caption("The gap between hears and speaks shows where children understand "
                   "a language more than they use it.")

    if sound_counts:
        examples = {i: w for g in ENGLISH_CONSONANTS.values() for i, w, _ in g}
        top = max(sound_counts.values())
        rows = "".join(
            f'<div class="sc-row"><span class="sc-ipa">/{ipa}/</span>'
            f'<span class="sc-w">{examples.get(ipa, "")}</span><span class="sc-bar">'
            f'<span style="width:{n / top * 100:.0f}%"></span></span>'
            f'<span class="sc-n">{n}</span></div>'
            for ipa, n in sorted(sound_counts.items(), key=lambda kv: (-kv[1], kv[0])))
        with st.container(border=True):
            st.markdown("**English sounds to watch across the caseload**")
            st.markdown(f'<div class="sc">{rows}</div>', unsafe_allow_html=True)
            st.caption("How many saved cases have a home language that doesn't use each "
                       "English consonant, from the Sound Explorer data.")

    with st.container(border=True):
        st.markdown("**Most common things to consider**")
        counts = pd.Series([x["text"].split(".")[0] for t in tips.values() for x in t
                            if x["kind"] != "general"]).value_counts()
        if counts.empty:
            st.write("Only general reminders so far.")
        else:
            st.dataframe(counts.rename_axis("Prompt").reset_index(name="Cases"),
                         hide_index=True, width="stretch")


# ---------------------------------------------------------------- Sound Explorer
def _word(word, letters):
    """'think', 'th' -> 'th' in bold inside the word."""
    i = word.find(letters)
    if i < 0:
        return word
    return f"{word[:i]}<b>{letters}</b>{word[i + len(letters):]}"


def consonant_grid(missing, language, compact=False):
    """English consonants as tiles. Tiles for sounds the home language lacks stand out."""
    rows = ""
    for group, sounds in ENGLISH_CONSONANTS.items():
        tiles = "".join(
            f'<div class="snd{" miss" if ipa in missing else ""}" '
            f'title="{"Not in " + language if ipa in missing else "In both languages"}">'
            f'<span class="ipa">{ipa}</span><span class="w">{_word(w, g)}</span></div>'
            for ipa, w, g in sounds)
        if compact:
            rows += tiles
        else:
            rows += f'<div class="snd-group"><div class="snd-label">{group}</div>' \
                    f'<div class="snd-row">{tiles}</div></div>'
    return f'<div class="snd-grid{" compact" if compact else ""}">{rows}</div>'


def tone_section(language, heading=True):
    """Pitch drawings for each tone of a tonal language."""
    data = TONES[language]
    if heading:
        st.header(f"The tones of {language}")
    st.markdown(f'<p class="tone-intro">{data["intro"]}</p>'
                '<p class="tone-how">Each drawing shows the voice\'s pitch from the start '
                'of the word to the end. Higher on the drawing means a higher voice.</p>'
                f'{tone_chart(data["tones"])}'
                '<div class="tone-key"><span>High</span><span>Low</span></div>',
                unsafe_allow_html=True)
    st.caption(data["caption"])
    return data["sources"]


def diglossia_diagram():
    """Spoken Arabic at home, Standard Arabic at school."""
    st.markdown(f"""
<div class="digl">
  <div class="digl-side home">{icon("chat", 52)}<div class="t">Spoken Arabic</div>
  <p>The dialect the child speaks at home and in the neighborhood, for everyday talk.</p>
  <div class="digl-tags"><span>Home</span><span>Family</span><span>Play</span></div></div>
  <div class="digl-mid"><div class="digl-arrow"></div>
  <p>A task in Standard Arabic may measure familiarity with that variety, not only the
  skill it targets.</p></div>
  <div class="digl-side school">{icon("school", 52)}<div class="t">Standard Arabic</div>
  <p>Used for reading, writing, and formal settings like the classroom. Children first
  learn to read in a variety they do not speak.</p>
  <div class="digl-tags"><span>Reading</span><span>Writing</span><span>School</span></div></div>
</div>""", unsafe_allow_html=True)
    st.caption("From Schiff and Saiegh-Haddad (2018). Ask the family which dialect the "
               "child speaks, and which variety a test uses.")
    return [SCHIFF_FULL]


def across_languages(picked=None):
    """Every English consonant against every home language with data: one matrix."""
    langs = [n for n in load_library() if n in SOUND_GAPS]
    sounds = [s for group in ENGLISH_CONSONANTS.values() for s in group]
    head = "".join(f'<th scope="col"><span>{ipa}</span></th>' for ipa, _, _ in sounds)
    rows = ""
    for lang in langs:
        missing = SOUND_GAPS[lang]["missing"]
        cells = "".join(f'<td class="{"x" if ipa in missing else ""}" title="/{ipa}/ '
                        f'{"not in" if ipa in missing else "in"} {lang}"></td>'
                        for ipa, _, _ in sounds)
        rows += (f'<tr{" class=on" if lang == picked else ""}><th scope="row">{lang}'
                 f'<small>{len(missing)}</small></th>{cells}</tr>')
    counts = "".join(
        f'<td class="cnt">{sum(ipa in SOUND_GAPS[l]["missing"] for l in langs) or ""}</td>'
        for ipa, _, _ in sounds)
    tally = {ipa: sum(ipa in SOUND_GAPS[l]["missing"] for l in langs) for ipa, _, _ in sounds}
    top_n = max(tally.values())
    common = [ipa for ipa, _, _ in sounds if tally[ipa] == top_n]
    examples = {ipa: w for ipa, w, _ in sounds}
    st.header("Across languages")
    st.markdown(f"""
<p class="section-sub" style="margin-top:0">Each filled square is an English consonant
that a home language doesn't use. The bottom row counts how many of these
{len(langs)} languages lack each sound.</p>
<div class="matrix-wrap"><table class="matrix{' has-pick' if picked in langs else ''}">
<thead><tr><th></th>{head}</tr></thead>
<tbody>{rows}<tr class="cnt-row"><th scope="row">Languages</th>{counts}</tr></tbody>
</table></div>""", unsafe_allow_html=True)
    if common:
        these = "these sounds" if len(common) > 1 else "this sound"
        who = (f"None of the {len(langs)} languages here use {these}" if top_n == len(langs)
               else f"{top_n} of the {len(langs)} languages here don't use {these}, more "
                    "than any other English consonant")
        st.markdown(f"""<div class="fact">{icon("bulb", 40)}
<p>{", ".join(f"/{c}/ as in <i>{examples[c]}</i>" for c in common)}. {who}, so errors
on {"them" if len(common) > 1 else "it"} in English may reflect many home languages.</p>
</div>""", unsafe_allow_html=True)


MOUTH_Y = [72, 46, 30, 18, 12, 10, 24, 62]  # height of the roof line at each place, in %


def mouth_map(missing, language):
    """English consonants laid out from the lips to the throat, along a drawn roof line."""
    n = len(PLACES)
    tiles = labels = dots = ""
    for i, (name, _, ipas) in enumerate(PLACES):
        t = "".join(f'<span class="mm-t{" miss" if s in missing else ""}">{s}</span>'
                    for s in ipas)
        tiles += f'<div class="mm-col">{t}</div>'
        labels += f'<div class="mm-lab">{name}</div>'
        hit = any(s in missing for s in ipas)
        dots += (f'<i class="mm-dot{" hit" if hit else ""}" style="left:{(i + 0.5) / n * 100:.2f}%;'
                 f'top:{MOUTH_Y[i]}%"></i>')
    pts = [((i + 0.5) / n * 800, y) for i, y in enumerate(MOUTH_Y)]
    p = [pts[0]] + pts + [pts[-1]]
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    for i in range(1, len(p) - 2):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p[i - 1], p[i], p[i + 1], p[i + 2]
        d += (f"C {x1 + (x2 - x0) / 6:.1f} {y1 + (y2 - y0) / 6:.1f} "
              f"{x2 - (x3 - x1) / 6:.1f} {y2 - (y3 - y1) / 6:.1f} {x2:.1f} {y2:.1f} ")
    band = (f'<svg viewBox="0 0 800 100" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="{d}" fill="none" stroke="#13303A" stroke-width="2.5" '
            'stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')
    st.markdown(f"""
<div class="mm" role="img" aria-label="English consonants arranged from the lips to the throat">
  <div class="mm-row">{tiles}</div>
  <div class="mm-band">{band}{dots}</div>
  <div class="mm-row">{labels}</div>
  <div class="mm-ends"><span>Front of the mouth</span><span>Back of the mouth</span></div>
</div>""", unsafe_allow_html=True)
    by_place = [(sum(s in missing for s in ipas), phrase) for _, phrase, ipas in PLACES]
    k, phrase = max(by_place)
    if k >= 2 and missing:
        st.markdown(f'<div class="fact">{icon("bulb", 40)}<p>{k} of the {len(missing)} '
                    f'English consonants {language} doesn\'t use are made {phrase}.</p></div>',
                    unsafe_allow_html=True)


def milestone_timeline():
    """When children master speech sounds, by language, from the cited studies."""
    order = list(load_library())
    lo, hi = 1.5, 6.5
    items = ""
    for k, (age, end, lang, what, src) in enumerate(MILESTONES):
        color = (LANG_COLORS[order.index(lang) % len(LANG_COLORS)] if lang in order
                 else "#13303A")
        left = (age - lo) / (hi - lo) * 100
        width = ((end - age) / (hi - lo) * 100) if end else 0
        when = (f"{int(age)};{round((age % 1) * 12)}" if not end else
                f"{int(age)};{round((age % 1) * 12)} to {int(end)};{round((end % 1) * 12)}")
        items += (f'<div class="tl-item {"up" if k % 2 == 0 else "down"}" '
                  f'style="--x:{left:.2f}%;--w:{width:.2f}%;--c:{color}">'
                  f'<span class="tl-mark"></span><div class="tl-card"><b>{lang}</b>'
                  f'<span class="tl-age">{when}</span><p>{what}</p>'
                  f'<span class="tl-src">{src}</span></div></div>')
    ticks = "".join(f'<span style="left:{(a - lo) / (hi - lo) * 100:.2f}%">{a} yr</span>'
                    for a in range(2, 7))
    st.markdown(f'<div class="tl"><div class="tl-axis"></div><div class="tl-ticks">{ticks}'
                f'</div>{items}</div>', unsafe_allow_html=True)
    st.caption("Ages are written years;months, so 3;6 is three and a half. Each study "
               "covered one dialect and group of children. Use these as reference "
               "points, not cutoffs.")


TOOLS = [
    ("assess", "Quick check", "Enter a child's languages and get cited things to consider. "
     "Nothing is stored unless you save.",
     "new-assessment"),
    ("interview", "Family Interview", "Print questions in six languages for the family.",
     "family-interview"),
    ("sounds", "Sound Explorer", "See which English sounds a home language doesn't use.",
     "sound-explorer"),
    ("library", "Knowledge Library", "Research on each home language, with sources.",
     "knowledge-library"),
    ("insights", "Insights", "Spot patterns across every saved case.", "insights"),
    ("refs", "References", "Every source in one list, plus how to cite the tool.",
     "references"),
]


def tools_grid():
    tiles = "".join(f'<a class="tool" href="{href}" target="_self"><div class="tool-art">'
                    f'{PAGE_ART[key]}</div><div class="tool-t">{title}</div>'
                    f'<p>{text}</p></a>' for key, title, text, href in TOOLS)
    st.markdown(f'<div class="tools">{tiles}</div>', unsafe_allow_html=True)


def word_pairs(missing):
    """Minimal pairs for each missing sound that has them."""
    examples = {i: (w, g) for grp in ENGLISH_CONSONANTS.values() for i, w, g in grp}
    cards = ""
    for ipa, _, _ in [s for grp in ENGLISH_CONSONANTS.values() for s in grp]:
        if ipa not in missing or ipa not in PAIRS:
            continue
        pairs = "".join(f'<div class="wp-pair"><span class="a">{a}</span>'
                        f'<span class="vs">or</span><span class="b">{b}</span></div>'
                        for a, b in PAIRS[ipa])
        cards += f'<div class="wp"><div class="wp-ipa">/{ipa}/</div>{pairs}</div>'
    if cards:
        st.markdown(f'<div class="wps">{cards}</div>', unsafe_allow_html=True)
        st.caption("Each pair differs by one sound. Say a word and ask the child to point "
                   "to the matching picture, or ask the child to name pictures of both. "
                   "Pairs are English words, not a test.")


def sound_quiz(language, missing):
    """A quick self-check: which of these English sounds does the language not use?"""
    import random
    all_ipa = [s for grp in ENGLISH_CONSONANTS.values() for s, _, _ in grp]
    seed_key = f"quiz_seed_{language}"
    if seed_key not in st.session_state:
        st.session_state[seed_key] = random.randint(0, 10**6)
    rnd = random.Random(st.session_state[seed_key])
    pick_miss = rnd.sample(sorted(missing), min(3, len(missing)))
    pick_have = rnd.sample([s for s in all_ipa if s not in missing], 3)
    options = pick_miss + pick_have
    rnd.shuffle(options)
    box = st.container(key="quizbox")
    box.markdown(f'<div class="quiz-q">Which of these English sounds does {language} '
                 'not use? Pick all that apply.</div>', unsafe_allow_html=True)
    chosen = box.pills("Sounds", options, selection_mode="multi",
                       key=f"quiz_pick_{language}_{st.session_state[seed_key]}",
                       label_visibility="collapsed",
                       format_func=lambda s: f"/{s}/")
    c1, c2 = box.columns([1, 1])
    checked = c1.button("Check my answer", type="primary", key=f"quiz_check_{language}")
    if c2.button("New question", key=f"quiz_new_{language}"):
        st.session_state[seed_key] = random.randint(0, 10**6)
        st.rerun()
    if checked:
        chosen = set(chosen or [])
        right = set(pick_miss)
        if chosen == right:
            box.success(f"Right. {language} doesn't use "
                        + ", ".join(f"/{s}/" for s in pick_miss) + ".")
        else:
            missed = right - chosen
            extra = chosen - right
            msg = []
            if missed:
                msg.append(f"{language} also doesn't use " + ", ".join(f"/{s}/" for s in sorted(missed)) + ".")
            if extra:
                msg.append(f"{language} does use " + ", ".join(f"/{s}/" for s in sorted(extra)) + ".")
            box.info(" ".join(msg) + " Check the grid above, then try a new question.")


def sound_explorer():
    page_header("Sound Explorer", "See which English consonants a child's home language "
                "doesn't use, and how tones work in Vietnamese, Mandarin, and Cantonese. "
                "Errors on these sounds can come from the home language, not a disorder.",
                "mint", PAGE_ART["sounds"],
                [f"{TOTAL_CONSONANTS} English consonants", f"Tone charts for {len(TONES)} "
                 "languages", "Cited sources"])

    languages = [n for n in load_library() if n in SOUND_GAPS or n in SOUND_PENDING]
    languages += [n for n in list(SOUND_GAPS) + list(SOUND_PENDING) if n not in languages]
    picked = st.segmented_control(
        "Home language", languages, key="snd_lang",
        default=None if st.session_state.get("snd_lang") else languages[0],
        format_func=lambda n: f"{n} ({AUTONYMS[n]})" if n in AUTONYMS else n) or languages[0]

    if picked in SOUND_PENDING:
        st.markdown(f'<div class="snd-soon">{icon("search", 40)}<div><b>The {picked} '
                    'consonant comparison is coming next.</b> Here is what the cited '
                    f'sources already show. {SOUND_PENDING[picked]}</div></div>',
                    unsafe_allow_html=True)
        sources = tone_section(picked, heading=False) if picked in TONES else []
        sources += PENDING_SOURCES.get(picked, [])
        with st.expander(f"Sources and further reading ({len(sources)})"):
            for source in sources:
                st.markdown(f"- {source}")
        st.page_link(PAGES["library"], label=f"Read the full {picked} note in the "
                     "Knowledge Library", icon=":material/menu_book:")
        across_languages()
        return

    data = SOUND_GAPS[picked]
    n_miss = len(data["missing"])
    st.markdown(f"""
<div class="snd-sum">
  <div class="snd-big">{n_miss}<span>of {TOTAL_CONSONANTS}</span></div>
  <div><div class="snd-sum-t">English consonants are not in {picked}
  (<span{RTL if picked in RTL_LANGS else ""}>{AUTONYMS.get(picked, picked)}</span>).</div>
  <div class="snd-key"><span><i class="k-miss"></i>Not in {picked}</span>
  <span><i class="k-both"></i>In both languages</span></div></div>
</div>""", unsafe_allow_html=True)

    st.markdown(consonant_grid(data["missing"], picked), unsafe_allow_html=True)
    st.caption(data["note"])
    st.download_button(f"Download a printable {picked} sound sheet",
                       sound_sheet_html(picked, data, ENGLISH_CONSONANTS, _word),
                       file_name=f"{picked.lower()}-sound-sheet.html", mime="text/html",
                       icon=":material/print:", key=f"sheet_{picked}",
                       help="Open the file, then Print > Save as PDF.")

    st.header("Where in the mouth")
    st.markdown('<p class="section-sub" style="margin-top:0">The same 24 consonants, '
                'placed where the tongue or lips make them, from the front of the mouth '
                'to the back.</p>', unsafe_allow_html=True)
    mouth_map(data["missing"], picked)

    if any(s in PAIRS for s in data["missing"]):
        st.header("Word pairs to try")
        st.markdown(f'<p class="section-sub" style="margin-top:0">For each English sound '
                    f'{picked} doesn\'t use, two English words that differ only in that '
                    'sound.</p>', unsafe_allow_html=True)
        word_pairs(data["missing"])

    st.header("Quick check")
    sound_quiz(picked, data["missing"])

    if data["extras"]:
        st.header(f"Also different in {picked}")
    cards = ""
    for title, lede, chips, text in data["extras"]:
        chip_html = "".join(f"<span>{c}</span>" for c in chips)
        cards += (f'<div class="snd-extra"><div class="t">{title}</div>'
                  f'<p class="lede">{lede}</p><div class="snd-chips">{chip_html}</div>'
                  f'<p>{text}</p></div>')
    if cards:
        st.markdown(f'<div class="snd-extras">{cards}</div>', unsafe_allow_html=True)
    extra_sources = tone_section(picked) if picked in TONES else []
    if picked == "Arabic":
        st.header("Two kinds of Arabic")
        extra_sources += diglossia_diagram()

    st.markdown("""
<div class="snd-how"><div class="t">How to use this</div>
<p>Compare the child's English errors with the highlighted sounds. Errors on sounds the
home language doesn't have may reflect the home language. Errors on sounds both languages
share, or errors in the home language too, deserve a closer look. This chart does not
diagnose, and the SLP makes every clinical decision.</p></div>""", unsafe_allow_html=True)

    all_sources = list(dict.fromkeys(data["sources"] + extra_sources))
    with st.expander(f"Sources ({len(all_sources)})"):
        for source in all_sources:
            st.markdown(f"- {source}")
    across_languages(picked)


# ---------------------------------------------------------------- Knowledge Library
def library():
    notes_all = load_library()
    n_sources = len({x for i in notes_all.values() for x in i.get("sources", [])})
    page_header("Knowledge Library", "Research on assessing children who speak each "
                "language. Every note lists its sources.", "leaf", PAGE_ART["library"],
                [f"{len(notes_all)} languages", f"{n_sources} cited sources",
                 f"{len(GLOSSARY)} key terms"])

    notes = load_library()
    if not notes:
        st.warning("No research notes found. Check that language_notes.json is in "
                   "the project folder.")
        return

    st.markdown('<h2 style="margin-top:0">Speech development at a glance</h2>'
                '<p class="section-sub">When children in each study had mastered key '
                'sounds. Select a language below for the full research note.</p>',
                unsafe_allow_html=True)
    milestone_timeline()
    st.header("Research by language")
    search = st.text_input("Search every language and key term",
                           placeholder="e.g. tones, dialect, final consonants"
                           ).strip().lower()

    if search:
        shown = {}
        for language, info in notes.items():
            sections = {t: x for t, x in info.get("sections", {}).items()
                        if search in x.lower() or search in t.lower()
                        or search in language.lower()}
            if sections:
                shown[language] = sections
        if not shown:
            st.caption("No language notes match that search.")
    else:
        picked = st.segmented_control(
            "Language", list(notes), default=list(notes)[0], key="lib_lang",
            format_func=lambda n: f"{n} ({AUTONYMS[n]})" if n in AUTONYMS else n
            ) or list(notes)[0]
        shown = {picked: notes[picked].get("sections", {})}

    for i, (language, sections) in enumerate(shown.items()):
        info = notes[language]
        color = LANG_COLORS[list(notes).index(language) % len(LANG_COLORS)]
        with st.container(border=True):
            st.markdown(
                f'<div class="lib-head"><span class="autonym" style="color:{color}"'
                f'{RTL if language in RTL_LANGS else ""}>{AUTONYMS.get(language, language)}'
                f'</span><span class="english">{language}</span></div>'
                + (f'<div class="lib-share">{info["california_share"]:.2f}% of California '
                   'English learners have this home language (California Department of '
                   'Education, 2022-23)</div>' if info.get("california_share") else "")
                + (f'<p class="lib-summary">{info["summary"]}</p>'
                   if info.get("summary") else ""), unsafe_allow_html=True)
            if language in TONES:
                tone_section(language, heading=False)
            if language in PHRASES:
                cards = "".join(f'<div class="ph"><span class="ph-v">{a}</span>'
                                f'<span class="ph-e">{b}</span></div>'
                                for a, b in PHRASES[language])
                st.markdown(f'<div class="ph-title">Phrases for sessions</div>'
                            f'<div class="phs">{cards}</div>', unsafe_allow_html=True)
                st.caption("Draft wording, not yet reviewed by a native speaker. In "
                           "Vietnamese, the speaker's word for themselves depends on the "
                           "relationship: cô for a woman, thầy or chú for a man, and con "
                           "for the child. Work with an interpreter for assessment.")
            if language == "Arabic":
                diglossia_diagram()
            if st.button(f"See {language} in the Sound Explorer", key=f"go_snd_{language}",
                         icon=":material/graphic_eq:"):
                st.session_state["snd_lang"] = language
                st.switch_page(PAGES["sounds"])
            tabs = st.tabs(list(sections.keys()))
            for tab, text in zip(tabs, sections.values()):
                tab.write(text)
            if info.get("sources"):
                with st.expander(f"Sources ({len(info['sources'])})"):
                    for source in info["sources"]:
                        st.markdown(f"- {source}")

    terms = {t: d for t, d in GLOSSARY.items()
             if not search or search in t.lower() or search in d.lower()}
    if terms:
        st.markdown(f'<div class="icon-head">{icon("book", 40)}<h2>Key terms</h2></div>',
                    unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (term, definition) in enumerate(terms.items()):
            with cols[i % 2].container(border=True):
                st.markdown(f"**{term}**")
                st.write(definition)

    st.caption("The ten languages here are the top 10 home languages of California "
               "English learners. Russian, Farsi, Filipino, Punjabi, and Korean are starter "
               "notes that will grow. Notes summarize published research and do not "
               "replace clinical judgment.")


# ---------------------------------------------------------------- References
SITE_URL = "https://cld-navigator.streamlit.app"


def all_references():
    """Every source the site cites: {full reference: [where it is used]}."""
    import sounds as snd
    used = {}

    def add(src, tag):
        used.setdefault(src, [])
        if tag not in used[src]:
            used[src].append(tag)

    for language, info in load_library().items():
        for src in info.get("sources", []):
            add(src, language)
    for _, _, srcs in MYTHS:
        for src in srcs:
            add(src, "Bilingual development")
    for language, data in SOUND_GAPS.items():
        for src in data["sources"]:
            add(src, "Speech sounds")
    for data in TONES.values():
        for src in data["sources"]:
            add(src, "Speech sounds")
    add(snd.SCHIFF_FULL, "Arabic")
    add(NEW_AMERICA, "Bilingual development")
    add(ASHA_INTERPRETERS, "Assessment")
    import sounds as _s
    for src in (_s.PEARSON_1997_FULL, _s.GIBSON_FULL, PEARSON, PENA_FULL):
        add(src, "Assessment")
    for src in (PEARSON, GENESEE, PHAM_TIPTON, PARADIS):
        add(src, "Family handout")
    return dict(sorted(used.items(), key=lambda kv: kv[0].lower()))


def _linkify(ref):
    return re.sub(r"(https?://\S+?)([.,]?)$",
                  lambda m: f'<a href="{m.group(1)}" target="_blank">{m.group(1)}</a>'
                            f'{m.group(2)}', ref)


def references():
    refs = all_references()
    tags = (["All"] + list(load_library())
            + ["Bilingual development", "Speech sounds", "Assessment", "Family handout"])
    journals = len({r for r in refs if "Journal" in r or "Pathology" in r
                    or "Psychology" in r or "Child Development" in r
                    or "Language Learning" in r or "Services in Schools" in r})
    page_header("References", "Every source CLD Navigator cites, in one list. Filter by "
                "language or topic, and cite the tool in your own work.", "mint",
                PAGE_ART["refs"],
                [f"{len(refs)} sources", f"{journals} journal articles",
                 f"{len(load_library())} languages"])

    st.markdown("""
<div class="std">
  <div><div class="t">Every prompt names its source</div>
  <p>Things to consider, myths, sound charts, and tone charts all list where they
  come from.</p></div>
  <div><div class="t">Gaps are labeled, not hidden</div>
  <p>Two checks use cutoffs this site set. The About page says so next to each one.</p></div>
  <div><div class="t">The SLP decides</div>
  <p>Notes summarize published research. They support clinical judgment and never
  replace it.</p></div>
</div>""", unsafe_allow_html=True)

    pick = st.segmented_control("Show", tags, default="All", key="ref_tag") or "All"
    shown = {r: t for r, t in refs.items() if pick == "All" or pick in t}
    items = "".join(
        f'<li><p>{_linkify(r)}</p><div class="ref-tags">'
        + "".join(f"<span>{t}</span>" for t in t_list) + "</div></li>"
        for r, t_list in shown.items())
    st.markdown(f'<p class="ref-count">{len(shown)} sources</p>'
                f'<ol class="refs">{items}</ol>', unsafe_allow_html=True)

    st.header("Cite CLD Navigator")
    st.markdown('<p class="section-sub" style="margin-top:0">APA 7 format. Select the '
                'copy button in the box.</p>', unsafe_allow_html=True)
    st.code(f"Pham, A. ({date.today().year}). CLD Navigator [Web application]. {SITE_URL}",
            language=None, wrap_lines=True)


# ---------------------------------------------------------------- Feedback
ROLES = ["School SLP", "Clinic or hospital SLP", "SLPA", "Professor or researcher",
         "SLP graduate student", "CSD undergraduate student", "Other"]
FEATURES = ["New Assessment", "Sound Explorer", "Knowledge Library", "Family Interview",
            "Interpreter steps", "Family handout", "Saved Cases", "Insights", "References"]
# Honest review status, shown on the About and Feedback pages. Update as reviews happen.
REVIEW_STATUS = [
    ("Content reviewed by a practicing SLP", "Not yet"),
    ("Vietnamese wording reviewed by a native speaker", "Not yet"),
    ("Other interview translations reviewed by native speakers", "Not yet"),
    ("Tested with real clinicians", "Not yet"),
    ("Every check lists its source", "Yes"),
]


def review_panel():
    rows = "".join(f'<div class="rv-row"><span>{item}</span><b class="{"yes" if s == "Yes" else "no"}">'
                   f'{s}</b></div>' for item, s in REVIEW_STATUS)
    st.markdown(f'<div class="rv">{rows}</div>', unsafe_allow_html=True)


def feedback():
    page_header("Feedback", "SLPs, professors, and students: tell me what works, what's "
                "wrong, and what's missing. Nothing here asks about a child.", "mint",
                PAGE_ART["interview"], ["About 3 minutes", "No names or emails",
                                        "Shapes what gets built next"])

    with st.form("feedback_form", border=False):
        c1, c2 = st.columns(2)
        role = c1.selectbox("Your role", ROLES, index=None, placeholder="Choose one")
        served = c2.text_input("Languages your clients or students speak",
                               placeholder="e.g. Spanish, Vietnamese, Punjabi")
        tried = st.multiselect("Which parts did you try?", FEATURES)
        useful = st.slider("How useful would this be in your work or studies?", 1, 5, 3,
                           help="1 = not useful, 5 = very useful")
        would = st.radio("Would you use CLD Navigator?", ["Yes", "Maybe", "No"],
                         horizontal=True, index=None)
        wrong = st.text_area("Is anything wrong, unclear, or out of date?")
        missing = st.text_area("What's missing that you'd need?")
        sent = st.form_submit_button("Send feedback", type="primary", icon=":material/send:")

    if sent:
        if not role or not would:
            st.error("Please choose your role and whether you'd use it.")
        else:
            with Session() as s:
                s.add(Feedback(role=role, languages_served=served.strip(),
                               tried="; ".join(tried), usefulness=useful, would_use=would,
                               wrong=wrong.strip(), missing=missing.strip()))
                s.commit()
            st.success("Thank you. Your feedback was saved.")

    st.caption("Prefer to write publicly, or want a reply? Open an issue on GitHub at "
               f"{REPO_URL}/issues. On the free hosted site, saved data resets when the "
               "site restarts, so feedback there is downloaded regularly.")

    with Session() as s:
        entries = s.query(Feedback).all()
        rows = [{"date": f.created_at.strftime("%Y-%m-%d"), "role": f.role,
                 "languages": f.languages_served or "", "tried": f.tried or "",
                 "usefulness (1-5)": f.usefulness, "would use": f.would_use,
                 "wrong": f.wrong or "", "missing": f.missing or ""} for f in entries]

    st.header("What reviewers have said")
    if not rows:
        st.markdown('<p class="section-sub" style="margin-top:0">No feedback yet. Be the '
                    'first.</p>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(rows)
        m1, m2, m3 = st.columns(3)
        m1.metric("Responses", len(df), border=True)
        m2.metric("Average usefulness", f"{df['usefulness (1-5)'].mean():.1f} / 5", border=True)
        m3.metric("Would use it", f"{(df['would use'] == 'Yes').mean() * 100:.0f}%", border=True)
        st.download_button("Download all feedback (.csv)", df.to_csv(index=False),
                           file_name="cld_navigator_feedback.csv", mime="text/csv")

    st.header("Review status")
    st.markdown('<p class="section-sub" style="margin-top:0">Where CLD Navigator stands '
                'today. This list changes as people review it.</p>', unsafe_allow_html=True)
    review_panel()


# ---------------------------------------------------------------- About
def about():
    page_header("About", "Who built CLD Navigator, how its checks work, and what it "
                "can't do yet.", "mint", PAGE_ART["about"],
                [f"{len(RULE_TABLE)} checks listed", "Open source"])

    st.markdown(f"""
<div class="hello">
  <div class="hello-mark">{HELLO_SVG}</div>
  <div>
    <p class="hi">I'm Audrey, a Communication Sciences and Disorders student at California
    State University, Fullerton.</p>
    <p>I spoke Vietnamese only at home, and when I started going to an American public
    school, my words were jumbled up. Bilingual children who speak less-common languages
    often get misidentified with speech disorders. I know, because I was one of them.</p>
    <p>I want to make sure that SLPs have appropriate resources to make the best decisions
    for their clientele. CLD Navigator is my start on that.</p>
    <div class="sig">Audrey Pham</div>
  </div>
</div>""", unsafe_allow_html=True)

    library = load_library()
    stats = [(len(library), "home languages"), (len(all_references()), "cited sources"),
             (len(SOUND_GAPS), "sound comparisons"), (len(TONES), "tone charts"),
             (len(INTERVIEW_LANGUAGES), "interview languages"), (len(GLOSSARY), "key terms")]
    stat_icons = ["globe", "book", "chat", "bulb", "calendar", "search"]
    cells = "".join(f'<div>{icon(stat_icons[k % 6], 30)}<b>{n}</b><span>{label}</span></div>'
                    for k, (n, label) in enumerate(stats))
    st.markdown(f'<div class="numbers">{cells}</div>', unsafe_allow_html=True)
    features = [
        "Records a bilingual child's languages, with how much the child hears and speaks "
        "each, and gives cited things to consider",
        "Sound Explorer: English consonants compared with seven home languages, a mouth "
        "map, tone charts, word pairs, and printable sheets",
        f"Knowledge Library: research notes on the top {len(library)} home languages of "
        "California English learners, with a development timeline",
        f"Family interview guide in {len(INTERVIEW_LANGUAGES)} languages, plus interpreter "
        "guidance and a family handout",
        "Saved cases with printable reports, a caseload Insights page, and a References "
        "page with every source",
    ]
    st.download_button("Download a one-page project summary",
                       project_summary_html(
                           stats, features, len(all_references()), SITE_URL, REPO_URL,
                           waffle([(n, i.get("california_share", 0)) for n, i in library.items()],
                                  ["#0E4F57", "#B3205A", "#6B4E9B", "#5E3A26", "#3E8A8A",
                                   "#C9951A", "#8A3B6E", "#3E7A4C", "#B0602A", "#3F5E9C"]),
                           sum(i.get("california_share", 0) for i in library.values())),
                       file_name="cld-navigator-summary.html", mime="text/html",
                       icon=":material/description:",
                       help="For portfolios and applications. Open, then Print > Save as PDF.")

    st.header("Review status")
    st.markdown('<p class="section-sub" style="margin-top:0">An honest look at what has and '
                'hasn\'t been checked yet. Practicing SLPs can help on the Feedback page.</p>',
                unsafe_allow_html=True)
    review_panel()

    st.header("What it is, and what it isn't")
    st.markdown(f"""
<div class="duo">
  <div style="background:var(--plum-50)">{icon("bulb", 44)}<div class="t" style="color:var(--plum)">What it is</div>
  <p>A support tool for speech-language pathologists assessing bilingual children,
  especially children who speak languages with few published tests.</p></div>
  <div style="background:var(--berry-50)">{icon("shield", 44)}<div class="t" style="color:var(--berry)">What it isn't</div>
  <p>It does not diagnose, and it is not a test. The SLP makes every clinical
  decision.</p></div>
</div>""", unsafe_allow_html=True)

    st.header("How the checks work")
    st.markdown('<p class="section-sub" style="margin-top:0">Each prompt comes from a simple '
                'rule. The table lists every rule, when it appears, and its source. Two '
                'checks use cutoffs this site set, 20% exposure and a 30-point gap. The '
                'cited studies back the reasoning behind them, not the exact numbers.</p>',
                unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(RULE_TABLE), hide_index=True, width="stretch")

    st.header("Privacy and limitations")
    st.markdown("""
<div class="lists">
  <div><h3>Privacy</h3><ul>
    <li>Cases use a code, never a name. Codes must include a number.</li>
    <li>Do not enter names or other identifying information about real children.</li>
    <li>The online demo clears saved cases whenever the site restarts.</li></ul></div>
  <div class="warn"><h3>Limitations</h3><ul>
    <li>The rules are not a validated tool.</li>
    <li>The site has not been tested with real clinicians or real cases.</li>
    <li>Notes for Russian, Farsi, Filipino, Punjabi, and Korean are starter notes, with
    less research than the first five languages.</li></ul></div>
</div>""", unsafe_allow_html=True)

    st.header("What I'd improve next")
    st.markdown('<p class="section-sub" style="margin-top:0">Get feedback from practicing '
                'SLPs and more experienced coders, add more languages to the Knowledge '
                'Library, and cite research for every rule.</p>', unsafe_allow_html=True)

    st.header("Built with")
    st.markdown('<div class="stack">' + "".join(
        f"<span>{t}</span>" for t in ["Python", "Streamlit", "SQLAlchemy", "SQLite", "pandas"])
        + "</div>", unsafe_allow_html=True)
    st.link_button("View the source code on GitHub", REPO_URL)
