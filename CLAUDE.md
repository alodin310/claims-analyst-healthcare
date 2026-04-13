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

### How to Query the Knowledge Base

To query the knowledge base, open Claude Code in this repo and ask a question. Claude Code should:

1. Read `knowledge/index.md` first to understand what wiki pages exist.
2. Read the relevant wiki page(s) from `knowledge/wiki/` to answer the question from synthesized knowledge.
3. Fall back to raw sources in `knowledge/raw/` if the wiki pages don't fully answer the question.
4. Cite which wiki page or raw source the answer comes from.

Example queries:
- "What does my knowledge base say about healthcare claims denial rates?"
- "What are the key regulatory requirements affecting claims processing at Molina Healthcare?"
- "What trends in managed care does my knowledge base cover?"

### How to Update the Knowledge Base

When adding new raw sources:
1. Save the file to `knowledge/raw/` with a descriptive filename.
2. Update `knowledge/index.md` to reflect the new source.
3. Update or create relevant wiki pages in `knowledge/wiki/` to synthesize the new information with existing knowledge.
4. Commit with a message like `knowledge: add [source name]`.

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
