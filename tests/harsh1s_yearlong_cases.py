"""Small executable fixtures for fork-local yearlong experiments."""

PROJECT = "capa"
CASES = [
    {"date": "2025-06-01", "seed": 350325},
]

def case_count():
    return len(CASES)
