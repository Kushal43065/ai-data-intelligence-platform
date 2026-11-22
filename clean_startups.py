
import csv

input_file = "ai_startups_source.csv"
output_file = "startups_final.csv"

with open(input_file, "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

# Remove duplicate company names
unique = {}
for row in rows:
    name = row.get("company_name", "").strip()

    if name and name.lower() not in unique:
        unique[name.lower()] = row

cleaned = list(unique.values())

# Select 1000 unique records
selected = cleaned[:1000]

with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=selected[0].keys()
    )
    writer.writeheader()
    writer.writerows(selected)

print("Original records:", len(rows))
print("Unique startups:", len(cleaned))
print("Final startup records:", len(selected))
print("Saved to:", output_file)
