# rules.py - simple checks that give the SLP things to consider.
# These NEVER diagnose. Every rule lists where it comes from, so the SLP
# can judge how much weight to give it.

LOW_EXPOSURE = 20  # percent. TODO: confirm this cutoff in research and cite it
BIG_GAP = 30       # percent. TODO: confirm and cite
VIETNAMESE_AGE_CUTOFF = 72  # months (age 6). From Phạm & McLeod (2019)

CITATION_PENDING = "Placeholder rule. Research citation in progress."
PHAM_MCLEOD = ("Phạm, B., & McLeod, S. (2019). Journal of Speech, Language, "
               "and Hearing Research.")
ASHA_VIETNAMESE = "ASHA. (n.d.). Vietnamese phonemic inventory."
PRATH = "Prath, S. (n.d.). Quick rules: Spanish phonology. Bilinguistics."
GOLDSTEIN = ("Goldstein, B., Fabiano, L., & Washington, P. (2005). Language, Speech, "
             "and Hearing Services in Schools.")
SCHIFF = "Schiff, R., & Saiegh-Haddad, E. (2018). Frontiers in Psychology."
SO_DODD = "So, L. K. H., & Dodd, B. J. (1995). Journal of Child Language."
HUA_DODD = "Hua, Z., & Dodd, B. (2000). Journal of Child Language."


def is_lang(name, *words):
    return (name or "").strip().lower() in words


def is_vietnamese(name):
    name = (name or "").strip().lower()
    return name.startswith("vietnam") or name in {"tiếng việt", "tieng viet"}


def is_english(name):
    return (name or "").strip().lower() == "english"


def check_percentages(languages):
    """Return a warning if the 'hears' or 'speaks' numbers add up to more than 100%."""
    warnings = []
    total_hears = sum(lang.percent_hears or 0 for lang in languages)
    total_speaks = sum(lang.percent_speaks or 0 for lang in languages)
    if total_hears > 100:
        warnings.append(f"The 'hears' numbers add up to {total_hears}%. "
                        "They should add up to 100% or less.")
    if total_speaks > 100:
        warnings.append(f"The 'speaks' numbers add up to {total_speaks}%. "
                        "They should add up to 100% or less.")
    return warnings


def tip(text, kind, source=None):
    """One 'thing to consider'. kind is 'language', 'exposure', or 'general'."""
    return {"text": text, "kind": kind, "source": source}


