# rules.py - simple checks that give the SLP things to consider.
# These NEVER diagnose. Before sharing the tool, back each rule with a research source.

LOW_EXPOSURE = 20  # percent. TODO: confirm this cutoff in research and cite it
BIG_GAP = 30       # percent. TODO: confirm and cite


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


def get_considerations(case):
    tips = []

    if len(case.languages) == 1:
        tips.append("Only one language was entered. Ask the family whether the "
                    "child hears any other languages.")

    for lang in case.languages:
        hears = lang.percent_hears or 0
        speaks = lang.percent_speaks or 0
        if hears < LOW_EXPOSURE:
            tips.append(f"The child hears {lang.name} only {hears}% of "
                        f"the time. Lower skills in {lang.name} may reflect limited "
                        "exposure, not a disorder.")
        if hears - speaks >= BIG_GAP:
            tips.append(f"The child hears {lang.name} much more than they speak it. "
                        "Consider testing understanding separately from speaking.")

    tips.append("Compare the child to bilingual peers from the same community, "
                "not to monolingual norms.")
    tips.append("A true language disorder usually shows up in all of a child's "
                "languages. Gather information on each one.")
    return tips
