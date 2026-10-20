# app.py - the website for CLD Navigator

import streamlit as st

from database import Case, Language, Session

st.set_page_config(page_title="CLD Navigator", page_icon="🗣️")
st.title("CLD Navigator")
st.caption("Assessment support for SLPs working with bilingual children")
st.warning("This tool only offers support. The SLP makes all clinical decisions.")

# Menu on the left side
page = st.sidebar.radio("Go to", ["New Assessment", "Saved Cases"])


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
                    st.success(f"Saved {case_code}!")


# ---------- Page 2: list of saved cases ----------
else:
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

                if st.button("Delete this case", key=f"del{case.id}"):
                    s.delete(case)
                    s.commit()
                    st.rerun()
                    