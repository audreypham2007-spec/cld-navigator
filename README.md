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
- Error Check: enter a child's English sound errors and error patterns plus the home language, and the site sorts each one into consistent with the home language (with its source), look closer, or no data. Nothing is saved, and the result downloads as a printable page
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
- Family Interview page explains ASHA's briefing, interaction, and debriefing steps for working with interpreters, and offers a printable family handout on raising a bilingual child
- About page shows the project by the numbers and downloads a one-page project summary for portfolios
- Feedback page for SLPs, professors, and students, with a downloadable summary
- Vietnamese session phrases in the Knowledge Library (draft, pending native-speaker review)
- Insights page charts patterns across all saved cases
- Sound Explorer compares English consonants with Spanish, Vietnamese, Arabic, Cantonese, Farsi, Filipino, and Punjabi, shows a cross-language matrix, draws the tones of Vietnamese, Mandarin, and Cantonese, and diagrams Arabic diglossia, with cited sources
- Sound Explorer mouth map places all 24 English consonants from the lips to the throat
- Sound Explorer word pairs (English minimal pairs) for each missing sound, and a quick self-check quiz
- Hand-drawn people: SLP personas, a bilingual child in the story section, a session scene on the Family Interview page, and friendly empty states
- All printables share a branded design: header band, cards, and the site's fonts and colors
- Printable one-page sound sheet for each language, from the Sound Explorer
- Saved cases, new cases, and printable reports list the English sounds each home language doesn't use; Insights charts them across the caseload
- Knowledge Library timeline shows when children in each cited study mastered key sounds
- Home page picture grid of every tool, waffle chart of California English learners, and a deck of sourced fun facts
- References page collects every source the site cites, filterable by language and topic, with an APA citation for the tool
- Home page lists five myths about bilingual children next to what peer-reviewed research says
- Loads five made-up demo cases so visitors can try the site
- Collects cited research notes on assessing different languages, covering the top 10 home languages of California English learners: Spanish, Vietnamese, Mandarin, Arabic, Cantonese, and starter notes for Russian, Farsi, Filipino, Punjabi, and Korean, plus a glossary of key terms, with search
- Lists every rule and its source on the About page

## Privacy
The New Assessment page can run every check without saving anything. Saved cases are for practice and demos, use a code instead of a name, and can all be deleted at once. Do not enter information that could identify a real child.

## Review status
Not yet reviewed by a practicing SLP or tested with real clinicians. The Feedback page collects reviews from SLPs, professors, and students. Two checks use cutoffs this site set (20% exposure, a 30-point hears/speaks gap); the cited studies support the reasoning, not the exact numbers.

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
| `sounds.py` | Sound Explorer data, Error Check patterns, and the home page myths, with sources |
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
