# AI Data Intelligence Platform

### FrontierAtlas – AI/Data Engineering Internship Assignment

A Python-based AI and Data Engineering platform for collecting, processing, cleaning, and organizing intelligence about AI startups, AI products, research papers, job opportunities, and AI news.

**GitHub Repository:** https://github.com/Kushal43065/ai-data-intelligence-platform

---

## 1. Project Overview

The AI Data Intelligence Platform demonstrates an end-to-end data collection and processing workflow using Python, public APIs, RSS feeds, asynchronous web crawling, and Large Language Models (LLMs).

The platform combines multiple data sources into structured datasets and provides mechanisms for data cleaning, deduplication, entity resolution, metadata extraction, and automated information processing.

The project also includes an architecture proposal for scaling the system to process more than 500,000 records.

## 2. Key Features

### Startup Data Collection
- Collects AI startup information from a public startup dataset.
- Cleans and standardizes startup records.
- Removes duplicate company names.
- Generates a structured CSV dataset.

### AI Product Collection
- Combines AI tools and developer tools datasets.
- Removes duplicate product records.
- Organizes product information into structured CSV files.

### Research Paper Metadata Extraction
- Collects research papers using the arXiv API.
- Retrieves titles, abstracts, authors, and publication dates.
- Extracts GitHub repository references.
- Collects GitHub repository metrics where available.
- Generates JSON and CSV outputs.

### AI Job Monitoring
- Collects job listings from five public job feeds:
  - Remote OK
  - Jobicy
  - Arbeitnow
  - Working Nomads
  - We Work Remotely
- Filters AI-related job titles.
- Processes publication dates.
- Removes duplicate job listings.
- Filters recent postings.

### AI News Monitoring
- Collects AI news from five RSS/Atom sources:
  - TechCrunch AI
  - The Verge AI
  - VentureBeat AI
  - MIT Technology Review
  - Google DeepMind
- Extracts article information.
- Processes publication timestamps.
- Retrieves article text where publicly accessible.

### Entity Resolution
- Normalizes startup names.
- Generates canonical startup names.
- Uses deterministic matching rules.
- Records matching methods and confidence values.
- Creates an entity mapping log.

### LLM Fallback Processing
- Integrates Google Gemini, Groq, and DeepSeek.
- Demonstrates provider fallback logic.
- Includes retry handling for rate limits.
- Includes text chunking for oversized inputs.

### Asynchronous Web Crawler
- Uses Python asyncio and aiohttp.
- Fetches multiple webpages concurrently.
- Extracts page titles and metadata.
- Saves crawl results in CSV format.

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data processing and cleaning |
| Requests | API requests |
| BeautifulSoup | HTML parsing |
| PyMuPDF | PDF text extraction |
| aiohttp | Asynchronous HTTP requests |
| Feedparser | RSS and Atom feed processing |
| Google Gemini | LLM processing |
| Groq | LLM provider integration |
| DeepSeek | LLM provider integration |
| GitHub REST API | Repository verification and metrics |
| arXiv API | Research paper collection |
| Google Sheets | Dataset organization |

---

## 4. Project Structure

```text
ai-data-intelligence-platform/
│
├── .github/
│   └── workflows/
│       ├── extraction-check.yml
│       └── python-tests.yml
│
├── src/
│   ├── collect_startups.py
│   ├── clean_startups.py
│   ├── clean_products.py
│   ├── bulk_arxiv.py
│   ├── merge_research.py
│   ├── collect_jobs.py
│   ├── collect_news.py
│   ├── entity_resolution.py
│   ├── llm_fallback.py
│   └── async_crawler.py
│
├── tests/
│   └── test_extractor.py
│
├── data/
│
├── architecture.pdf
├── crawler_strategy.md
├── requirements.txt
├── README.md
├── .gitignore
│
├── extract_paper_meta.py
├── github_metrics.py
│
├── startups_final.csv
├── products_final.csv
├── research_papers_final.csv
├── jobs_final.csv
├── news_final.csv
├── entity_mapping_log.csv
│
└── Additional JSON and source datasets
```

