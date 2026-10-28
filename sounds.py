# sounds.py - data for the Sound Explorer page and the home page myths.
# Every claim here names its source. Nothing here diagnoses.

# English consonants, grouped by how they are made.
# (IPA symbol, example word, letters in the word that make the sound)
ENGLISH_CONSONANTS = {
    "Stops": [("p", "pig", "p"), ("b", "bat", "b"), ("t", "top", "t"),
              ("d", "dog", "d"), ("k", "cat", "c"), ("ɡ", "go", "g")],
    "Nasals": [("m", "moon", "m"), ("n", "nose", "n"), ("ŋ", "sing", "ng")],
    "Fricatives": [("f", "fish", "f"), ("v", "van", "v"), ("θ", "think", "th"),
                   ("ð", "this", "th"), ("s", "sun", "s"), ("z", "zoo", "z"),
                   ("ʃ", "ship", "sh"), ("ʒ", "measure", "s"), ("h", "hat", "h")],
    "Affricates": [("tʃ", "chip", "ch"), ("dʒ", "jump", "j")],
    "Liquids and glides": [("l", "leaf", "l"), ("ɹ", "red", "r"), ("w", "wet", "w"),
                           ("j", "yes", "y")],
}
TOTAL_CONSONANTS = sum(len(v) for v in ENGLISH_CONSONANTS.values())

ASHA_SPANISH = ("American Speech-Language-Hearing Association. (n.d.). Spanish phonemic "
                "inventory. https://www.asha.org/practice/multicultural/phono/")
ASHA_VIETNAMESE = ("American Speech-Language-Hearing Association. (n.d.). Vietnamese "
                   "phonemic inventory. https://www.asha.org/practice/multicultural/phono/")
PHAM_MCLEOD = ("Phạm, B., & McLeod, S. (2019). Vietnamese-speaking children's acquisition "
               "of consonants, semivowels, vowels, and tones in Northern Viet Nam. Journal "
               "of Speech, Language, and Hearing Research. "
               "https://doi.org/10.1044/2019_JSLHR-S-17-0405")

# English consonants NOT in each home language, from the cited source.
SOUND_GAPS = {
    "Spanish": {
        "missing": {"ŋ", "v", "ð", "θ", "z", "ʃ", "ʒ", "h", "dʒ", "ɹ"},
        "note": "Dialects of Spanish differ, so check the child's dialect.",
        "extras": [
            ("Word endings", "Only five consonants end Spanish words.",
             ["l", "r", "d", "n", "s"],
             "Dropped final consonants and simplified final clusters in English can "
             "come from this."),
            ("Vowels", "Spanish has five vowels. English has many more.",
             ["i", "e", "a", "o", "u"],
             "English vowel pairs like “seat” and “sit” can be "
             "hard to tell apart."),
        ],
        "sources": [ASHA_SPANISH],
    },
    "Vietnamese": {
        "missing": {"ɡ", "θ", "ð", "ʃ", "ʒ", "tʃ", "dʒ", "ɹ"},
        "note": "Sources differ slightly on /ɡ ʃ ʒ/, likely because of dialect. Ask "
                "which of the three major dialects (Northern, Central, Southern) the "
                "child speaks.",
        "extras": [],
        "sources": [ASHA_VIETNAMESE, PHAM_MCLEOD],
    },
}
BILING_CANTONESE = ("Bilinguistics. (n.d.). Cantonese speech and language development. "
                    "https://bilinguistics.com/cantonese-speech-and-language-development/")
BILING_ARABIC = ("Bilinguistics. (n.d.). Arabic speech and language development. "
                 "https://bilinguistics.com/languages/arabic-speech-and-language-development/")
SOUND_GAPS["Cantonese"] = {
    "missing": {"b", "d", "ɡ", "v", "z", "ʃ", "ʒ", "tʃ", "dʒ", "θ", "ð", "ɹ"},
    "note": "When a family says the child speaks \u201cChinese,\u201d ask which "
            "language, since Cantonese and Mandarin sound systems differ.",
    "extras": [
        ("Grammar", "Cantonese has no articles, plural endings, or tense endings, and its "
         "pronouns don't mark he or she.",
         ["a / the", "-s", "-ed", "he / she"],
         "English learners may leave out articles, plural -s, and past tense, or mix up "
         "he and she. These patterns are a typical part of learning English."),
    ],
    "sources": [BILING_CANTONESE],
}
SOUND_GAPS["Arabic"] = {
    "missing": {"p", "v", "ŋ", "ɹ", "tʃ", "ʒ", "dʒ"},
    "note": "Arabic dialects differ, so a sound marked here may be used in the child's "
            "dialect. Ask which dialect the child speaks.",
    "extras": [
        ("Grammar", "Two common English patterns from Arabic.",
         ["al-", "am / is / are"],
         "The Arabic article can carry over, as in \u201cAlcoffee is ready.\u201d Forms "
         "of \u201cto be\u201d may be left out, as in \u201cI boy.\u201d"),
    ],
    "sources": [BILING_ARABIC],
}

