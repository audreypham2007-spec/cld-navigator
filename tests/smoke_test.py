"""Smoke test: opens every page of CLD Navigator in Streamlit's test runner and reports errors.

Run it from the project folder:
    python tests/smoke_test.py

It works on a temporary copy of the project, so your saved cases are never touched.
"""
import os
import shutil
import sys
import tempfile

from streamlit.testing.v1 import AppTest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["home", "error_check", "assess", "saved_cases", "interview", "insights",
         "sound_explorer", "library", "references", "feedback", "about"]

# Page keys used by links between pages, and the view function each one runs
LINKS = {"home": "home", "errors": "error_check", "assess": "assess", "cases": "saved_cases",
         "interview": "interview", "insights": "insights", "sounds": "sound_explorer",
         "library": "library", "refs": "references", "feedback": "feedback", "about": "about"}

SCRIPT = '''
import os, sys
sys.path.insert(0, {tmp!r}); os.chdir({tmp!r})
import streamlit as st
import views
from common import PAGES, apply_style, footer
apply_style()
for key, fn in {links!r}.items():
    PAGES.setdefault(key, st.Page(getattr(views, fn), title=key, url_path=key))
views.{fn}()
footer()
'''


def main():
    tmp = tempfile.mkdtemp()
    for name in os.listdir(REPO):
        path = os.path.join(REPO, name)
        if os.path.isfile(path):
            shutil.copy(path, tmp)
    failed = 0
    for fn in PAGES:
        at = AppTest.from_string(SCRIPT.format(tmp=tmp, fn=fn, links=LINKS), default_timeout=60)
        try:
            at.run()
            problems = [str(e.value) for e in at.exception]
        except Exception as e:  # the page could not even start
            problems = [f"{type(e).__name__}: {e}"]
        status = "PASS" if not problems else "FAIL"
        failed += bool(problems)
        print(f"{status}  {fn}")
        for p in problems:
            print("      " + p[:500])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(PAGES) - failed} of {len(PAGES)} pages passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
