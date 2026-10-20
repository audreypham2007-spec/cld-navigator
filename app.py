# app.py - the website for CLD Navigator

import json

import streamlit as st

from database import Case, Language, Session
from rules import get_considerations

st.set_page_config(page_title="CLD Navigator", page_icon="🗣️")
st.title("CLD Navigator")
st.caption("Assessment support for SLPs working with bilingual children")
st.warning("This tool only offers support. The SLP makes all clinical decisions.")

page = st.sidebar.radio("Go to", ["New Assessment", "Saved Cases",
                                  "Knowledge Library", "About & Limitations"])


# ---------- Page 1: the form ----------
if page == "New Assessment":
    st.header("New Assessment")

    with st.form("new_case", clear_on_submit=True):
        case_code = st.text_input("Case code (never a real name)", placeholder="CASE-001")
        age = st.number_input("Child's age in months", min_value=0, max_value=216, value=48)

        st.subheader("Language 1")
        lang1 = st.text_input("Language name", key="lang1")
        hears1 = st.slider("% of the time the child HEARS it", 0, 100, 50, key="h1")
        speaks1 = st.slider("% of the time the child SPEAKS it", 0, 100, 50, key="s1")

        st.subheader("Language 2 (optional)")
        lang2 = st.text_input("Language name", key="lang2")
        hears2 = st.slider("% of the time the child HEARS it", 0, 100, 50, key="h2")
        speaks2 = st.slider("% of the time the child SPEAKS it", 0, 100, 50, key="s2")

        concerns = st.text_area("Concerns from family or teacher")
        notes = st.text_area("Clinician notes")

        submitted = st.form_submit_button("Save case")

    if submitted:
        if not case_code or not lang1:
            st.error("Please fill in the case code and at least one language.")
        else:
            with Session() as s:
                if s.query(Case).filter_by(case_code=case_code).first():
                    st.error(f"{case_code} already exists. Use a different code.")
                else:
                    case = Case(case_code=case_code, age_months=age,
                                concerns=concerns, notes=notes)
                    case.languages.append(Language(name=lang1, percent_hears=hears1,
                                                   percent_speaks=speaks1))
                    if lang2:
                        case.languages.append(Language(name=lang2, percent_hears=hears2,
                                                       percent_speaks=speaks2))
                    s.add(case)
                    s.commit()
                    st.success(f"Saved {case_code}! See it on the Saved Cases page.")


# ---------- Page 2: saved cases ----------
elif page == "Saved Cases":
    st.header("Saved Cases")

    with Session() as s:
        cases = s.query(Case).order_by(Case.created_at.desc()).all()

        if not cases:
            st.info("No cases yet. Add one on the New Assessment page.")

        for case in cases:
            with st.expander(f"{case.case_code}  ·  {case.age_months} months"):
                for lang in case.languages:
                    st.write(f"**{lang.name}**: hears {lang.percent_hears}%, "
                             f"speaks {lang.percent_speaks}%")
                st.write("**Concerns:**", case.concerns or "None")
                st.write("**Notes:**", case.notes or "None")

                st.write("**Things to consider:**")
                for tip in get_considerations(case):
                    st.write("•", tip)

                if st.button("Delete this case", key=f"del{case.id}"):
                    s.delete(case)
                    s.commit()
                    st.rerun()


# ---------- Page 3: knowledge library ----------
elif page == "Knowledge Library":
    st.header("Knowledge Library")
    st.write("Research notes on assessing children who speak each language.")

    try:
        with open("language_notes.json", encoding="utf-8") as f:
            library = json.load(f)
    except FileNotFoundError:
        library = {}

    for language, info in library.items():
        with st.expander(language):
            st.write(info.get("notes") or "No notes yet.")
            if info.get("sources"):
                st.write("**Sources:**")
                for source in info["sources"]:
                    st.write("•", source)


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
""")