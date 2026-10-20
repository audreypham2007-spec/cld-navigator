# rules.py - simple checks that give the SLP things to consider.
# These NEVER diagnose. Before sharing the tool, back each rule with a research source.

LOW_EXPOSURE = 20  # percent. TODO: confirm this cutoff in research and cite it
BIG_GAP = 30       # percent. TODO: confirm and cite


def get_considerations(case):
    tips = []

    if len(case.languages) == 1:
        tips.append("Only one language was entered. Ask the family whether the "
                    "child hears any other languages.")

    for lang in case.languages:
        if lang.percent_hears < LOW_EXPOSURE:
            tips.append(f"The child hears {lang.name} only {lang.percent_hears}% of "
                        f"the time. Lower skills in {lang.name} may reflect limited "
                        "exposure, not a disorder.")
        if lang.percent_hears - lang.percent_speaks >= BIG_GAP:
            tips.append(f"The child hears {lang.name} much more than they speak it. "
                        "Consider testing understanding separately from speaking.")

    tips.append("Compare the child to bilingual peers from the same community, "
                "not to monolingual norms.")
    tips.append("A true language disorder usually shows up in all of a child's "
                "languages. Gather information on each one.")
    return tips
