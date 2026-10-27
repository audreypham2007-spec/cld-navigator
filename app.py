# app.py - the starting point for CLD Navigator.
# Run it with:  streamlit run app.py
# Each page lives in views.py. Shared styling and helpers live in common.py.

import streamlit as st

import views
from common import PAGES, announcement_bar, apply_style, footer

st.set_page_config(page_title="CLD Navigator", page_icon=":material/record_voice_over:", layout="centered")
apply_style()

# Every page gets its own web address, like /knowledge-library
PAGES.update({
    "home": st.Page(views.home, title="Home", icon=":material/home:", default=True),
    "assess": st.Page(views.assess, title="New Assessment", icon=":material/edit_note:",
                      url_path="new-assessment"),
    "cases": st.Page(views.saved_cases, title="Saved Cases", icon=":material/folder_open:",
                     url_path="saved-cases"),
    "interview": st.Page(views.interview, title="Family Interview", icon=":material/family_restroom:",
                         url_path="family-interview"),
    "insights": st.Page(views.insights, title="Insights", icon=":material/bar_chart:",
                        url_path="insights"),
    "library": st.Page(views.library, title="Knowledge Library", icon=":material/menu_book:",
                       url_path="knowledge-library"),
    "about": st.Page(views.about, title="About", icon=":material/info:", url_path="about"),
})

page = st.navigation(list(PAGES.values()), position="top")
announcement_bar()
page.run()
footer()