# Languages in the Library without a consonant comparison yet: what we do know.
SOUND_PENDING = {
    "Mandarin": "Children in Hua and Dodd (2000) learned tones first and syllable-initial "
                "consonants last.",
}
MANDARIN_READING = ("Assessing speech production in Mandarin-English bilingual children: "
                    "Comparison of Mandarin and English sound systems and special "
                    "considerations. (2024). Perspectives of the ASHA Special Interest "
                    "Groups, 9(3), 715-737. https://doi.org/10.1044/2023_PERSP-23-00101")


# ---------------------------------------------------------------- myths
GENESEE = ("Genesee, F. (2009). Early childhood bilingualism: Perils and possibilities. "
           "Journal of Applied Research on Learning, 2(Special Issue), Article 2.")
PEARSON = ("Pearson, B. Z., Fernández, S. C., & Oller, D. K. (1993). Lexical development "
           "in bilingual infants and toddlers: Comparison to monolingual norms. Language "
           "Learning, 43(1), 93-120. https://doi.org/10.1111/j.1467-1770.1993.tb00174.x")
PARADIS = ("Paradis, J., Crago, M., Genesee, F., & Rice, M. (2003). French-English "
           "bilingual children with SLI: How do they compare with their monolingual "
           "peers? Journal of Speech, Language, and Hearing Research, 46(1), 113-127. "
           "https://doi.org/10.1044/1092-4388(2003/009)")
PENA = ("Peña, E., Iglesias, A., & Lidz, C. S. (2001). Reducing test bias through dynamic "
        "assessment of children's word learning ability. American Journal of "
        "Speech-Language Pathology, 10(2), 138-154. "
        "https://doi.org/10.1044/1058-0360(2001/014)")
PHAM_TIPTON = ("Pham, G., & Tipton, T. (2018). Internal and external factors that support "
               "children's minority first language and English. Language, Speech, and "
               "Hearing Services in Schools. https://doi.org/10.1044/2018_LSHSS-17-0086")

MYTHS = [
    ("Learning two languages causes a language delay.",
     "In a study of toddlers aged 8 to 30 months, there was no statistical basis for "
     "concluding that bilingual children were slower to build early vocabulary, when "
     "words in both languages were counted.",
     [PEARSON]),
    ("Mixing two languages in one sentence means the child is confused.",
     "Code-mixing is a normal part of bilingual development and reflects the child's "
     "knowledge of both grammars, not confusion.",
     [GENESEE]),
    ("Families should switch to English at home.",
     "Parents should be encouraged to keep using the home language. In one Vietnamese-"
     "English study, parents' use of Vietnamese contributed to children's Vietnamese vocabulary "
     "and was not related to their English vocabulary.",
     [GENESEE, PHAM_TIPTON]),
    ("A child with a language disorder should learn only one language.",
     "Bilingual children with specific language impairment performed like monolingual "
     "peers with the same impairment on the grammar measured. Learning two languages "
     "did not appear to add risk. The studies are small, so this is still an active "
     "research area.",
     [PARADIS, GENESEE]),
    ("A low score on an English test means a disorder.",
     "Bilingual vocabulary norms should count both languages. In a test-teach-retest "
     "word-learning task, how much a child learned predicted ability groups better "
     "than a one-time test score.",
     [PEARSON, PENA]),
]


SHORT = {GENESEE: "Genesee (2009)", PEARSON: "Pearson et al. (1993)",
         PARADIS: "Paradis et al. (2003)", PENA: "Peña et al. (2001)",
         PHAM_TIPTON: "Pham and Tipton (2018)", ASHA_SPANISH: "ASHA",
         ASHA_VIETNAMESE: "ASHA", PHAM_MCLEOD: "Phạm and McLeod (2019)"}


def short_cite(source):
    return SHORT.get(source, source.split("(")[0].strip())


