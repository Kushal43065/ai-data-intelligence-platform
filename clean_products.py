
import csv

files = ["developer_tools.csv", "ai_tools.csv"]

all_products = []

for filename in files:
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        all_products.extend(list(reader))

print("Total records before cleaning:", len(all_products))

# Remove duplicates using domain, then name as fallback
unique_products = {}

for product in all_products:
    domain = product.get("domain", "").strip().lower()
    name = product.get("name", "").strip().lower()

    key = domain if domain else name

    if key and key not in unique_products:
        unique_products[key] = product

cleaned = list(unique_products.values())

# Select 1000 unique products
selected = cleaned[:1000]

with open("products_final.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=selected[0].keys()
    )
    writer.writeheader()
    writer.writerows(selected)

print("Unique products:", len(cleaned))
print("Final product records:", len(selected))
print("Saved to: products_final.csv")
