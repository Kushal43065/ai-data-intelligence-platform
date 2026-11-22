



import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import time

BASE_URL = "https://export.arxiv.org/api/query"

SEARCH_QUERY = (
    "cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR "
    "cat:cs.CL OR cat:cs.RO OR cat:cs.NE OR stat.ML"
)

TARGET_COUNT = 1000
BATCH_SIZE = 100
NS = {"atom": "http://www.w3.org/2005/Atom"}

papers = []
seen_ids = set()

for start in range(0, TARGET_COUNT, BATCH_SIZE):
    params = {
        "search_query": SEARCH_QUERY,
        "start": start,
        "max_results": BATCH_SIZE,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    print(f"Fetching papers {start + 1} to {start + BATCH_SIZE}...")

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ResearchPaperCollector/1.0"}
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        for entry in root.findall("atom:entry", NS):
            id_url = entry.findtext("atom:id", default="", namespaces=NS)
            arxiv_id = id_url.rstrip("/").split("/")[-1].split("v")[0]

            if not arxiv_id or arxiv_id in seen_ids:
                continue

            seen_ids.add(arxiv_id)

            title = entry.findtext(
                "atom:title", default="", namespaces=NS
            ).strip().replace("\n", " ")

            abstract = entry.findtext(
                "atom:summary", default="", namespaces=NS
            ).strip().replace("\n", " ")

            authors = [
                author.findtext("atom:name", default="", namespaces=NS)
                for author in entry.findall("atom:author", NS)
            ]

            published = entry.findtext(
                "atom:published", default="", namespaces=NS
            )

            papers.append({
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "publication_date": published[:10],
                "arxiv_page_url": id_url,
                "arxiv_pdf_url": (
                    "https://arxiv.org/pdf/" + arxiv_id
                ),
                "github_url": None,
                "github_stars": None,
                "source": "arXiv API"
            })

        print("Unique papers collected:", len(papers))

        if len(papers) >= TARGET_COUNT:
            break

        time.sleep(3)

    except Exception as error:
        print("Collection stopped:", error)
        break

papers = papers[:TARGET_COUNT]

with open(
    "bulk_research_papers.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(papers, file, indent=2, ensure_ascii=False)

print("\nCollection completed.")
print("Total unique papers:", len(papers))
print("Output: bulk_research_papers.json")

