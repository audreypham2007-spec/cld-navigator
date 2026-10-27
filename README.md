# CLD Navigator

A support tool for speech-language pathologists (SLPs) assessing bilingual
children, especially children who speak languages with few published tests.

**Live site:** https://cld-navigator.streamlit.app

## Why I built this
Bilingual children who speak less-common languages often get misidentified
with speech disorders. I know, because I was one of them. I spoke Vietnamese
only at home, and when I started going to an American public school, my words
were jumbled up. I want to make sure that SLPs have appropriate resources to
make the best decisions for their clientele.

## What it does
- Saves case information using a code, never a child's name (codes must include a number)
- Records up to four languages per child, with how much the child hears and speaks each one
- Exposure calculator turns a family's weekly routine into hears and speaks percentages
- Checks that exposure percentages add up and that no language is entered twice
- Shows "things to consider" for each case, grouped by type, each with its source
- Research-backed checks for Vietnamese, Spanish, Arabic, Cantonese, and Mandarin
- Charts each child's language exposure
- Searches, sorts, and edits saved cases
- Downloads a printable report for each case, or all cases as a spreadsheet (.csv)
- Builds a printable family language interview in English, Spanish, Vietnamese, Simplified or Traditional Chinese, or Arabic, with optional English under each question
- Insights page charts patterns across all saved cases
- Loads five made-up demo cases so visitors can try the site
- Collects cited research notes on assessing different languages, covering Spanish, Vietnamese, Mandarin, Arabic, and Cantonese (the top five home languages of California English learners), plus a glossary of key terms, with search
- Lists every rule and its source on the About page

## What it does NOT do
It does not diagnose and is not a test. It has not been validated with real
clinicians or cases.

## Built with
Python, Streamlit, SQLAlchemy, SQLite, pandas

## Project files
| File | What it does |
|---|---|
| `app.py` | Starts the site and sets up the page menu |
| `views.py` | One function per page |
| `content.py` | Family interview questions and glossary terms |
| `report.py` | Printable reports |
| `common.py` | Shared styling, footer, and helpers |
| `rules.py` | The "things to consider" checks and their sources |
| `database.py` | Saves cases and languages |
| `sample_data.py` | The made-up demo cases |
| `language_notes.json` | Research notes for the Knowledge Library |
| `.streamlit/config.toml` | Site colors and font |

## What I'd improve next
I would like to get feedback from practicing SLPs, as well as more experienced
coders, to improve my website. I would love to add more languages to the
knowledge library, as well as cite research for every rule.

## Run it yourself
    pip install -r requirements.txt
    streamlit run app.py
