
import json
import re
import urllib.request
import urllib.error
import time

with open("bulk_research_papers.json", encoding="utf-8") as f:
    papers = json.load(f)

pattern = r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"

checked = set()
results = []

for paper in papers:
    urls = re.findall(pattern, paper.get("abstract", ""))

    for owner, repo in urls:
        repo = repo.rstrip(".")
        key = (owner, repo)

        if key in checked:
            continue

        checked.add(key)

        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        request = urllib.request.Request(
            api_url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "ResearchPaperCollector"
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))

            results.append({
                "arxiv_id": paper["arxiv_id"],
                "paper_title": paper["title"],
                "github_url": data["html_url"],
                "repository_name": data["full_name"],
                "stars": data["stargazers_count"],
                "verification": "Repository exists; paper association needs review"
            })

            print("Verified:", data["full_name"],
                  "Stars:", data["stargazers_count"])

        except urllib.error.HTTPError as error:
            print("Could not verify:", owner, repo, error.code)

        except Exception as error:
            print("Error:", error)

        time.sleep(1)

with open("github_metrics.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nRepositories checked:", len(checked))
print("Verified repositories:", len(results))
print("Saved to github_metrics.json")
