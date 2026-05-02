# CLAUDE.md — Claims Analyst Healthcare

## Project Overview

This is an analytics engineering portfolio project for ISBA 4715 (SQL & Analytics Engineering) at LMU. The project targets a **Claims Data Analyst** role at **Molina Healthcare** and demonstrates the ability to build an end-to-end data pipeline using industry-standard tools.

**Student:** Anders Lodin
**Repo:** https://github.com/alodin310/claims-analyst-healthcare
**Job Posting:** `docs/job-posting.pdf` (Molina Healthcare — Analyst, Data)

---

## What This Project Builds

**Structured data path:**
API Source → GitHub Actions → Snowflake (raw schema) → dbt (staging → mart/star schema) → Streamlit Dashboard

**Knowledge base path:**
Web scrape / documents → GitHub Actions → `knowledge/raw/` → Claude Code synthesis → `knowledge/wiki/`

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data Warehouse | Snowflake (trial, AWS US East 1) |
| Transformation | dbt |
| Orchestration | GitHub Actions (scheduled) |
| Dashboard | Streamlit (deployed to Community Cloud) |
| Knowledge Base | Claude Code (scrape → summarize → query) |
| Version Control | Git + GitHub (public repo) |

---

## Directory Structure

```
.
├── .github/workflows/    # GitHub Actions pipeline definitions
├── extract/              # Python extraction scripts (API + web scrape)
├── dbt_project/          # dbt models, tests, and schema definitions
├── streamlit_app/        # Streamlit dashboard code
├── knowledge/
│   ├── raw/              # Raw scraped sources (15+ files, 3+ sites/authors)
│   └── wiki/             # Claude Code-generated synthesis wiki pages
├── docs/                 # Proposal, job posting, pipeline diagram, ERD, slides, resume
├── .env.example          # Required environment variable keys (no values)
├── .gitignore
├── CLAUDE.md             # This file
└── README.md
```

---

## Environment Variables

Never commit real credentials. Copy `.env.example` to `.env` and fill in your values. Required variables:

```
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_WAREHOUSE=
```

Add any API keys or scraping service credentials as needed.

---

## dbt Project Conventions

- Raw data lands in Snowflake `raw` schema
- Staging models: `stg_<source>_<entity>.sql` — clean, rename, cast types
- Mart models: fact and dimension tables forming a star schema
- All models must pass `dbt test` before committing
- `dbt run` and `dbt test` must execute without errors

---

## Knowledge Base

The `knowledge/` folder is a Claude Code-curated knowledge base about the healthcare claims analytics domain.

### Structure

- `knowledge/raw/` — Unstructured source files scraped from the web (company pages, press releases, earnings calls, research papers, regulatory filings, etc.). At least 15 sources from at least 3 different sites or authors.
- `knowledge/wiki/` — Claude Code-generated synthesis wiki pages. At least 3 pages: an overview, a key entities/themes page, and one synthesis page.
- `knowledge/index.md` — Index of all wiki pages with one-line summaries.

### Knowledge Base Schema

Three operations govern how this knowledge base is maintained and used:

#### Ingest
When a new source lands in `knowledge/raw/`:
1. Read the new file and identify which domain theme(s) it covers (company financials, claims analytics, analyst role, regulatory).
2. Update the relevant wiki page(s) in `knowledge/wiki/` to synthesize the new information — add a new section or expand an existing one, with a citation back to the raw file.
3. Add a row to the appropriate table in `knowledge/index.md` (both the Raw Sources section and any cross-reference updates).
4. Commit with message: `knowledge: ingest [short description of source]`.

#### Query
When asked a question about healthcare claims analytics, Molina Healthcare, or the Claims Data Analyst role:
1. Read `knowledge/index.md` first — identify which wiki page(s) are relevant.
2. Read those wiki page(s) to produce a synthesized answer with citations.
3. Only open raw files in `knowledge/raw/` if the wiki page doesn't fully answer the question or if direct quotes/data are needed.
4. Always cite: "per [wiki page or raw filename]" at the end of each answer.

#### Lint
Periodically (or when the corpus has grown significantly), scan the knowledge base for quality issues:
1. **Contradictions** — do any wiki pages make conflicting claims about MCR thresholds, denial rates, or role requirements? Flag and resolve using the most recent source.
2. **Stale claims** — financial figures (MCR, premium revenue, membership counts) are time-sensitive. Flag anything older than 2 quarters as potentially stale.
3. **Orphan pages** — wiki pages not linked from `knowledge/index.md` or not cross-referenced by any other page.
4. **Missing cross-references** — if two wiki pages cover related topics but don't link to each other, add the link.
5. Commit lint fixes with message: `knowledge: lint [what was fixed]`.

---

### How to Query the Knowledge Base (Quick Reference)

Example queries:
- "What does my knowledge base say about healthcare claims denial rates?"
- "What are the key regulatory requirements affecting claims processing at Molina Healthcare?"
- "What trends in managed care does my knowledge base cover?"
- "What technical skills does the Molina Analyst, Data role require?"

### How to Update the Knowledge Base

When adding new raw sources:
1. Save the file to `knowledge/raw/` with a descriptive filename.
2. Run the **Ingest** operation above.
3. Commit with a message like `knowledge: ingest [source name]`.

---

## Milestones

| Milestone | Due | Key Deliverables |
|---|---|---|
| Proposal | Apr 13, 2026 | `docs/job-posting.pdf`, `docs/proposal.md`, repo initialized |
| Milestone 01 | Apr 27, 2026 | API extraction, Snowflake raw, dbt staging + mart, GitHub Actions, pipeline diagram |
| Milestone 02 | May 4, 2026 | Web scrape source, Streamlit dashboard (deployed), knowledge base, README, ERD, slides |
| Final | May 11, 2026 | `docs/resume.pdf`, live demo/interview |

---

## Security Reminders

- Never commit `.env` files or any file containing real credentials
- Use GitHub Actions secrets for CI/CD credentials
- The `.gitignore` excludes `.env` and common secret file patterns
