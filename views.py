# views.py - one function per page of the website.

import re

import pandas as pd
import streamlit as st

from common import (GOLD, PAGES, REPO_URL, TEAL, case_summary_text, chunk, exposure_key,
                    load_library, page_header, show_considerations, years_months)
from content import (GLOSSARY, INTERVIEW_LABELS, INTERVIEW_LANGUAGES, RTL_CODES,
                     interview_lines)
from art import BUBBLES_SVG, PAGE_ART
from database import Case, Language, Session
from report import case_report_html, interview_html
from rules import RULE_TABLE, check_percentages, get_considerations
from sample_data import load_demo_cases

MAX_LANGUAGES = 4

# The six Vietnamese tones on the syllable "ma", with common meanings.
TONE_WORDS = [("ma", "ghost"), ("má", "mother"), ("mà", "but"),
              ("mả", "grave"), ("mã", "horse"), ("mạ", "rice seedling")]

# Each language's name in its own writing system.
RTL = ' dir="rtl"'
LANG_COLORS = ["#B3205A", "#0E4F57", "#B98A0E", "#6B4E9B", "#5E3A26"]

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
}
# Card backgrounds and text colors (dark cards get white text).
TINT_BG = ["#F9E3EB", "#E2EEEE", "#F3EAE3", "#EEE8F5", "#EEF1F4"]
CARD_INK = ["#B3205A", "#0E4F57", "#5E3A26", "#6B4E9B", "#1C2B33"]
AUTONYMS = {"Spanish": "Español", "Vietnamese": "Tiếng Việt", "Mandarin": "普通话",
            "Arabic": "العربية", "Cantonese": "廣東話"}