# ---------------------------------------------------------------- tones
# Pitch on a 1 (low) to 5 (high) scale. Mandarin and Cantonese values are the
# canonical tone numbers from Politzer-Ahles (2021).
POLITZER = ("Politzer-Ahles, S. (2021). Phonetic description of tone. The Hong Kong "
            "Polytechnic University. https://polyu.edu.hk/cbs/sjpolit/Classes/CBS516/"
            "Phonetics/phonetic-description-tone.html")
KIRBY = ("Kirby, J. P. (2011). Vietnamese (Hanoi Vietnamese). Journal of the "
         "International Phonetic Association, 41(3), 381-392. "
         "https://doi.org/10.1017/S0025100311000181")
SHORT.update({POLITZER: "Politzer-Ahles (2021)", KIRBY: "Kirby (2011)"})

# (tone label, syllable, written form, meaning, pitch points, note)
TONES = {
    "Mandarin": {
        "intro": "Four tones. The same syllable, ma, means four different things.",
        "tones": [("Tone 1", "mā", "妈", "mother", [5, 5], "55"),
                  ("Tone 2", "má", "麻", "hemp", [3, 5], "35"),
                  ("Tone 3", "mǎ", "马", "horse", [2, 1, 3], "213"),
                  ("Tone 4", "mà", "骂", "scold", [5, 1], "51")],
        "caption": "Tone numbers from Politzer-Ahles (2021). Children in Hua and Dodd "
                   "(2000) learned tones first, and tone errors were uncommon.",
        "sources": [POLITZER],
    },
    "Cantonese": {
        "intro": "Six tones. The syllable fan has six meanings.",
        "tones": [("Tone 1", "fan1", "分", "divide", [5, 5], "55"),
                  ("Tone 2", "fan2", "粉", "powder", [3, 5], "35"),
                  ("Tone 3", "fan3", "訓", "teach", [3, 3], "33"),
                  ("Tone 4", "fan4", "焚", "burn", [2, 1], "21"),
                  ("Tone 5", "fan5", "奮", "strive", [1, 2], "12"),
                  ("Tone 6", "fan6", "份", "portion", [2, 2], "22")],
        "caption": "Tone numbers and example syllables from Politzer-Ahles (2021). "
                   "Children in So and Dodd (1995) mastered tones by about age 2.",
        "sources": [POLITZER],
    },
    "Vietnamese": {
        "intro": "Six tones in Northern Vietnamese. Only the tone changes the word.",
        "tones": [("Ngang", "ma", "ma", "ghost", [3, 3], "level"),
                  ("Huyền", "mà", "mà", "but", [2.5, 1.2], "low, falling"),
                  ("Sắc", "má", "má", "mother", [3, 5], "rising"),
                  ("Hỏi", "mả", "mả", "grave", [3, 1.5, 2.6], "dipping"),
                  ("Ngã", "mã", "mã", "horse", [3, 3.6, None, 4, 5], "rising, with a break"),
                  ("Nặng", "mạ", "mạ", "rice seedling", [2.5, 1.2, "stop"], "low, short, cut off")],
        "caption": "Approximate shapes, for orientation only. Tones vary by dialect and "
                   "speaker. For acoustic detail, see Kirby (2011). Tones 3 (ngã) and 4 "
                   "(hỏi) may still be developing before age 6 (Phạm and McLeod, 2019).",
        "sources": [KIRBY, PHAM_MCLEOD],
    },
}

SCHIFF_FULL = ("Schiff, R., & Saiegh-Haddad, E. (2018). Development and relationships "
               "between phonological awareness, morphological awareness and word reading "
               "in spoken and standard Arabic. Frontiers in Psychology, 9, 356. "
               "https://doi.org/10.3389/fpsyg.2018.00356")

SHORT.update({BILING_CANTONESE: "Bilinguistics", BILING_ARABIC: "Bilinguistics"
              , MANDARIN_READING: "ASHA Perspectives (2024)"})


