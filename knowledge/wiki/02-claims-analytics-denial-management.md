# Healthcare Claims Analytics & Denial Management

## The Scale of the Problem

Claim denials have become one of the most financially consequential challenges in U.S. healthcare. In 2024, initial denial rates averaged **11.81%** across payers — up from ~10.2% in prior years and trending higher. Among ACA marketplace plans, roughly 49 million in-network claims were denied in 2023 alone. Medicare Advantage initial denials average ~15.7%; commercial payers average ~13.9%.

For managed care organizations like Molina Healthcare, this isn't just a provider-side problem — it's a two-sided analytical challenge. Molina both *pays* claims (and must deny those that fail medical necessity, authorization, or eligibility criteria) and *reports* claim outcomes to CMS and state regulators who audit denial rates as part of managed care oversight.

**Sources:** [US Healthcare Denial Rates & Statistics 2026](../raw/08-us-healthcare-denial-rates-reimbursement-stats.md) · [Average Denial Rate 2025 Benchmarks](../raw/11-average-claim-denial-rate-2025-benchmarks.md)

---

## Why Claims Are Denied: Root Cause Breakdown

The sources converge on a consistent picture of denial root causes, though they differ on which is "top":

| Root Cause | Key Stat |
|---|---|
| Inaccurate/incomplete patient data at intake | 26% of denials; 68% of providers cite as primary driver |
| Prior authorization errors (missing/incorrect) | Top-3 cause across multiple surveys |
| Coding inaccuracies (ICD-10, CPT) | Up to 49% of claims affected by "routine" coding issues |
| Eligibility/coverage verification errors | Frequently top-5 across surveys |
| Medical necessity documentation gaps | Rose 5% in 2024; especially for emergency services and telehealth |
| Administrative errors (wrong member ID, demographics) | Cited in Experian and AHA data |

**The deeper pattern:** Most denials are preventable, and most preventable denials originate *upstream* — in scheduling, intake, eligibility verification, and prior authorization workflows — not in billing. This means the analytical leverage point is pre-submission data quality, not post-denial rework.

Where sources disagree: Experian's 2025 State of Claims report emphasizes "bad data" as the primary culprit; the Forvis Mazars managed care report and the RapidClaims analysis both put prior authorization and medical necessity documentation higher. The divergence likely reflects different payer mixes in the survey populations (commercial vs. Medicare Advantage vs. Medicaid).

**Sources:** [Experian State of Claims 2025](../raw/10-experian-state-of-claims-report-2025.md) · [Managed Care Denials Trends](../raw/09-managed-care-denials-trends-mitigate.md) · [Average Denial Rate 2025](../raw/11-average-claim-denial-rate-2025-benchmarks.md)

---

## Financial Impact

The cost of denials compounds through the entire revenue cycle:

- **Administrative cost per denied claim:** rose from $43.84 (2022) to $57.23 (2023) — a 31% increase in one year
- **Hospitals spent $19.7 billion** challenging denied claims in a single year (AHA)
- **35–60% of denied claims are never resubmitted**, representing pure revenue loss
- **Labor is ~90% of claims processing expense** — denials multiply labor costs directly
- Average cost to rework a single denied claim: **$25–$181** depending on complexity

For a managed care organization like Molina, the financial calculus runs in both directions. When Molina denies a claim correctly, it reduces MCR (good for margins). When Molina denies a claim that gets overturned on appeal, it pays the original claim *plus* administrative overhead. In Medicare Advantage, **57% of initial denials are ultimately overturned** on appeal — suggesting systematic over-denial is both costly and regulatory-risk-laden.

**Sources:** [US Healthcare Denial Statistics](../raw/08-us-healthcare-denial-rates-reimbursement-stats.md) · [Managed Care Denials](../raw/09-managed-care-denials-trends-mitigate.md)

---

## The Emerging AI Dynamic

A notable shift since 2022: payers are increasingly deploying AI to automate denial decisions, while providers are increasingly deploying AI to prevent denials before submission and automate appeals.

**On the payer side:**
- Denials triggered by Requests for Information (RFIs) increased 9% from 2022 to 2024 — driven largely by AI-initiated documentation requests
- Algorithmic denial systems (e.g., nH Predict) are alleged to drive automatic denials of 50–75% of decisions in some cases
- Documentation requests are expanding into lower-dollar claims that historically cleared automatically

