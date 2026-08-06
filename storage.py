import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FICHIER_IDS = os.path.join(SCRIPT_DIR, "seen_ids.txt")

def load_seen_ids():
    """Load the seen IDs from the file."""
    if not os.path.exists(FICHIER_IDS):
        return set()
    with open(FICHIER_IDS, "r") as f:
        return set(line.strip() for line in f)

def add_seen_id(seen_id):
    """Add a seen ID to the file."""
    with open(FICHIER_IDS, "a") as f:
        f.write(f"{seen_id}\n")