# ---------------------------------------------------------------- fun facts
# (big glyph, fact, short source). Every fact comes from a source the site cites.
FACTS = [
    ("mạ", "Ma, má, mà, mả, mã, mạ: six Vietnamese words that differ only in tone.",
     "Phạm and McLeod (2019)"),
    ("5", "Only five consonants end Spanish words: l, r, d, n, and s.", "ASHA"),
    ("2", "Cantonese-speaking children had mastered tones and vowels by about age 2.",
     "So and Dodd (1995)"),
    ("ع", "Arabic-speaking children first learn to read in a variety of Arabic they don't "
          "speak at home.", "Schiff and Saiegh-Haddad (2018)"),
    ("妈", "Mandarin-speaking children learned tones first and the consonants that start "
           "syllables last.", "Hua and Dodd (2000)"),
    ("ɹ", "The English r sound, as in red, is missing from Spanish, Vietnamese, Arabic, "
          "Cantonese, Filipino, and Punjabi.", "ASHA, Bilinguistics"),
    ("27", "Across 27 languages, most consonants were acquired by age 5.",
     "McLeod and Crowe (2018)"),
    ("82%", "About 82% of California English learners speak Spanish at home.",
     "California Department of Education"),
    ("Both", "Bilingual toddlers kept pace with monolingual peers in early vocabulary when "
           "words in both languages were counted.", "Pearson et al. (1993)"),
]
FACTS += [
    ("93%", "The top 10 home languages cover 93% of California English learners.",
     "California Department of Education"),
    ("v", "Tagalog doesn't use English /v/, so vase may sound like base.", "Bilinguistics"),
    ("4", "Only four English consonants, /w/, /ð/, /θ/, and /ŋ/, don't occur in Farsi.",
     "MultiCSD"),
    ("SOV", "Punjabi, Farsi, and Korean all put the verb at the end of the sentence.",
     "Bilinguistics, MultiCSD"),
    ("6:4", "Cantonese uses six tones. Mandarin uses four.", "Politzer-Ahles (2021)"),
    ("p", "Arabic doesn't use the English p sound, as in pig.", "Bilinguistics"),
    ("3;6", "In one study, 75% of Mandarin-speaking children had acquired the consonants "
            "that start syllables by age 3;6.", "Hua and Dodd (2000)"),
]


# ---------------------------------------------------------------- mouth map
# Where in the mouth each English consonant is made (standard phonetics),
# from the lips at the front to the throat at the back.
PLACES = [
    ("Lips", "with both lips", ["p", "b", "m", "w"]),
    ("Lip and teeth", "with the lip on the teeth", ["f", "v"]),
    ("Teeth", "with the tongue at the teeth", ["θ", "ð"]),
    ("Gum ridge", "at the ridge behind the teeth", ["t", "d", "s", "z", "n", "l"]),
    ("Behind the ridge", "just behind the gum ridge", ["ʃ", "ʒ", "tʃ", "dʒ", "ɹ"]),
    ("Roof", "at the hard roof of the mouth", ["j"]),
    ("Soft palate", "at the soft back of the roof", ["k", "ɡ", "ŋ"]),
    ("Throat", "in the throat", ["h"]),
]

# ---------------------------------------------------------------- timeline
# (age in years, end age or None, language, what happens, short source)
MILESTONES = [
    (2.0, None, "Cantonese", "Tones and vowels mastered", "So and Dodd (1995)"),
    (3.5, None, "Mandarin", "75% of children have the consonants that start syllables",
     "Hua and Dodd (2000)"),
    (4.0, None, "Cantonese", "Few speech sound errors after this age", "So and Dodd (1995)"),
    (5.0, None, "27 languages", "Most consonants acquired", "McLeod and Crowe (2018)"),
    (5.4, 5.9, "Vietnamese", "Nearly all sounds and tones acquired (Northern)",
     "Phạm and McLeod (2019)"),
]


# ---------------------------------------------------------------- word pairs
# English minimal pairs: two real words that differ only in the target sound.
# Useful for probing whether a child hears and says the contrast.
PAIRS = {
    "p": [("pig", "big"), ("pat", "bat")],
    "b": [("bat", "pat"), ("bear", "pear")],
    "d": [("dime", "time"), ("dug", "tug")],
    "ɡ": [("goat", "coat"), ("gold", "cold")],
    "ŋ": [("sing", "sin"), ("thing", "thin")],
    "v": [("van", "ban"), ("vote", "boat")],
    "θ": [("think", "sink"), ("thin", "tin")],
    "ð": [("they", "day"), ("then", "den")],
    "z": [("zoo", "sue"), ("zip", "sip")],
    "ʃ": [("ship", "sip"), ("shoe", "sue")],
    "h": [("hat", "at"), ("hold", "old")],
    "tʃ": [("chip", "ship"), ("chin", "shin")],
    "dʒ": [("jam", "yam"), ("joke", "yoke")],
    "ɹ": [("red", "wed"), ("rock", "lock")],
}


# ---------------------------------------------------------------- more languages
BILING_TAGALOG = ("Bilinguistics. (n.d.). Filipino - Tagalog speech and language "
                  "development. https://bilinguistics.com/languages/"
                  "filipino-tagalog-speech-and-language-development/")
