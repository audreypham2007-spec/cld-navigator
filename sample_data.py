# sample_data.py - made-up demo cases so visitors can try the site.
# None of these are real children.

from database import Case, Language

DEMO_CASES = [
    {"case_code": "DEMO-001", "age_months": 54,
     "concerns": "Teacher reports short sentences in English.",
     "notes": "Made-up demo case.",
     "languages": [("Vietnamese", 70, 40), ("English", 30, 60)]},
    {"case_code": "DEMO-002", "age_months": 84,
     "concerns": "Family asks about speech sound errors in English.",
     "notes": "Made-up demo case.",
     "languages": [("Spanish", 50, 50), ("English", 50, 50)]},
    {"case_code": "DEMO-003", "age_months": 40,
     "concerns": "Parent wonders whether the child is talking enough.",
     "notes": "Made-up demo case.",
     "languages": [("Vietnamese", 90, 85)]},
    {"case_code": "DEMO-004", "age_months": 60,
     "concerns": "Teacher wonders whether the child understands classroom directions.",
     "notes": "Made-up demo case.",
     "languages": [("Arabic", 60, 70), ("English", 40, 30)]},
    {"case_code": "DEMO-005", "age_months": 66,
     "concerns": "Family reports some sound errors in Cantonese.",
     "notes": "Made-up demo case.",
     "languages": [("Cantonese", 55, 50), ("English", 45, 50)]},
]


def load_demo_cases(session):
    """Add any demo cases that aren't saved yet. Returns how many were added."""
    added = 0
    for demo in DEMO_CASES:
        if session.query(Case).filter_by(case_code=demo["case_code"]).first():
            continue
        case = Case(case_code=demo["case_code"], age_months=demo["age_months"],
                    concerns=demo["concerns"], notes=demo["notes"])
        for name, hears, speaks in demo["languages"]:
            case.languages.append(Language(name=name, percent_hears=hears,
                                           percent_speaks=speaks))
        session.add(case)
        added += 1
    session.commit()
    return added
