# Project Brainstorm

## Job Posting Analysis

**Role:** Analyst, Data — Molina Healthcare (Long Beach, CA)
**SQL requirement:** "SQL Queries experience" listed under Required Experience

**Skills the posting requires that overlap with ISBA 4715:**
- SQL querying (joins, CTEs, window functions)
- Large dataset analysis and parsing
- Finding trends and communicating insights across departments
- Dashboard/reporting experience

## Data Source Brainstorm

**Source 1 — API (structured pipeline):**
- CMS Medicare Provider Data API (`data.cms.gov`) — public REST API, no auth required, 5,000+ provider records with payment amounts, specialty codes, and service counts. Maps directly to claims analytics work.

**Source 2 — Web scrape (knowledge base):**
- Molina Healthcare investor relations page (press releases, earnings calls, financial results)
- Healthcare claims industry reports (Experian, denial rate benchmarks)
- CMS managed care regulatory filings
- Job postings for similar analyst roles (for role requirements research)

## Domain Research

**Key themes identified:**
- Medical Cost Ratio (MCR) is the primary financial health metric for managed care orgs — Molina targets ~88–89%
- Claim denial rates averaging 10–15% industry-wide; prior authorization and coding errors are top causes
- Medicaid redetermination post-COVID created significant membership volatility for Molina
- CMS managed care reporting requirements (HEDIS, EPSDT, encounter data) shape what analysts must track

## Star Schema Design

**Fact table:** `fct_cms_provider_payments` — one row per provider per specialty, with payment and service count measures

**Dimension tables:**
- `dim_provider` — NPI, name, credentials, gender
- `dim_specialty` — specialty code, description
- `dim_location` — state, ZIP, RUCA (urban/rural)

## Transferability

This project transfers to:
- Business Intelligence Analyst (healthcare or insurance)
- Junior Data Engineer (pipeline + dbt experience)
- Healthcare Reporting Analyst (CMS data familiarity)
- Managed Care Analytics roles at other payers (Centene, CVS Health, Elevance)
</content>
</invoke>