BILING_PUNJABI = ("Bilinguistics. (n.d.). Punjabi speech and language development. "
                  "https://bilinguistics.com/languages/punjabi-speech-and-language-development/")
MULTICSD_FARSI = ("Gildersleeve-Neumann, C., Wahlstrom, A., & Morandi, M. (2022). Farsi "
                  "(Persian). MultiCSD. https://sites.google.com/view/multicsd/"
                  "global-languages/farsi-persian")
MULTICSD_KOREAN = ("Gildersleeve-Neumann, C. (n.d.). Korean. MultiCSD. "
                   "https://sites.google.com/view/multicsd/global-languages/korean")
BILING_RUSSIAN = ("Bilinguistics. (2013). The influence of a first language on English "
                  "acquisition: A look at Spanish, Russian, and Vietnamese [Presentation "
                  "slides]. https://bilinguistics.com/wp-content/uploads/2013/12/"
                  "Are-His-Errors-Russian-Vietnamese-Spanish.pdf")

SOUND_GAPS["Farsi"] = {
    "missing": {"w", "ð", "θ", "ŋ"},
    "note": "Farsi speakers may find these sounds harder to say in English.",
    "extras": [("Stress", "Farsi stress usually falls on the last stem syllable.",
                ["last syllable"],
                "English learners may stress the last syllable of some English words.")],
    "sources": [MULTICSD_FARSI],
}
SOUND_GAPS["Filipino"] = {
    "missing": {"f", "v", "z", "ʒ", "θ", "ð", "ɹ", "ʃ", "tʃ", "dʒ", "t", "d"},
    "note": "/ʃ tʃ dʒ/ are used in some dialects or in loanwords. /t/ and /d/ are made "
            "at the teeth in Tagalog, so they count as different from English.",
    "extras": [("Common patterns", "Sounds may be swapped for the nearest Tagalog sound.",
                ["vase → base", "math → mat", "that → dat"],
                "English /v/ may be said as /b/, and both “th” sounds as /t/ "
                "or /d/."),
               ("Clusters and stress", "Tagalog words don't start with consonant "
                "clusters, except borrowed words.", ["plank → pank", "BUTterfly"],
                "Clusters may be reduced, and English stress may shift.")],
    "sources": [BILING_TAGALOG],
}
SOUND_GAPS["Punjabi"] = {
    "missing": {"ʒ", "θ", "ð", "ɹ", "w", "v"},
    "note": "/v/ is used in some Punjabi dialects and in loanwords.",
    "extras": [("Grammar", "Punjabi puts the verb last and has no articles.",
                ["verb last", "a / the", "am / is / are"],
                "Verb-final order, missing articles, and a missing “to be” can "
                "carry into English while a child learns it.")],
    "sources": [BILING_PUNJABI],
}
SOUND_PENDING.update({
    "Russian": "Voiceless “th” (as in think) is in English but not in Russian. "
               "Russian has no articles and no present-tense “to be.”",
    "Korean": "Korean consonants at the ends of words are unreleased, and Korean /l/ "
              "becomes a flap between vowels.",
})
PENDING_SOURCES = {"Mandarin": [MANDARIN_READING], "Russian": [BILING_RUSSIAN],
                   "Korean": [MULTICSD_KOREAN]}
SHORT.update({BILING_TAGALOG: "Bilinguistics", BILING_PUNJABI: "Bilinguistics",
              MULTICSD_FARSI: "MultiCSD", MULTICSD_KOREAN: "MultiCSD",
              BILING_RUSSIAN: "Bilinguistics (2013)"})

# Other names families use for these languages.
ALIASES = {"tagalog": "Filipino", "pilipino": "Filipino", "persian": "Farsi",
           "putonghua": "Mandarin", "panjabi": "Punjabi", "vietnam": "Vietnamese",
           "tiếng việt": "Vietnamese", "español": "Spanish"}

ASHA_INTERPRETERS = ("American Speech-Language-Hearing Association. (n.d.). Collaborating "
                     "with interpreters, transliterators, and translators [Practice Portal]. "
                     "https://www.asha.org/practice-portal/professional-issues/"
                     "collaborating-with-interpreters/")

PEARSON_1997_FULL = ("Pearson, B. Z., Fernández, S. C., Lewedeg, V., & Oller, D. K. (1997). The "
                     "relation of input factors to lexical learning by bilingual infants. "
                     "Applied Psycholinguistics, 18(1), 41-58. "
                     "https://doi.org/10.1017/S0142716400009863")
