
import asyncio
import aiohttp
import csv
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlparse

URLS = [
    "https://techcrunch.com/category/artificial-intelligence/",
    "https://www.theverge.com/ai-artificial-intelligence",
    "https://venturebeat.com/category/ai/",
    "https://www.technologyreview.com/topic/artificial-intelligence/",
    "https://deepmind.google/blog/"
]

HEADERS = {
    "User-Agent": "AcademicResearchCrawler/1.0 (educational project)"
}

async def fetch_page(session, url):
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=20)
        ) as response:

            if response.status != 200:
                print(f"Skipped {url}: HTTP {response.status}")
                return None

            html = await response.text()
            soup = BeautifulSoup(html, "lxml")

            title = soup.title.get_text(strip=True) if soup.title else ""

            description_tag = soup.find(
                "meta", attrs={"name": "description"}
            )

            description = (
                description_tag.get("content", "")
                if description_tag else ""
            )

            return {
                "source": urlparse(url).netloc,
                "url": url,
                "title": title,
                "description": description,
                "crawled_at_utc": datetime.now(
                    timezone.utc
                ).isoformat()
            }

    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        print(f"Request failed for {url}: {error}")
        return None

async def main():
    connector = aiohttp.TCPConnector(limit=5)

    async with aiohttp.ClientSession(
        headers=HEADERS,
        connector=connector
    ) as session:

        tasks = [fetch_page(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)

    records = [item for item in results if item is not None]

    if records:
        with open(
            "async_crawler_results.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=records[0].keys()
            )
            writer.writeheader()
            writer.writerows(records)

    print("\nCrawling completed!")
    print("Pages successfully fetched:", len(records))
    print("Output: async_crawler_results.csv")

if __name__ == "__main__":
    asyncio.run(main())
