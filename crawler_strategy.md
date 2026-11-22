
# Web Crawler Strategy

## 1. Asynchronous Crawling
The crawler uses Python asyncio and aiohttp to fetch multiple pages concurrently, improving collection efficiency.

## 2. Anti-Bot Protection
Some websites use Cloudflare and DataDome to protect their content.

The crawler does not attempt to bypass these security mechanisms.

## 3. Handling HTTP Errors
- HTTP 403: Skip pages where access is forbidden.
- HTTP 429: Respect rate limits and retry after an appropriate delay.
- HTTP 5xx: Retry temporary server failures with exponential backoff.
- Timeout: Record the failed request and continue.

## 4. Data Collection Alternatives
- Prefer official APIs.
- Use publicly available RSS and Atom feeds.
- Respect robots.txt, website terms, and access restrictions.
- Use authorized access when required.

## 5. Logging
Record failed URLs, HTTP status codes, timestamps, and error messages for later review.

## 6. Scalability
For large-scale crawling, use distributed workers, a task queue, deduplication, and centralized storage.
