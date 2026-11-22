

import csv
import urllib.request

datasets = {
    "developer_tools.csv":
    "https://raw.githubusercontent.com/harpd-dev/harpd-ai-datasets/main/data/research/developer-tools-index.csv",

    "ai_tools.csv":
    "https://raw.githubusercontent.com/harpd-dev/harpd-ai-datasets/main/data/research/ai-tools-index.csv"
}

for filename, url in datasets.items():
    print("Downloading", filename)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Engineer-Demo/1.0"}
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()

    with open(filename, "wb") as f:
        f.write(content)

    with open(filename, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print("Records:", len(rows))
    print("Columns:", list(rows[0].keys()) if rows else [])

print("\nProduct dataset downloads completed!")
