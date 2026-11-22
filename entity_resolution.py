
import csv
import re
import json
from collections import defaultdict

INPUT_FILE = "startups_final.csv"

SEED_FILE = "seed_startups.csv"
OUTPUT_FILE = "entity_mapping_log.csv"

# Normalize company names for deterministic matching
def normalize_name(name):
    name = str(name or "").lower().strip()

    # Remove website prefixes
    name = re.sub(r"^https?://", "", name)
    name = re.sub(r"^www\.", "", name)

    # Remove punctuation and spaces
    name = re.sub(r"[^a-z0-9]", "", name)

    return name


# Read startup dataset
with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

if not rows:
    raise ValueError("Startup dataset is empty.")

# Automatically identify the company-name column
possible_names = [
    "company_name", "company", "name", "startup_name"
]

name_column = next(
    (c for c in possible_names if c in fieldnames),
    None
)

if not name_column:
    raise ValueError(
        "Company name column not found. Available columns: "
        + str(fieldnames)
    )

# Create 50 unique seed startups
seed_entities = {}

for row in rows:
    name = row.get(name_column, "").strip()
    key = normalize_name(name)

    if name and key and key not in seed_entities:
        seed_entities[key] = {
            "canonical_name": name,
            "category": row.get("category", ""),
            "country": row.get("country", ""),
            "website": row.get("website", "")
        }

    if len(seed_entities) == 50:
        break

if len(seed_entities) < 50:
    raise ValueError("Fewer than 50 unique seed startups found.")

# Save seed list
with open(SEED_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "canonical_name",
            "category",
            "country",
            "website"
        ]
    )
    writer.writeheader()
    writer.writerows(seed_entities.values())

# Build entity mapping
mapping_log = []

for row in rows:
    original_name = row.get(name_column, "").strip()
    key = normalize_name(original_name)

    if key in seed_entities:
        canonical = seed_entities[key]["canonical_name"]
        status = "MATCHED"
        method = "NORMALIZED_EXACT_MATCH"
        confidence = 1.0
    else:
        canonical = ""
        status = "UNMATCHED"
        method = "NO_EXACT_MATCH"
        confidence = 0.0

    mapping_log.append({
        "original_name": original_name,
        "normalized_name": key,
        "canonical_name": canonical,
        "status": status,
        "matching_method": method,
        "confidence": confidence
    })

# Save mapping log
with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "original_name",
            "normalized_name",
            "canonical_name",
            "status",
            "matching_method",
            "confidence"
        ]
    )

    writer.writeheader()
    writer.writerows(mapping_log)

matched = sum(
    1 for item in mapping_log
    if item["status"] == "MATCHED"
)

print("========== ENTITY RESOLUTION ==========")
print("Startup records processed:", len(rows))
print("Seed entities created:", len(seed_entities))
print("Matched records:", matched)
print("Unmatched records:", len(mapping_log) - matched)
print("Saved:", SEED_FILE)
print("Saved:", OUTPUT_FILE)
