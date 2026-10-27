# CLD Navigator

A support tool for speech-language pathologists (SLPs) assessing bilingual
children, especially children who speak languages with few published tests.

## Why I built this
Bilingual children who speak less-common languages often get misidentified
with speech disorders. I know, because I was one of them. I spoke Vietnamese
only at home, and when I started going to an American public school, my words
were jumbled up. I want to make sure that SLPs have appropriate resources to
make the best decisions for their clientele.

## What it does
- Saves case information using a code, never a child's name
- Checks that language exposure percentages add up
- Shows "things to consider" about each child's language exposure
- Lets the SLP download a plain-text summary of each case
- Collects cited research notes on assessing different languages
- Always reminds the SLP that they make the clinical decisions

## What it does NOT do
It does not diagnose and is not a test. It has not been validated with real
clinicians or cases.

## Built with
Python, Streamlit, SQLAlchemy, SQLite

## Project files
| File | What it does |
|---|---|
| `app.py` | The website pages |
| `database.py` | Saves cases and languages |
| `rules.py` | The "things to consider" checks |
| `language_notes.json` | Research notes for the Knowledge Library |
| `.streamlit/config.toml` | Site colors and font |

## What I'd improve next
I would like to get feedback from practicing SLPs, as well as more experienced
coders, to improve my website. I would love to add more languages to the
knowledge library, as well as cite research for every rule.

## Run it yourself
    pip install -r requirements.txt
    streamlit run app.py