def get_considerations(case, library_languages=()):
    """Build the list of things to consider for one case."""
    tips = []
    names = [lang.name for lang in case.languages]

    # --- Language-specific research (backed by the Knowledge Library) ---
    if any(is_vietnamese(n) for n in names) and case.age_months < VIETNAMESE_AGE_CUTOFF:
        tips.append(tip(
            "Northern Vietnamese-speaking children had acquired nearly all Vietnamese "
            "sounds and tones by about age 5;5 to 5;11. Exceptions were initial "
            "/ɲ, s, z, x/, the semivowel /w/ within syllables, and tones 3 (ngã) and "
            "4 (hỏi). Errors on these in Vietnamese may still be typical for this "
            "child's age. The study covered the Northern dialect only, so ask the "
            "family which dialect the child speaks.",
            "language", PHAM_MCLEOD))

    if any(is_vietnamese(n) for n in names) and any(is_english(n) for n in names):
        tips.append(tip(
            "English consonants not found in standard Vietnamese include "
            "/ɡ θ ð ʃ ʒ tʃ dʒ ɹ/. Errors on these in English may reflect "
            "first-language influence rather than a speech disorder.",
            "language", ASHA_VIETNAMESE))

    if any(is_lang(n, "spanish", "español") for n in names) and any(is_english(n) for n in names):
        tips.append(tip(
            "Spanish uses only five word-final consonants (/s, n, r, l, d/) and five "
            "vowels. Dropped final consonants, simplified final clusters, or mixed-up "
            "English vowels (like \"seat\" and \"sit\") may reflect Spanish influence "
            "rather than a disorder.", "language", PRATH))
        tips.append(tip(
            "Spanish-English bilingual 5-year-olds did not differ significantly from "
            "monolingual peers in phonological accuracy, and how much they used each "
            "language did not predict phonological skills. Assess phonology directly "
            "in both languages.", "language", GOLDSTEIN))

    if any(is_lang(n, "arabic") for n in names):
        tips.append(tip(
            "Arabic-speaking children speak a spoken dialect at home and learn "
            "Standard Arabic mainly at school. Ask which dialect the child speaks, "
            "and check which variety a test uses.", "language", SCHIFF))

    if any(is_lang(n, "chinese") for n in names):
        tips.append(tip(
            "\"Chinese\" covers several languages, including Mandarin and Cantonese. "
            "Ask the family which one the child hears, since research and tests differ.",
            "language"))

    if any(is_lang(n, "mandarin", "putonghua") for n in names) and case.age_months <= 54:
        tips.append(tip(
            "In Hua & Dodd (2000), Mandarin-speaking children produced syllable-initial "
            "consonants correctly about two-thirds of the time at age 4;6, with four "
            "affricates still developing. Errors on initial consonants may still be "
            "typical at this age.", "language", HUA_DODD))

    if any(is_lang(n, "cantonese") for n in names) and case.age_months >= 48:
        tips.append(tip(
            "Cantonese-speaking children in So & Dodd (1995) made few phonological "
            "errors after age 4. Errors in Cantonese at this age are worth a closer look.",
            "language", SO_DODD))

    library_lower = {name.lower() for name in library_languages}
    for name in names:
        if name.lower() in library_lower:
            tips.append(tip(f"The Knowledge Library has research notes and assessment "
                            f"tools for {name}.", "language"))

    # --- Exposure checks ---
    if len(case.languages) == 1:
        tips.append(tip("Only one language was entered. Ask the family whether the "
                        "child hears any other languages.", "exposure"))

    for lang in case.languages:
        hears = lang.percent_hears or 0
        speaks = lang.percent_speaks or 0
        if hears < LOW_EXPOSURE:
            tips.append(tip(f"The child hears {lang.name} only {hears}% of the time. "
                            f"Lower skills in {lang.name} may reflect limited "
                            "exposure, not a disorder.", "exposure", CITATION_PENDING))
        if hears - speaks >= BIG_GAP:
            tips.append(tip(f"The child hears {lang.name} much more than they speak "
                            "it. Consider testing understanding separately from "
                            "speaking.", "exposure", CITATION_PENDING))

    # --- General reminders ---
    tips.append(tip("Compare the child to bilingual peers from the same community, "
                    "not to monolingual norms.", "general"))
    tips.append(tip("A true language disorder usually shows up in all of a child's "
                    "languages. Gather information on each one.", "general"))
    return tips


# A plain-language list of every rule, shown on the About page.
RULE_TABLE = [
    {"Rule": "Vietnamese sounds and tones still developing",
     "When it shows": f"Vietnamese entered and child under {VIETNAMESE_AGE_CUTOFF} months",
     "Source": PHAM_MCLEOD},
    {"Rule": "English sounds not in Vietnamese",
     "When it shows": "Vietnamese and English both entered",
     "Source": ASHA_VIETNAMESE},
    {"Rule": "Spanish influence on English sounds",
     "When it shows": "Spanish and English both entered",
     "Source": PRATH},
    {"Rule": "Assess phonology in both languages",
     "When it shows": "Spanish and English both entered",
     "Source": GOLDSTEIN},
    {"Rule": "Arabic dialect vs Standard Arabic",
     "When it shows": "Arabic entered",
     "Source": SCHIFF},
    {"Rule": "Mandarin initial consonants still developing",
     "When it shows": "Mandarin entered and child 54 months or younger",
     "Source": HUA_DODD},
    {"Rule": "Few Cantonese errors after age 4",
     "When it shows": "Cantonese entered and child 48 months or older",
     "Source": SO_DODD},
    {"Rule": "Ask which Chinese language",
     "When it shows": "\"Chinese\" entered",
     "Source": "Reminder to complete the language history."},
    {"Rule": "Limited exposure",
     "When it shows": f"Child hears a language less than {LOW_EXPOSURE}% of the time",
     "Source": CITATION_PENDING},
    {"Rule": "Hears much more than speaks",
     "When it shows": f"Hears minus speaks is {BIG_GAP} points or more",
     "Source": CITATION_PENDING},
    {"Rule": "Only one language entered",
     "When it shows": "One language on the case",
     "Source": "Reminder to complete the language history."},
    {"Rule": "Compare to bilingual peers; check every language",
     "When it shows": "Every case",
     "Source": "General reminder. Citation in progress."},
]
