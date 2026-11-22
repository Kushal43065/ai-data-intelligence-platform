
import json
import csv
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "data scientist",
    "ai engineer",
    "ai researcher",
    "llm",
    "generative ai",
    "nlp engineer",
    "computer vision",
    "ml engineer",
    "machine learning engineer",
    "research scientist",
    "robotics engineer",
    "data science",
    "prompt engineer",
    "ai developer",
    "research engineer",
    "applied scientist"
]


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Engineer-Student-Project/1.0"}
    )

    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()


def parse_date(value):
    if not value:
        return None

    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, timezone.utc)

        value = str(value).strip()

        if value.isdigit():
            return datetime.fromtimestamp(int(value), timezone.utc)

        try:
            date = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError:
            date = parsedate_to_datetime(value)

        if date.tzinfo is None:
            return None

        return date.astimezone(timezone.utc)

    except (ValueError, TypeError, OverflowError):
        return None


def get_value(job, keys):
    for key in keys:
        if job.get(key) not in (None, ""):
            return job[key]
    return ""


def is_ai_job(title):
    title = str(title).lower()

    return any(keyword in title for keyword in KEYWORDS)


jobs = []


def add_job(
    source, title, company, location,
    date_value, url, description
):
    title = str(title).strip()
    description = str(description).strip()

    if not title or not is_ai_job(title):
        return

    published = parse_date(date_value)

    if not published:
        return

    now = datetime.now(timezone.utc)

    if not (
        now - timedelta(hours=24)
        <= published <= now
    ):
        return

    jobs.append({
        "source": source,
        "title": title,
        "company": company,
        "location": location,
        "published_at_utc": published.isoformat(),
        "job_url": url,
        "description": description
    })


# 1. REMOTE OK
try:
    data = json.loads(fetch("https://remoteok.com/api"))

    for job in data:
        if not isinstance(job, dict):
            continue

        if not job.get("position"):
            continue

        add_job(
            "Remote OK",
            job.get("position", ""),
            job.get("company", ""),
            job.get("location", ""),
            job.get("date"),
            job.get("url", ""),
            job.get("description", "")
        )

    print("Remote OK: completed")

except Exception as e:
    print("Remote OK error:", e)


# 2. JOBICY
try:
    data = json.loads(
        fetch("https://jobicy.com/api/v2/remote-jobs?count=50")
    )

    for job in data.get("jobs", []):
        add_job(
            "Jobicy",
            get_value(job, ["jobTitle", "title"]),
            get_value(job, ["companyName", "company"]),
            get_value(job, ["jobGeo", "location"]),
            get_value(job, ["pubDate", "pub_date", "jobPosted", "date"]),
            get_value(job, ["url", "jobUrl"]),
            get_value(job, ["jobDescription", "description"])
        )

    print("Jobicy: completed")

except Exception as e:
    print("Jobicy error:", e)


# 3. ARBEITNOW
try:
    data = json.loads(
        fetch("https://www.arbeitnow.com/api/job-board-api?page=1")
    )

    for job in data.get("data", []):
        add_job(
            "Arbeitnow",
            job.get("title", ""),
            get_value(job, ["company_name", "company"]),
            job.get("location", ""),
            get_value(job, ["created_at", "createdAt", "date"]),
            job.get("url", ""),
            job.get("description", "")
        )

    print("Arbeitnow: completed")

except Exception as e:
    print("Arbeitnow error:", e)


# 4. WORKING NOMADS
try:
    data = json.loads(
        fetch("https://www.workingnomads.com/api/exposed_jobs/")
    )

    if isinstance(data, dict):
        data = data.get("jobs", [])

    for job in data:
        add_job(
            "Working Nomads",
            job.get("title", ""),
            get_value(job, ["company_name", "company"]),
            job.get("location", ""),
            get_value(job, ["pub_date", "pubDate", "date"]),
            get_value(job, ["url", "link"]),
            get_value(job, ["description", "excerpt"])
        )

    print("Working Nomads: completed")

except Exception as e:
    print("Working Nomads error:", e)


# 5. WE WORK REMOTELY
try:
    root = ET.fromstring(
        fetch("https://weworkremotely.com/remote-jobs.rss")
    )

    for item in root.findall(".//item"):
        add_job(
            "We Work Remotely",
            item.findtext("title", ""),
            "",
            "Remote",
            item.findtext("pubDate", ""),
            item.findtext("link", ""),
            item.findtext("description", "")
        )

    print("We Work Remotely: completed")

except Exception as e:
    print("We Work Remotely error:", e)


# REMOVE DUPLICATES
unique_jobs = {}

for job in jobs:
    key = job["job_url"].strip().lower()

    if not key:
        key = (
            job["source"] + "|" +
            job["company"] + "|" +
            job["title"]
        ).lower()

    unique_jobs[key] = job


final_jobs = list(unique_jobs.values())


# SAVE CSV
fields = [
    "source",
    "title",
    "company",
    "location",
    "published_at_utc",
    "job_url",
    "description"
]

with open(
    "jobs_final.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fields
    )

    writer.writeheader()
    writer.writerows(final_jobs)


# SAVE JSON
with open(
    "jobs_final.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        final_jobs,
        file,
        indent=2,
        ensure_ascii=False
    )


# FINAL SUMMARY
print("\n========== AI JOB COLLECTION ==========")

print("Total AI jobs:", len(final_jobs))

print("\nJobs by source:")

for source in sorted(set(job["source"] for job in final_jobs)):
    count = sum(
        1 for job in final_jobs
        if job["source"] == source
    )

    print(source, ":", count)

print("\nSaved files:")
print("jobs_final.csv")
print("jobs_final.json")
