"""Small executable fixtures for fork-local yearlong experiments."""

PROJECT = "capa"
CASES = [
    {"date": "2025-06-01", "seed": 350325},
    {"date": "2025-06-14", "seed": 337358},
    {"date": "2025-06-15", "seed": 361843},
    {"date": "2025-06-20", "seed": 762350},
    {"date": "2025-06-21", "seed": 814280},
    {"date": "2025-06-27", "seed": 99821},
    {"date": "2025-07-04", "seed": 743218},
    {"date": "2025-07-05", "seed": 66930},
]

def case_count():
    return len(CASES)
