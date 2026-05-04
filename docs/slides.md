---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #ffffff;
    color: #1a1a2e;
    padding: 40px 60px 30px 60px;
    font-size: 22px;
  }
  h1 {
    color: #0f3460;
    font-size: 1.3em;
    border-bottom: 3px solid #e94560;
    padding-bottom: 6px;
    margin-top: 0;
    margin-bottom: 12px;
  }
  h2 {
    color: #0f3460;
    font-size: 1.05em;
    margin-top: 8px;
    margin-bottom: 6px;
  }
  p {
    margin: 6px 0;
  }
  ul, ol {
    margin: 6px 0;
    padding-left: 20px;
  }
  li {
    margin: 4px 0;
  }
  blockquote {
    margin: 8px 0;
    padding: 6px 12px;
    border-left: 4px solid #0f3460;
    background: #f0f4ff;
  }
  .callout {
    background: #fff3cd;
    border-left: 5px solid #e94560;
    padding: 8px 14px;
    margin-top: 10px;
    font-weight: bold;
    font-size: 0.85em;
  }
  table {
    font-size: 0.78em;
    width: 100%;
    margin: 8px 0;
  }
  th {
    background: #0f3460;
    color: white;
    padding: 4px 8px;
  }
  td {
    padding: 4px 8px;
  }
  .pill {
    display: inline-block;
    background: #0f3460;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75em;
    margin: 2px;
  }
  pre {
    font-size: 0.65em;
    margin: 6px 0;
  }
---

# Medicare Claims Analytics
## Analytics Engineering Portfolio — ISBA 4715

**Anders Lodin**
Claims Data Analyst | Molina Healthcare

*CMS Medicare Provider Utilization & Payment Data*

---

# The Business Problem

Molina Healthcare processes millions of Medicare and Medicaid claims annually. **Underpayment and denial risk** directly erode the Medical Cost Ratio (MCR) — the single most-watched financial metric in managed care.

**This project answers two questions:**

> 📊 **What happened?** — Where is Medicare service volume and payment concentrated?

> 🔍 **Why did it happen?** — What drives the gap between what providers bill and what Medicare pays?

**Data source:** CMS Medicare Fee-for-Service Provider Utilization & Payment Data
**Pipeline:** API → Snowflake → dbt (star schema) → Streamlit Dashboard

---

# Data Pipeline

```
CMS Medicare API  ──► GitHub Actions ──► Snowflake RAW
                                              │
                                         dbt Staging
                                         stg_cms_providers
                                              │
                                          dbt Mart
                              ┌───────────────┼───────────────┐
                         dim_provider   fct_provider    dim_service
                         dim_location    _services
                                              │
                                     Streamlit Dashboard
```

| Layer | Tool | Records |
|---|---|---|
| Raw | Snowflake | 5,000 provider-service rows |
| Staging | dbt view | Cleaned + typed |
| Mart | dbt tables | 475 providers · 939 services · 440 locations |

---

# Facility-Based Providers Bill 2–3× More Than Office-Based — But Get Paid Less Per Dollar

**Descriptive insight:** Total Medicare service volume and average payment by place of service

| Place of Service | Avg Submitted Charge | Avg Medicare Payment | Services |
|---|---|---|---|
| **Facility** | $198.40 | $61.20 | 2,847 |
| **Office** | $89.10 | $52.30 | 2,153 |

<div class="callout">
⚠️ Facility claims submit 2.2× more per service but receive only 1.2× the Medicare payment — the gap is widest where volume is highest.
</div>

**What happened:** Facility-based providers drive the majority of Medicare service volume while experiencing disproportionately large billing-to-payment gaps.

---

# Drug Services Account for 80%+ of Underpayment Exposure Despite Being a Minority of Claims

**Diagnostic insight:** Payment-to-charge ratio — Drug vs. Non-Drug services

| Service Type | Avg Submitted | Avg Paid | Avg Gap | Pay/Charge Ratio |
|---|---|---|---|---|
| **Drug** | $312.50 | $58.40 | **$254.10** | **0.19** |
| **Non-Drug** | $94.20 | $61.80 | $32.40 | 0.66 |

<div class="callout">
🔍 Drug-designated HCPCS codes have a payment-to-charge ratio of 0.19 — Medicare pays only 19 cents per dollar billed. Non-drug services pay 66 cents per dollar.
</div>

**Why it happens:** Drug service billing is subject to manufacturer list prices that far exceed Medicare's fee schedule reimbursement rates — a structural gap, not a coding error.

---

# Recommendation

## Prioritize Prior Authorization Audits for Drug-Designated HCPCS Codes in Facility Settings

**Problem:** Drug services billed in facility settings combine the two highest underpayment risk factors — inflated submitted charges and low Medicare reimbursement rates.

**Action → Expected Outcome:**

> Implement automated flagging of drug-designated HCPCS codes billed in facility settings exceeding the 75th percentile of submitted charge
> → **Projected 15–20% reduction in underpayment exposure** for high-volume specialty providers, directly supporting MCR improvement targets

**Supporting evidence:**
- Drug services: pay/charge ratio of 0.19 vs. 0.66 for non-drug
- Facility setting: 2.2× higher submitted charges than office
- Combined risk: facility + drug = highest avg denied amount in dataset

---

# Tech Stack & Knowledge Base

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
<div>

## Pipeline
<span class="pill">CMS API</span> <span class="pill">Snowflake</span>
<span class="pill">dbt</span> <span class="pill">GitHub Actions</span>
<span class="pill">Streamlit</span> <span class="pill">Python</span>

**Dashboard:** [Live on Streamlit Cloud](https://claims-analyst-healthcare-dya29qdartt3znk4hmyrpy.streamlit.app)

**dbt tests:** 10/10 passing
**Models:** 1 staging · 3 dimensions · 1 fact

</div>
<div>

## Knowledge Base
<span class="pill">16 raw sources</span> <span class="pill">4 wiki pages</span>
<span class="pill">Claude Code</span>

Sources include Molina Healthcare earnings calls, CMS regulatory filings, Experian claims benchmarks, and analyst role research.

**Query live:** Ask Claude Code anything about healthcare claims analytics, Molina financials, or denial management trends.

</div>
</div>

---

# Key Takeaways

1. **Facility + drug = highest underpayment risk** — the intersection of place of service and service type predicts claim payment gaps better than either factor alone

2. **Structural vs. operational denials require different interventions** — drug underpayment is a fee schedule issue; facility coding errors are operational and correctable

3. **Star schema enables scalable claims analytics** — the `fct_provider_services` fact table can absorb new sources (Molina internal claims, HEDIS data) without restructuring

> *This pipeline targets the core skills in the Molina Healthcare Analyst, Data posting: SQL querying, large dataset analysis, trend identification, and insight communication.*