---

## 5. Installation and Setup

### Prerequisites

- Python 3.11 or later
- Git
- Internet connection
- API keys for the LLM services you intend to use

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kushal43065/ai-data-intelligence-platform.git

cd ai-data-intelligence-platform
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

If additional packages are required:

```bash
pip install pandas requests feedparser beautifulsoup4 lxml aiohttp google-genai groq openai python-dotenv pymupdf
```

---

## 6. API Configuration

Create a `.env` file in the root directory.

Add the API keys you have access to:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

**Security Note:** Never upload `.env` files, API keys, passwords, or other credentials to GitHub.

The `.gitignore` file excludes environment files and virtual environment folders.

---

## 7. Running the Project

Run commands from the repository root directory.

### Startup Collection

```bash
python src/collect_startups.py
python src/clean_startups.py
```

Output:

```text
startups_final.csv
```

### Product Processing

```bash
python src/clean_products.py
```

Output:

```text
products_final.csv
```

### Research Paper Collection

```bash
python src/bulk_arxiv.py
python src/merge_research.py
```

Output:

```text
research_papers_final.csv
research_papers_final.json
```

### Job Collection

```bash
python src/collect_jobs.py
```

Output:

```text
jobs_final.csv
jobs_final.json
```

### News Collection

```bash
python src/collect_news.py
```

Output:

```text
news_final.csv
news_final.json
```

### Entity Resolution

```bash
python src/entity_resolution.py
```

Output:

```text
seed_startups.csv
entity_mapping_log.csv
```

### LLM Processing

```bash
python src/llm_fallback.py
```

The script provides options to test individual providers or the automatic fallback sequence.

### Asynchronous Crawling

```bash
python src/async_crawler.py
```

Output:

```text
async_crawler_results.csv
```

### Original Research Paper Extractor

```bash
python extract_paper_meta.py
```

The original extractor downloads configured arXiv papers, extracts PDF text, and generates structured metadata.

---

## 8. Dataset Outputs

The project generates the following primary datasets:

| Dataset | Output File | Demonstrated Records |
|---|---|---:|
| AI Startups | startups_final.csv | 1,000 |
| AI Products | products_final.csv | 1,000 |
| Research Papers | research_papers_final.csv | 1,000 |
| AI Jobs | jobs_final.csv | Depends on collection run |
| AI News | news_final.csv | Depends on collection run |
| Entity Mapping | entity_mapping_log.csv | 1,000 |

Additional files include JSON datasets, GitHub metrics, and crawler results.

Record counts reflect the demonstrated collection runs and may change when scripts are executed again.

---

## 9. Google Sheets Dashboard

The collected datasets are organized into six Google Sheets tabs:

1. Startups
2. Products
3. Research Papers
4. Jobs
5. News
6. Entity Mapping Log

**Dashboard Link:**

https://docs.google.com/spreadsheets/d/1V4uM7X6ucIilq2bl9j2a24dTfezLsxiH2mSK_BSmonM/edit?usp=sharing

The spreadsheet is intended for reviewer access with Viewer permissions.

---

## 10. LLM Fallback Architecture

The project demonstrates a multi-provider LLM integration strategy.

Configured providers:

1. Google Gemini
2. Groq
3. DeepSeek

Implemented processing mechanisms include:

- Provider selection and fallback sequence.
- Retry handling for rate-limit errors.
- Text chunking for oversized prompts.
- Error handling for unavailable providers.

Gemini processing was successfully tested.

Groq and DeepSeek execution depends on available provider access, model availability, and account credits. Their complete fallback behavior has not been verified in the demonstrated run.

---

## 11. Asynchronous Crawler

The crawler uses asynchronous HTTP requests to fetch multiple webpages concurrently.

### Main Components

- aiohttp for asynchronous requests.
- asyncio for concurrent execution.
- BeautifulSoup for HTML parsing.
- CSV output for collected metadata.

### Demonstrated Result

```text
Crawling completed!

Pages successfully fetched: 4

Output: async_crawler_results.csv
```

The crawler follows responsible collection practices:

