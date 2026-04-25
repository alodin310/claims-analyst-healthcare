import os
import requests
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://data.cms.gov/data-api/v1/dataset/92396110-2aed-4d63-a6a2-5d6207d46a29/data"
LIMIT = 1000
OFFSET = 0
MAX_ROWS = 5000
ALL_ROWS = []

print("Fetching data from CMS API...")
while len(ALL_ROWS) < MAX_ROWS:
    response = requests.get(API_URL, params={"limit": LIMIT, "offset": OFFSET})
    response.raise_for_status()
    batch = response.json()
    if not batch:
        break
    ALL_ROWS.extend(batch)
    print(f"  Fetched {len(ALL_ROWS)} rows so far...")
    OFFSET += LIMIT

print(f"Total rows fetched: {len(ALL_ROWS)}")

if not ALL_ROWS:
    raise ValueError("No data returned from API.")

COLUMNS = list(ALL_ROWS[0].keys())

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

col_defs = ", ".join([f'"{col}" STRING' for col in COLUMNS])
cursor.execute(f'DROP TABLE IF EXISTS RAW.CMS_MEDICARE_PROVIDERS')
cursor.execute(f'CREATE TABLE RAW.CMS_MEDICARE_PROVIDERS ({col_defs})')

placeholders = ", ".join(["%s"] * len(COLUMNS))
insert_sql = f'INSERT INTO RAW.CMS_MEDICARE_PROVIDERS VALUES ({placeholders})'

batch_size = 500
for i in range(0, len(ALL_ROWS), batch_size):
    batch = ALL_ROWS[i:i + batch_size]
    rows = [tuple(str(row.get(col, "")) for col in COLUMNS) for row in batch]
    cursor.executemany(insert_sql, rows)
    print(f"  Inserted {min(i + batch_size, len(ALL_ROWS))} / {len(ALL_ROWS)} rows...")

conn.commit()
cursor.close()
conn.close()

print("Done. Data loaded into CLAIMS_HEALTHCARE.RAW.CMS_MEDICARE_PROVIDERS")
