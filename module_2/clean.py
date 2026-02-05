import json

# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def load_data(filename="applicant_data.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_data(raw_entries):
    cleaned = []

    for entry in raw_entries:
        cleaned_entry = {
            "school": entry.get("school"),
            "program": entry.get("program"),
            "degree_type": entry.get("degree_type"),
            "status": entry.get("applicant_status"),
            "decision_date": _normalize_date(entry.get("decision_date")),
            "gpa": entry.get("gpa"),
            "gre": {
                "total": entry.get("gre_total"),
                "v": entry.get("gre_v"),
                "q": entry.get("gre_q"),
                "aw": entry.get("gre_aw")
            },
            "citizenship": entry.get("citizenship"),
            "term": entry.get("term"),
            "comments": entry.get("comments"),
            "url": entry.get("url")
        }

        cleaned.append(cleaned_entry)

    return cleaned


# ============================================================
# PRIVATE HELPERS
# placeholder for future formatting - might want to include 2026 for entries of this year
# ============================================================

def _normalize_date(date_str):
    if not date_str:
        return None
    return date_str