- Respects website access restrictions.
- Uses public RSS feeds and accessible pages.
- Handles HTTP errors and access restrictions.
- Does not attempt to bypass Cloudflare, DataDome, or other anti-bot systems.

See `crawler_strategy.md` for additional details.

---

## 12. Architecture and Scalability

The architecture document describes a proposed design for supporting 500,000+ records.

### Proposed Architecture Components

- Distributed asynchronous crawling workers.
- Centralized task queues.
- Scheduled data collection.
- Deduplication and entity resolution.
- Centralized storage.
- Freshness monitoring.
- LLM request management.
- Retry and error-handling mechanisms.

The architecture is designed to address:

- Large-scale data collection.
- HTTP 413 payload-size errors.
- HTTP 429 rate-limit errors.
- Duplicate records across distributed workers.
- Data freshness and consistency.

**Architecture Document:** `architecture.pdf`

The 500,000+ record capacity is a proposed architectural target. The current implementation has not been load-tested at that scale.

---

## 13. Original Research Paper OCR and Metadata Extraction

The original component retrieves five configured arXiv papers and extracts metadata from their PDFs.

### Extracted Information

- arXiv identifiers.
- Paper titles.
- Authors.
- Abstracts.
- Publication dates.
- PDF and abstract URLs.
- GitHub repository references.
- Research tasks and methods.
- Models and datasets.
- Benchmark claims.

### Extraction Method

The extractor uses the arXiv API, PyMuPDF, and heuristic extraction rules to create structured JSON records.

Repository associations and scientific claims require manual verification against the original papers.

---

## 14. Testing

Run the automated unit tests:

```bash
python -m pytest -v
```

The repository also includes GitHub Actions workflows for automated testing and extraction checks.

GitHub Actions:

https://github.com/Kushal43065/ai-data-intelligence-platform/actions

Successful automated tests indicate that the configured checks passed. They do not guarantee complete scientific accuracy or production readiness.

---

## 15. Limitations and Future Improvements

### Current Limitations

1. Heuristic extraction may miss information in complex PDF layouts.
2. GitHub repository existence does not prove association with a research paper.
3. Some entity matches require additional manual verification.
4. The asynchronous crawler demonstration fetched four webpages.
5. Groq and DeepSeek provider execution depends on available credits and access.
6. Distributed processing for 500,000+ records remains a proposed architecture rather than a fully implemented system.
7. Dataset quality and source coverage require continued validation.

### Future Improvements

- Implement distributed crawling with task queues.
- Add centralized database storage.
- Improve entity resolution with alias and fuzzy matching.
- Introduce token-aware LLM chunking.
- Add comprehensive monitoring and structured logs.
- Implement automated data-quality validation.
- Perform large-scale load testing.

---

## 16. References and Data Sources

- arXiv API: https://info.arxiv.org/help/api/
- GitHub REST API: https://docs.github.com/en/rest
- Remote OK: https://remoteok.com/
- Jobicy: https://jobicy.com/
- Arbeitnow: https://www.arbeitnow.com/
- Working Nomads: https://www.workingnomads.com/
- We Work Remotely: https://weworkremotely.com/
- TechCrunch: https://techcrunch.com/
- The Verge: https://www.theverge.com/
- VentureBeat: https://venturebeat.com/
- MIT Technology Review: https://www.technologyreview.com/
- Google DeepMind: https://deepmind.google/

---

## 17. Project Repository

**GitHub Repository:**

https://github.com/Kushal43065/ai-data-intelligence-platform

**Google Sheets Dashboard:**

https://docs.google.com/spreadsheets/d/1V4uM7X6ucIilq2bl9j2a24dTfezLsxiH2mSK_BSmonM/edit?usp=sharing

---

## 18. Project Information

**Project Name:** AI Data Intelligence Platform

**Assignment:** FrontierAtlas AI/Data Engineering Intern Trial Task

**Primary Language:** Python

**Repository:** Public GitHub Repository

**Deliverables:** Source code, structured datasets, architecture documentation, asynchronous crawler, LLM processing module, entity resolution module, and Google Sheets dashboard.