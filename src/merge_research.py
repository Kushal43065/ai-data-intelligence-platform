
import json
import csv

# Load the two datasets
with open("bulk_research_papers.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

with open("github_metrics.json", "r", encoding="utf-8") as f:
    github_data = json.load(f)

# Match GitHub results with research papers using arXiv ID
github_lookup = {
    str(item.get("arxiv_id", "")): item
    for item in github_data
}

final_papers = []

for paper in papers:
    arxiv_id = str(paper.get("arxiv_id", ""))
    github = github_lookup.get(arxiv_id, {})

    record = {
        "arxiv_id": arxiv_id,
        "title": paper.get("title", ""),
        "authors": ", ".join(paper.get("authors", []))
        if isinstance(paper.get("authors"), list)
        else paper.get("authors", ""),
        "abstract": paper.get("abstract", ""),
        "publication_date": paper.get("publication_date", ""),
        "arxiv_page_url": paper.get("arxiv_page_url", ""),
        "github_url": github.get("github_url", ""),
        "repository_name": github.get("repository_name", ""),
        "github_stars": github.get("stars", ""),
        "verification": github.get(
            "verification", "No GitHub repository verified"
        )
    }

    final_papers.append(record)

# Save JSON
with open("research_papers_final.json", "w", encoding="utf-8") as f:
    json.dump(final_papers, f, indent=2, ensure_ascii=False)

# Save CSV for Google Sheets
with open("research_papers_final.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=final_papers[0].keys())
    writer.writeheader()
    writer.writerows(final_papers)

print("Total research papers:", len(final_papers))
print("Papers with GitHub URLs:", sum(bool(p["github_url"]) for p in final_papers))
print("Saved: research_papers_final.json")
print("Saved: research_papers_final.csv")
