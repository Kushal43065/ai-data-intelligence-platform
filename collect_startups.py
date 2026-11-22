
import csv
import urllib.request

url = "https://raw.githubusercontent.com/runsmlee/ai-startup-dataset/main/ai-startups.csv"

print("Downloading AI startup dataset...")

request = urllib.request.Request(
    url,
    headers={"User-Agent": "AI-Engineer-Demo/1.0"}
)

with urllib.request.urlopen(request, timeout=60) as response:
    data = response.read()

with open("ai_startups_source.csv", "wb") as f:
    f.write(data)

print("Download completed!")

with open("ai_startups_source.csv", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

print("Total startup records:", len(rows))
print("First 5 startups:")

for row in rows[:5]:
    print(row["company_name"], "-", row["category"])

