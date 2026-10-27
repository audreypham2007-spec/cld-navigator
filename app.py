# app.py - the website for CLD Navigator

import json
from pathlib import Path

import streamlit as st

from database import Case, Language, Session
from rules import check_percentages, get_considerations

HERE = Path(__file__).parent  # the project folder, so files load on any computer
PAGES = ["Home", "New Assessment", "Saved Cases", "Knowledge Library",
         "About & Limitations"]

st.set_page_config(page_title="CLD Navigator", page_icon="🗣️", layout="centered")

# A little extra styling on top of .streamlit/config.toml
st.markdown("""
<style>
.hero-title {font-size: 2.6rem; font-weight: 700; color: #1F6F78; margin-bottom: 0;}
.hero-sub {font-size: 1.15rem; color: #4A5A5E; margin-top: 0.2rem;}
.footer {color: #6B7A7E; font-size: 0.85rem; text-align: center; margin-top: 3rem;}
</style>
""", unsafe_allow_html=True)


def go_to(page_name):
    """Switch pages when a button is clicked."""
    st.session_state.page = page_name


def load_library():
    """Read the research notes. Returns {} if the file is missing."""
    try:
        with open(HERE / "language_notes.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def case_summary_text(case, tips):
    """Plain-text version of a case, for the download button."""
    lines = [f"CLD Navigator case summary: {case.case_code}",
             f"Age: {case.age_months} months", "", "Languages:"]
    for lang in case.languages:
        lines.append(f"- {lang.name}: hears {lang.percent_hears}%, "
                     f"speaks {lang.percent_speaks}%")
    lines += ["", f"Concerns: {case.concerns or 'None'}",
              f"Notes: {case.notes or 'None'}", "", "Things to consider:"]
    lines += [f"- {tip}" for tip in tips]
    lines += ["", "This summary offers support only. The SLP makes all clinical decisions."]
    return "\n".join(lines)


def show_considerations(tips):
    with st.container(border=True):
        st.markdown("**Things to consider**")
        for tip in tips:
            st.markdown(f"- {tip}")


# ---------- Sidebar ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.markdown("### 🗣️ CLD Navigator")
    st.radio("Go to", PAGES, key="page", label_visibility="collapsed")
    st.divider()
    st.caption("Support tool only. The SLP makes all clinical decisions. "
               "Never enter a child's real name.")

page = st.session_state.page


# ---------- Page 0: home ----------
if page == "Home":
    st.markdown('<p class="hero-title">CLD Navigator</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Assessment support for speech-language '
                'pathologists working with bilingual children, especially children '
                'who speak languages with few published tests.</p>',
                unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    col_a.button("Start a new assessment", type="primary", use_container_width=True,
                 on_click=go_to, args=("New Assessment",))
    col_b.button("Browse the Knowledge Library", use_container_width=True,
                 on_click=go_to, args=("Knowledge Library",))

    st.subheader("Why I built this")
    st.write("Bilingual children who speak less-common languages often get "
             "misidentified with speech disorders. I know, because I was one of them. "
             "I spoke Vietnamese only at home, and when I started going to an American "
             "public school, my words were jumbled up. I want to make sure that SLPs "
             "have appropriate resources to make the best decisions for their clientele.")

    st.subheader("What it does")
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.markdown("**📝 Record exposure**")
        st.write("Log how much a child hears and speaks each language, under a "
                 "case code, never a name.")
    with c2.container(border=True):
        st.markdown("**💡 Things to consider**")
        st.write("See prompts that separate limited exposure from a possible disorder.")
    with c3.container(border=True):
        st.markdown("**📚 Research notes**")
        st.write("Read cited notes on sounds, development, and tools for each language.")

    st.subheader("How to use it")
    st.markdown("""
1. **New Assessment:** enter a case code, the child's age, and each language.
2. **Saved Cases:** review the case and its things to consider. Download a summary.
3. **Knowledge Library:** check the research notes for the child's language.
""")
    st.info("CLD Navigator does not diagnose and is not a test. It has not been "
            "validated with real clinicians or cases.")


# ---------- Page 1: the form ----------
elif page == "New Assessment":
    st.header("New Assessment")
    st.caption("Use a code like CASE-001. Never enter a real name.")

    with st.form("new_case", clear_on_submit=True):
        col_code, col_age = st.columns(2)
        case_code = col_code.text_input("Case code", placeholder="CASE-001")
        age = col_age.number_input("Child's age in months", min_value=0,
                                   max_value=216, value=48)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Language 1**")
            lang1 = st.text_input("Language name", key="lang1",
                                  placeholder="e.g. Vietnamese")
            hears1 = st.slider("% of the time the child HEARS it", 0, 100, 50, key="h1")
            speaks1 = st.slider("% of the time the child SPEAKS it", 0, 100, 50, key="s1")
        with col2:
            st.markdown("**Language 2 (optional)**")
            lang2 = st.text_input("Language name", key="lang2",
                                  placeholder="e.g. English")
            hears2 = st.slider("% of the time the child HEARS it", 0, 100, 50, key="h2")
            speaks2 = st.slider("% of the time the child SPEAKS it", 0, 100, 50, key="s2")

        concerns = st.text_area("Concerns from family or teacher")
        notes = st.text_area("Clinician notes")

        submitted = st.form_submit_button("Save case", type="primary")

    if submitted:
        case_code = case_code.strip().upper()
        lang1, lang2 = lang1.strip(), lang2.strip()

        languages = [Language(name=lang1, percent_hears=hears1, percent_speaks=speaks1)]
        if lang2:
            languages.append(Language(name=lang2, percent_hears=hears2,
                                      percent_speaks=speaks2))
        problems = check_percentages(languages)

        if not case_code or not lang1:
            st.error("Please fill in the case code and at least one language.")
        elif problems:
            for problem in problems:
                st.error(problem)
        else:
            with Session() as s:
                if s.query(Case).filter_by(case_code=case_code).first():
                    st.error(f"{case_code} already exists. Use a different code.")
                else:
                    case = Case(case_code=case_code, age_months=age,
                                concerns=concerns, notes=notes)
                    case.languages.extend(languages)
                    s.add(case)
                    s.commit()
                    st.success(f"Saved {case_code}! It's on the Saved Cases page.")
                    show_considerations(get_considerations(case))


# ---------- Page 2: saved cases ----------
elif page == "Saved Cases":
    st.header("Saved Cases")

    with Session() as s:
        cases = s.query(Case).order_by(Case.created_at.desc()).all()

        if not cases:
            st.info("No cases yet. Add one on the New Assessment page.")
            st.button("Start a new assessment", type="primary",
                      on_click=go_to, args=("New Assessment",))
        else:
            all_languages = {lang.name.title() for c in cases for lang in c.languages}
            m1, m2 = st.columns(2)
            m1.metric("Cases", len(cases))
            m2.metric("Languages represented", len(all_languages))

            search = st.text_input("Search by case code or language", "").strip().lower()
            shown = [c for c in cases
                     if not search
                     or search in c.case_code.lower()
                     or any(search in lang.name.lower() for lang in c.languages)]
            if not shown:
                st.warning("No cases match that search.")

            for case in shown:
                tips = get_considerations(case)
                langs = ", ".join(lang.name for lang in case.languages)
                with st.expander(f"{case.case_code}  ·  {case.age_months} months  ·  {langs}"):
                    for lang in case.languages:
                        st.markdown(f"**{lang.name}**")
                        st.progress(lang.percent_hears / 100,
                                    text=f"Hears {lang.percent_hears}%")
                        st.progress(lang.percent_speaks / 100,
                                    text=f"Speaks {lang.percent_speaks}%")
                    st.write("**Concerns:**", case.concerns or "None")
                    st.write("**Notes:**", case.notes or "None")
                    show_considerations(tips)

                    st.download_button("Download summary (.txt)",
                                       case_summary_text(case, tips),
                                       file_name=f"{case.case_code}.txt",
                                       key=f"dl{case.id}")

                    sure = st.checkbox("I want to delete this case", key=f"sure{case.id}")
                    if st.button("Delete this case", key=f"del{case.id}", disabled=not sure):
                        s.delete(case)
                        s.commit()
                        st.rerun()


# ---------- Page 3: knowledge library ----------
elif page == "Knowledge Library":
    st.header("Knowledge Library")
    st.write("Research notes on assessing children who speak each language. "
             "Every note lists its sources.")

    library = load_library()
    if not library:
        st.warning("No research notes found. Check that language_notes.json is in "
                   "the project folder.")

    for language, info in library.items():
        with st.expander(f"{language}", expanded=len(library) == 1):
            if info.get("summary"):
                st.info(info["summary"])

            sections = info.get("sections")
            if sections:
                tabs = st.tabs(list(sections.keys()))
                for tab, text in zip(tabs, sections.values()):
                    tab.write(text)
            else:
                st.write(info.get("notes") or "No notes yet.")

            if info.get("sources"):
                st.markdown("**Sources**")
                for source in info["sources"]:
                    st.markdown(f"- {source}")

    st.caption("More languages coming soon. Notes summarize published research "
               "and do not replace clinical judgment.")


# ---------- Page 4: about & limitations ----------
else:
    st.header("About & Limitations")
    st.markdown("""
**What this tool is:** a support tool for speech-language pathologists (SLPs)
assessing bilingual children, especially children who speak languages with
few published tests.

**What it does:** saves case information, shows things to consider about each
child's language exposure, and collects research notes on different languages.

**What it does NOT do:** it does not diagnose, and it is not a test. The SLP
makes every clinical decision.

**Limitations:**
- The "things to consider" are simple rules, not a validated tool.
- It has not been tested with real clinicians or real cases.
- Do not enter names or other identifying information about real children.
- The online demo resets its saved cases whenever the site restarts.
""")

    st.subheader("Built with")
    st.write("Python, Streamlit, SQLAlchemy, SQLite")


st.markdown('<p class="footer">Built by Audrey Pham · Communication Sciences and '
            'Disorders, Cal State Fullerton</p>', unsafe_allow_html=True)
