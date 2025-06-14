"""Small executable fixtures for fork-local yearlong experiments."""

PROJECT = "capa"
CASES = [
    {"date": "2025-06-01", "seed": 350325},
    {"date": "2025-06-14", "seed": 337358},
]

def case_count():
    return len(CASES)
