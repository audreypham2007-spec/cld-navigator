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
    "errors": st.Page(views.error_check, title="Error Check", icon=":material/rule:",
                      url_path="error-check"),
    "assess": st.Page(views.assess, title="New Assessment", icon=":material/edit_note:",
                      url_path="new-assessment"),
    "cases": st.Page(views.saved_cases, title="Saved Cases", icon=":material/folder_open:",
                     url_path="saved-cases"),
    "interview": st.Page(views.interview, title="Family Interview", icon=":material/family_restroom:",
                         url_path="family-interview"),
    "insights": st.Page(views.insights, title="Insights", icon=":material/bar_chart:",
                        url_path="insights"),
    "sounds": st.Page(views.sound_explorer, title="Sound Explorer", icon=":material/graphic_eq:",
                      url_path="sound-explorer"),
    "library": st.Page(views.library, title="Knowledge Library", icon=":material/menu_book:",
                       url_path="knowledge-library"),
    "refs": st.Page(views.references, title="References", icon=":material/format_quote:",
                    url_path="references"),
    "feedback": st.Page(views.feedback, title="Feedback", icon=":material/rate_review:",
                        url_path="feedback"),
    "about": st.Page(views.about, title="About", icon=":material/info:", url_path="about"),
})

# Group the menu so it stays short: Learn comes first, since the reference
# material is the heart of the site.
MENU = {
    "": [PAGES["home"], PAGES["about"], PAGES["feedback"]],
    "Learn": [PAGES["sounds"], PAGES["library"], PAGES["refs"]],
    "Assess": [PAGES["errors"], PAGES["assess"], PAGES["interview"], PAGES["cases"],
               PAGES["insights"]],
}
page = st.navigation(MENU, position="top")
announcement_bar()
page.run()
footer()
