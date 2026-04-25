import os
import json
import snowflake.connector
from firecrawl import V1FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

app = V1FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])

BASE = "https://investors.molinahealthcare.com/news-releases/news-release-details"

KNOWN_SLUGS = [
    "molina-healthcare-reports-first-quarter-2026-financial-results",
    "molina-healthcare-announces-first-quarter-2026-earnings-release",
    "molina-healthcare-reports-fourth-quarter-and-year-end-2025",
    "molina-healthcare-reports-third-quarter-2025-financial-results",
    "molina-healthcare-reports-second-quarter-2025-financial-results",
    "molina-healthcare-reports-first-quarter-2025-financial-results",
    "molina-healthcare-reports-fourth-quarter-and-year-end-2024",
    "molina-healthcare-reports-third-quarter-2024-financial-results",
    "molina-healthcare-reports-second-quarter-2024-financial-results",
    "molina-healthcare-reports-first-quarter-2024-financial-results",
    "molina-healthcare-reports-fourth-quarter-and-year-end-2023",
    "molina-healthcare-reports-third-quarter-2023-financial-results",
    "molina-healthcare-reports-second-quarter-2023-financial-results",
    "molina-healthcare-reports-first-quarter-2023-financial-results",
    "molina-healthcare-reports-fourth-quarter-and-year-end-2022",
    "molina-healthcare-reports-third-quarter-2022-financial-results",
    "molina-healthcare-reports-second-quarter-2022-financial-results",
    "molina-healthcare-reports-first-quarter-2022-financial-results",
]

all_links = [f"{BASE}/{slug}" for slug in KNOWN_SLUGS]
print(f"Prepared {len(all_links)} press release URLs to attempt.")

if not all_links:
    raise ValueError("No press release URLs discovered.")

print("Scraping individual press release pages...")
pages = []
for url in all_links:
    try:
        result = app.scrape_url(url, formats=["markdown"])
        pages.append({
            "url": url,
            "title": result.title or "",
            "markdown": result.markdown or "",
            "metadata": result.metadata if isinstance(result.metadata, dict) else {},
        })
        print(f"  Scraped: {(result.title or url)[:70]}")
    except Exception as e:
        print(f"  Skipped {url}: {e}")

print(f"\nSuccessfully scraped {len(pages)} pages.")

conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    database=os.environ["SNOWFLAKE_DATABASE"],
    warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
)
cursor = conn.cursor()

cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {os.environ['SNOWFLAKE_DATABASE']}.RAW")
cursor.execute(f"USE SCHEMA {os.environ['SNOWFLAKE_DATABASE']}.RAW")

cursor.execute("DROP TABLE IF EXISTS RAW.MOLINA_NEWS_RELEASES")
cursor.execute("""
    CREATE TABLE RAW.MOLINA_NEWS_RELEASES (
        url        STRING,
        title      STRING,
        markdown   STRING,
        metadata   STRING,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
    )
""")

insert_sql = "INSERT INTO RAW.MOLINA_NEWS_RELEASES (url, title, markdown, metadata) VALUES (%s, %s, %s, %s)"
for page in pages:
    cursor.execute(insert_sql, (page["url"], page["title"], page["markdown"], json.dumps(page["metadata"])))

conn.commit()
cursor.close()
conn.close()

print(f"Done. {len(pages)} rows loaded into CLAIMS_HEALTHCARE.RAW.MOLINA_NEWS_RELEASES")