**On the provider/analytics side:**
- 67% of providers believe AI could improve the claims process; only 14% currently use it
- Of those using AI, 69% report reduced denial rates and/or improved resubmission success
- AI tools focus on: pre-submission claim scrubbing, ICD-10/CPT code validation, HCC v28 compliance, eligibility verification automation

**The analytical implication:** A claims data analyst at Molina in 2026 is working in an environment where both sides of the payer-provider dynamic are increasingly automated. Analysts who can build and interpret denial pattern models — not just run denial rate reports — will be more valuable.

**Sources:** [US Denial Statistics](../raw/08-us-healthcare-denial-rates-reimbursement-stats.md) · [Experian State of Claims](../raw/10-experian-state-of-claims-report-2025.md) · [Average Denial Rate 2025](../raw/11-average-claim-denial-rate-2025-benchmarks.md)

---

## CMS Reporting & Regulatory Oversight

Managed care organizations like Molina operate under CMS managed care reporting requirements that impose structured data obligations. CMS tracks:

- **Improper payment rates**: Medicare FFS at 7.38%; Medicare Part C (MA) at 5.61%; Medicare Part D at ~3.7% — combined Medicare + Medicaid improper payments exceeded $100 billion in FY2023
- **Denial rate monitoring** as part of MA plan auditing and state Medicaid contract oversight
- **T-MSIS (Transformed Medicaid Statistical Information System)**: the primary federal data infrastructure for Medicaid claims analytics, used by CMS to monitor managed care plan performance and detect fraud, waste, and abuse

For a claims analyst at Molina, T-MSIS familiarity is a differentiator — job postings specifically for Medicaid claims analytics (e.g., at GDIT supporting CMS) list T-MSIS experience as a required skill.

### The Three CMS Managed Care Reports

Under the May 2016 final rule (42 CFR § 438), states administering managed care programs must submit three structured reports to CMS annually:

1. **MCPAR (Managed Care Program Annual Report)** — due 180 days after close of each contract year. Covers plan performance, appeals and grievances, access, and quality measures. CMS publishes Public Use Files (PUFs) on data.medicaid.gov, making this a publicly accessible research dataset.

2. **MLR Summary Report** (42 CFR § 438.74) — requires states to report the Medical Loss Ratio for each managed care plan. This is the regulatory mechanism that enforces MCR floors — if a plan's MLR falls below the minimum, it must issue rebates to the state. For analysts at Molina, understanding the MLR report structure is essential for connecting internal MCR calculations to what gets reported to regulators.

3. **NAAAR (Network Adequacy and Access Assurances Report)** — tracks whether plans maintain adequate provider networks for enrollees.

All three reports flow through CMS's **MDCT-MCR portal** (Medicaid Data Collection Tool for Managed Care Reporting). For a claims data analyst, the MCPAR appeals/grievances data and the MLR Summary Report are the most directly relevant — they shape what internal denial and cost data must ultimately reconcile to.

**Sources:** [CMS Medicaid Managed Care Reporting](../raw/16-cms-medicaid-managed-care-reporting.md) · [US Denial Statistics](../raw/08-us-healthcare-denial-rates-reimbursement-stats.md)

---

## Analytical Framework for Denial Management

Industry best practice from Forvis Mazars and other sources converges on a six-component framework that shapes how analytics teams structure their work:

1. **Upstream prevention metrics**: Track denial rates at point of intake/eligibility, not just after submission
2. **Segmented analytics**: Denial rates by payer, denial reason, service type, provider — not just aggregate rate
3. **Overturn rate tracking**: Appeals success by payer is a signal of systematic over-denial vs. legitimate denials
4. **Days to resolution**: Measures operational efficiency of the denial management cycle
5. **Payer engagement data**: Trended denial data by payer, used in provider relations negotiations
6. **Automation ROI tracking**: Pre/post metrics for AI or automation tools

The key insight: treating denial rate as a single KPI obscures the analytical story. A 10% denial rate that's 80% preventable is a different problem than a 10% rate that's driven by legitimate medical necessity determinations.

*Cross-reference: → [Molina Healthcare Overview](01-molina-healthcare-overview.md) for how denial patterns connect to MCR and company financials* · → [Claims Data Analyst Role](03-claims-data-analyst-role.md) for the skills needed to build these analytics