GIBSON_FULL = ("Gibson, T. A., Oller, D. K., Jarmulowicz, L., & Ethington, C. A. (2012). The "
               "receptive-expressive gap in the vocabulary of young second-language learners: "
               "Robustness and possible mechanisms. Bilingualism: Language and Cognition, "
               "15(1), 102-116. https://doi.org/10.1017/S1366728910000490")


# ---------------------------------------------------------------- error check
PRATH_FULL = ("Prath, S. (n.d.). Quick rules: Spanish phonology. Bilinguistics. "
              "https://bilinguistics.com/quick-rules-spanish-phonology/")
SHORT.update({PRATH_FULL: "Prath (Bilinguistics)", PEARSON_1997_FULL: "Pearson et al. (1997)",
              GIBSON_FULL: "Gibson et al. (2012)"})

# Error patterns an SLP might see in a child's English, and which home languages the
# cited sources link them to: {key: (label, {language: (why, source)})}.
PATTERNS = {
    "final": ("Drops or changes final consonants", {
        "Spanish": ("Only five consonants end Spanish words: l, r, d, n, and s.", ASHA_SPANISH),
    }),
    "clusters": ("Simplifies consonant clusters, like plank to pank", {
        "Spanish": ("Simplified final clusters in English may reflect Spanish influence.",
                    PRATH_FULL),
        "Filipino": ("Tagalog words don't start with consonant clusters, except borrowed "
                     "words.", BILING_TAGALOG),
    }),
    "vowels": ("Mixes up English vowels, like seat and sit", {
        "Spanish": ("Spanish has five vowels. English has many more.", ASHA_SPANISH),
    }),
    "stress": ("Stresses the wrong syllable", {
        "Filipino": ("Tagalog stress falls on one of the last two syllables and can change "
                     "meaning.", BILING_TAGALOG),
        "Farsi": ("Farsi stress usually falls on the last stem syllable.", MULTICSD_FARSI),
    }),
    "articles": ("Leaves out a, an, or the", {
        "Cantonese": ("Cantonese has no articles.", BILING_CANTONESE),
        "Punjabi": ("Punjabi has no articles.", BILING_PUNJABI),
        "Russian": ("Russian has no articles.", BILING_RUSSIAN),
    }),
    "endings": ("Leaves off plural -s or past tense -ed", {
        "Cantonese": ("Cantonese doesn't mark plurals or tense on words.", BILING_CANTONESE),
    }),
    "to_be": ("Leaves out am, is, or are", {
        "Arabic": ("Forms of “to be” may be left out, as in “I boy.”",
                   BILING_ARABIC),
        "Punjabi": ("Punjabi often leaves out “to be.”", BILING_PUNJABI),
        "Russian": ("Russian has no present-tense “to be.”", BILING_RUSSIAN),
    }),
    "verb_last": ("Puts the verb at the end of the sentence", {
        "Punjabi": ("Punjabi uses subject-object-verb order.", BILING_PUNJABI),
        "Farsi": ("Farsi uses subject-object-verb order.", MULTICSD_FARSI),
        "Korean": ("Korean uses subject-object-verb order.", MULTICSD_KOREAN),
    }),
    "he_she": ("Mixes up he and she", {
        "Cantonese": ("Cantonese pronouns don't mark he or she.", BILING_CANTONESE),
    }),
}


def classify_errors(language, sounds, patterns):
    """Sort a child's English errors by whether the cited sources link them to the home
    language. Returns (explained, look_closer, no_data), each a list of
    (label, reason, source or None)."""
    explained, closer, no_data = [], [], []
    gaps = SOUND_GAPS.get(language)
    for ipa in sounds:
        label = f"/{ipa}/"
        if gaps is None:
            no_data.append((label, f"This site doesn't have a {language} consonant "
                                   "comparison yet.", None))
        elif ipa in gaps["missing"]:
            explained.append((label, f"{language} doesn't use this sound.", gaps["sources"][0]))
        else:
            closer.append((label, f"{language} uses this sound too, so a {language} sound "
                                  "difference doesn't explain the error.", gaps["sources"][0]))
    for key in patterns:
        label, by_lang = PATTERNS[key]
        if language in by_lang:
            why, src = by_lang[language]
            explained.append((label, why, src))
        else:
            no_data.append((label, f"The sources on this site don't link this pattern to "
                                   f"{language}.", None))
    return explained, closer, no_data
