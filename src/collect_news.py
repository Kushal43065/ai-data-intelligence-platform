
import csv
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser


# -------------------------------------------------
# CONFIGURATION: FIVE AI NEWS SOURCES
# -------------------------------------------------

SOURCES = {
    "TechCrunch AI":
        "https://techcrunch.com/category/artificial-intelligence/feed/",

    "The Verge AI":
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",

    "VentureBeat AI":
        "https://venturebeat.com/category/ai/feed/",

    "MIT Technology Review":
        "https://www.technologyreview.com/topic/artificial-intelligence/feed/",

    "Google DeepMind":
        "https://deepmind.google/blog/rss.xml"
}

AI_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "generative ai",
    "large language model",
    "llm",
    "chatgpt",
    "openai",
    "google gemini",
    "computer vision",
    "neural network",
    "robotics",
    "ai model",
    "ai agent",
    "deepmind",
    "anthropic",
    "nvidia ai"
]


# -------------------------------------------------
# DOWNLOAD WEB CONTENT
# -------------------------------------------------

def fetch_url(url, timeout=30):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 AI-News-Research-Project/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


# -------------------------------------------------
# CLEAN HTML
# -------------------------------------------------

class TextExtractor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = []
        self.capture = False
        self.skip = 0

    def handle_starttag(self, tag, attrs):

        if tag in ["script", "style", "nav", "footer", "header"]:
            self.skip += 1

        if tag in ["article", "main"]:
            self.capture = True

        if tag in ["p", "h1", "h2", "h3"] and self.skip == 0:
            self.text.append("\n")

    def handle_endtag(self, tag):

        if tag in ["script", "style", "nav", "footer", "header"]:
            self.skip = max(0, self.skip - 1)

        if tag in ["article", "main"]:
            self.capture = False

    def handle_data(self, data):

        if self.skip == 0 and data.strip():
            self.text.append(data.strip())

    def get_text(self):
        return " ".join(self.text)


def clean_html(value):

    value = unescape(str(value or ""))

    parser = TextExtractor()

    try:
        parser.feed(value)
        return re.sub(r"\s+", " ", parser.get_text()).strip()
    except Exception:
        return re.sub(r"<[^>]+>", " ", value).strip()


# -------------------------------------------------
# PARSE PUBLICATION DATE
# -------------------------------------------------

def parse_date(value):

    if not value:
        return None

    try:

        value = str(value).strip()

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


# -------------------------------------------------
# EXTRACT ARTICLE FULL TEXT
# -------------------------------------------------

def get_article_text(url, fallback):

    if not url:
        return fallback

    try:

        content = fetch_url(url, timeout=20)
        html = content.decode("utf-8", errors="ignore")

        parser = TextExtractor()
        parser.feed(html)

        article_text = parser.get_text()

        article_text = re.sub(
            r"\s+", " ", article_text
        ).strip()

        if len(article_text) > 300:
            return article_text[:30000]

    except Exception:
        pass

    # Use RSS summary if article page is unavailable
    return fallback


# -------------------------------------------------
# RSS / ATOM FEED PARSER
# -------------------------------------------------

def get_tag(element, tag_name):

    for child in element.iter():

        if child.tag.split("}")[-1].lower() == tag_name.lower():
            return child

    return None


def get_text(element, tag_name):

    child = get_tag(element, tag_name)

    if child is None:
        return ""

    return "".join(child.itertext()).strip()


def get_link(element):

    for child in element:

        if child.tag.split("}")[-1].lower() == "link":

            href = child.attrib.get("href")

            if href:
                return href

            if child.text:
                return child.text.strip()

    return ""


def collect_feed(source_name, feed_url):

    collected = []

    print("\nChecking:", source_name)

    try:

        feed_content = fetch_url(feed_url)

        root = ET.fromstring(feed_content)

        items = [
            element for element in root.iter()
            if element.tag.split("}")[-1].lower()
            in ["item", "entry"]
        ]

        print("Articles found in feed:", len(items))

        for item in items:

            title = get_text(item, "title")

            link = get_link(item)

            raw_date = (
                get_text(item, "pubDate")
                or get_text(item, "published")
                or get_text(item, "updated")
                or get_text(item, "date")
            )

            published = parse_date(raw_date)

            description = (
                get_text(item, "encoded")
                or get_text(item, "description")
                or get_text(item, "summary")
                or get_text(item, "content")
            )

            description = clean_html(description)

            if not title or not link:
                continue

            # Check AI relevance
            searchable_text = (
                title + " " + description
            ).lower()

            if not any(
                keyword in searchable_text
                for keyword in AI_KEYWORDS
            ):
                continue

            # Require a valid publication date
            if published is None:
                continue

            now = datetime.now(timezone.utc)

            # Keep only articles from the last 24 hours
            if not (
                now - timedelta(hours=24)
                <= published <= now
            ):
                continue

            # Retrieve article text where publicly accessible
            full_text = get_article_text(
                link,
                description
            )

            collected.append({

                "source": source_name,

                "title": clean_html(title),

                "published_at_utc": published.isoformat(),

                "original_publication_date": raw_date,

                "article_url": link,

                "description": description,

                "full_text": full_text,

                "full_text_status": (
                    "Article text retrieved"
                    if len(full_text) > len(description) + 100
                    else "RSS summary or accessible text"
                )

            })

            # Avoid sending requests too quickly
            time.sleep(0.5)

        print("Recent AI articles:", len(collected))

    except Exception as error:

        print("Source error:", source_name, error)

    return collected


# -------------------------------------------------
# COLLECT FROM ALL FIVE SOURCES
# -------------------------------------------------

all_news = []

for source_name, feed_url in SOURCES.items():

    news = collect_feed(source_name, feed_url)

    all_news.extend(news)


# -------------------------------------------------
# REMOVE DUPLICATES
# -------------------------------------------------

unique_news = {}

for article in all_news:

    key = article["article_url"].strip().lower()

    if key:
        unique_news[key] = article


final_news = list(unique_news.values())


# -------------------------------------------------
# SAVE CSV
# -------------------------------------------------

fields = [
    "source",
    "title",
    "published_at_utc",
    "original_publication_date",
    "article_url",
    "description",
    "full_text",
    "full_text_status"
]

with open(
    "news_final.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fields
    )

    writer.writeheader()
    writer.writerows(final_news)


# -------------------------------------------------
# SAVE JSON
# -------------------------------------------------

with open(
    "news_final.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        final_news,
        file,
        indent=2,
        ensure_ascii=False
    )


# -------------------------------------------------
# FINAL REPORT
# -------------------------------------------------

print("\n========== AI NEWS COLLECTION REPORT ==========")

print("Total recent AI news articles:", len(final_news))

print("\nArticles collected per source:")

for source in SOURCES:

    count = sum(
        1 for article in final_news
        if article["source"] == source
    )

    print(source, ":", count)


print("\nFull-text status:")

for status in set(
    article["full_text_status"]
    for article in final_news
):

    count = sum(
        1 for article in final_news
        if article["full_text_status"] == status
    )

    print(status, ":", count)


print("\nSaved files:")
print("news_final.csv")
print("news_final.json")

print("\nCollection completed!")