STEPS = [
    ("Record the child's languages",
     "Enter how much the child hears and speaks each language. Not sure? The "
     "calculator turns a family's weekly routine into percentages."),
    ("Read the things to consider",
     "Each case gets prompts that separate limited exposure from a possible "
     "disorder. Every prompt names its source."),
    ("Check the research",
     "The Knowledge Library covers sounds, development, and tests for each "
     "home language, with citations."),
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


# ---------------------------------------------------------------- Home
def home():
    library = load_library()
    sources = len({src for info in library.values() for src in info.get("sources", [])})
    coverage = sum(info.get("california_share", 0) for info in library.values())

    hero = st.container(key="hero")
    left, right = hero.columns([1.15, 0.85], gap="large", vertical_alignment="center")
    with left:
        st.markdown("""
<div class="home-title">Is it a language difference, or a disorder?</div>
<p class="home-lede">Enter a bilingual child's languages and get research-backed
things to consider in a few minutes, each with a source you can cite.</p>
""", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        if b1.button("Start an assessment", type="primary", width="stretch"):
            st.switch_page(PAGES["assess"])
        if b2.button("Try a demo case, 1 click", width="stretch"):
            with Session() as s:
                load_demo_cases(s)
            st.switch_page(PAGES["cases"])
        st.markdown(f"""
<div class="facts"><span>Free, no account</span><span>{len(library)} languages</span>
<span>{sources} cited sources</span><span>{coverage:.0f}% of CA English learners</span></div>""", unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="home-art">{BUBBLES_SVG}</div>', unsafe_allow_html=True)

    st.header("Two mistakes, both costly")
    st.markdown(f"""
<div class="risks">
  <div class="risk r1"><div class="risk-title">A difference called a disorder</div>
  <p>A child still learning English gets placed in services they don't need.</p></div>
  <div class="risk r2"><div class="risk-title">A disorder called a difference</div>
  <p>A child with a real disorder waits for help because the struggle gets blamed
  on learning English.</p></div>
  <div class="risk-quote">"Schools across the nation both over- and under-identify ELs
  with disabilities," partly because "several features of language learning mimic
  those associated with certain disabilities."<span class="pv-src">{NEW_AMERICA}</span></div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="bigstat"><div class="n">{coverage:.0f}%</div>
<div><div class="t">of California English learners speak one of the {len(library)} home
languages in the Knowledge Library.</div>
<div class="s">Spanish {library.get("Spanish", {}).get("california_share", 0):.1f}%, then
Vietnamese, Mandarin, Arabic, and Cantonese. California Department of Education,
2022-23.</div></div></div>""", unsafe_allow_html=True)

    st.header("How it works")
    steps = "".join(f'<div class="step c{i}"><div class="num">{i}</div>'
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

    story = st.container(key="story")
    story.header("Why I built this")
    story.markdown("""
<div class="quote">
<p>"Bilingual children who speak less-common languages often get misidentified with
speech disorders. I know, because I was one of them. I spoke Vietnamese only at home,
and when I started going to an American public school, my words were jumbled up."</p>
<div class="sign">Audrey Pham</div>
<div class="role">Communication Sciences and Disorders, California State University, Fullerton</div>
</div>
""", unsafe_allow_html=True)

    if library:
        st.header("Explore by language")
        st.markdown('<p class="section-sub">Researched, cited, and written for the SLP '
                    'in the room. Ranked by share of California English learners. Swipe '
                    'to see all five.</p>', unsafe_allow_html=True)
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
                f'{RTL if name == "Arabic" else ""}>{AUTONYMS.get(name, name)}</div>'
                f'<div class="card-name">{name}</div>'
                f'<div class="card-text">{first}</div>'
                f'<div class="card-link" style="color:{color}">Read the research</div></a>')
        st.markdown(f'<div class="carousel">{"".join(cards)}</div>', unsafe_allow_html=True)
        st.caption("Spanish alone is the home language of 81.9% of California English "
                   "learners (California Department of Education, 2022-23).")

    st.header("Built for")
    st.markdown("""
<div class="personas">
  <div class="persona"><div class="who" style="color:#0E4F57">School SLPs</div>
  <p>Sort out a referral for a bilingual student before the IEP meeting, with sources
  you can cite.</p></div>
  <div class="persona"><div class="who" style="color:#B3205A">Clinic SLPs</div>
  <p>Walk into an evaluation knowing what's typical for the child's home language and
  age.</p></div>
  <div class="persona"><div class="who" style="color:#6B4E9B">SLP grad students</div>
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
Knowledge Library. The About page shows which checks have a citation and which are
still placeholders.</p></details>
<details><summary>Which languages are covered?</summary>
<p>Spanish, Vietnamese, Mandarin, Arabic, and Cantonese. Russian, Farsi, Filipino,
Punjabi, and Korean are next.</p></details>
</div>""", unsafe_allow_html=True)

    cta = st.container(key="cta")
    c1, c2 = cta.columns([1.6, 1], vertical_alignment="center")
    c1.markdown('<div class="cta-title">See what CLD Navigator finds for a real-looking '
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
                "Four short steps. You get research-backed things to consider the "
                "moment you save.", "mint", PAGE_ART["assess"],
                ["A few minutes", "Saved under a code", "Edit anytime"])

    if st.session_state.pop("reset_pending", False):
        reset_form()
    for key, value in form_defaults().items():
        st.session_state.setdefault(key, value)

    chunk(1, "Languages the child hears", "mint",
          "Pick how many, then fill in each one below. Not sure of the percentages? "
          "Use the calculator.")
    count = st.segmented_control("How many languages does the child hear?",
                                 list(range(1, MAX_LANGUAGES + 1)),
                                 key="lang_count") or 1
    exposure_calculator()

    with st.form("new_case", border=False):
        chunk(2, "About the child", "butter",
              "Use a code like CASE-001. Codes need at least one number, so a real "
              "name can't be saved by mistake.")
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
        submitted = st.form_submit_button("Save case", type="primary")

    if submitted:
        save_new_case(count)

    just_saved = st.session_state.pop("just_saved", None)
    if just_saved:
        with Session() as s:
            case = s.query(Case).filter_by(case_code=just_saved).first()
            if case:
                st.success(f"Saved {just_saved}. The form is ready for the next case.")
                show_considerations(get_considerations(case, load_library().keys()))
        st.page_link(PAGES["cases"], label="See all saved cases", icon=":material/folder_open:")


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
    page_header("Saved Cases", "Every case you've saved, with its exposure chart, "
                "things to consider, and printable report.", "butter", PAGE_ART["cases"],
                ["Print or save as PDF", "Spreadsheet export", "Search and sort"])
    library_names = load_library().keys()

    with Session() as s:
        if st.button("Load demo cases", help="Adds five made-up cases to try the site."):
            added = load_demo_cases(s)
            st.toast(f"Added {added} demo cases." if added
                     else "Demo cases are already loaded.")

        cases = s.query(Case).all()
        if not cases:
            st.info("No cases yet. Add one on the New Assessment page, or load the "
                    "demo cases above.")
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

                b1, b2, b3 = st.columns(3)
                b1.download_button("Printable report",
                                   case_report_html(case, tips, years_months),
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
    for title, lines in sections:
        with st.container(border=True):
            items = ""
            for main, english in lines:
                eng = (f'<div class="q-en" dir="ltr">{english}</div>' if english else "")
                items += f'<li value="{number}">{main}{eng}</li>'
                number += 1
            st.markdown(f'<div class="q-block"{direction}><div class="q-title">{title}'
                        f'</div><ol>{items}</ol></div>', unsafe_allow_html=True)

    st.caption("Use a trained interpreter when the family prefers a language you "
               "don't speak.")


# ---------------------------------------------------------------- Insights
def insights():
    page_header("Insights", "Patterns across every saved case: which languages, which "
                "ages, and where children hear a language more than they speak it.",
                "sky", PAGE_ART["insights"], ["Updates as you save", "Caseload view"])

    with Session() as s:
        cases = s.query(Case).all()
        if not cases:
            st.info("No cases yet. Load the demo cases on the Saved Cases page.")
            st.page_link(PAGES["cases"], label="Open Saved Cases", icon=":material/folder_open:")
            return
        rows = [{"case": c.case_code, "age_months": c.age_months,
                 "language": l.name.title(), "hears": l.percent_hears or 0,
                 "speaks": l.percent_speaks or 0, "languages_on_case": len(c.languages)}
                for c in cases for l in c.languages]
        tips = {c.case_code: get_considerations(c, load_library().keys())
                for c in cases}

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

    with st.container(border=True):
        st.markdown("**Most common things to consider**")
        counts = pd.Series([x["text"].split(".")[0] for t in tips.values() for x in t
                            if x["kind"] != "general"]).value_counts()
        if counts.empty:
            st.write("Only general reminders so far.")
        else:
            st.dataframe(counts.rename_axis("Prompt").reset_index(name="Cases"),
                         hide_index=True, width="stretch")


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
                f'{RTL if language == "Arabic" else ""}>{AUTONYMS.get(language, language)}'
                f'</span><span class="english">{language}</span></div>'
                + (f'<div class="lib-share">{info["california_share"]:.2f}% of California '
                   'English learners have this home language (California Department of '
                   'Education, 2022-23)</div>' if info.get("california_share") else "")
                + (f'<p class="lib-summary">{info["summary"]}</p>'
                   if info.get("summary") else ""), unsafe_allow_html=True)
            if language == "Vietnamese":
                tone_strip()
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
        st.header("Key terms")
        cols = st.columns(2)
        for i, (term, definition) in enumerate(terms.items()):
            with cols[i % 2].container(border=True):
                st.markdown(f"**{term}**")
                st.write(definition)

    st.caption("Coming next: Russian, Farsi, Filipino (Tagalog), Punjabi, and Korean, "
               "the rest of the top 10 home languages of California English learners. "
               "Notes summarize published research and do not replace clinical judgment.")


# ---------------------------------------------------------------- About
def about():
    page_header("About", "What CLD Navigator is, how its checks work, and what it "
                "can't do yet.", "mint", PAGE_ART["about"],
                [f"{len(RULE_TABLE)} checks listed", "Open source"])
    st.markdown("""
<div class="duo">
  <div style="background:#EEE8F5"><div class="t" style="color:#6B4E9B">What it is</div>
  <p>A support tool for speech-language pathologists assessing bilingual children,
  especially children who speak languages with few published tests.</p></div>
  <div style="background:#F9E3EB"><div class="t" style="color:#B3205A">What it isn't</div>
  <p>It does not diagnose, and it is not a test. The SLP makes every clinical
  decision.</p></div>
</div>""", unsafe_allow_html=True)

    st.header("How the checks work")
    st.write("Each prompt comes from a simple rule. The table lists every rule, when "
             "it appears, and its source. Rules marked \"citation in progress\" use "
             "placeholder cutoffs I still need to back with research.")
    st.dataframe(pd.DataFrame(RULE_TABLE), hide_index=True, width="stretch")

    st.header("Privacy")
    st.markdown("""
- Cases use a code, never a name. Codes must include a number.
- Do not enter names or other identifying information about real children.
- The online demo clears saved cases whenever the site restarts.
""")

    st.header("Limitations")
    st.markdown("""
- The rules are not a validated tool.
- The site has not been tested with real clinicians or real cases.
- The Knowledge Library covers Spanish, Vietnamese, Mandarin, Arabic, and Cantonese so far.
""")

    st.header("What I'd improve next")
    st.write("Get feedback from practicing SLPs and more experienced coders, add "
             "more languages to the Knowledge Library, and cite research for every rule.")

    st.header("Built with")
    st.write("Python, Streamlit, SQLAlchemy, SQLite, pandas")
    st.link_button("View the source code on GitHub", REPO_URL)
