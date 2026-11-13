# AI Governance Risk Assessment

A GRC tool that assesses AI use cases against the **NIST AI Risk Management
Framework (AI RMF)** — GOVERN / MAP / MEASURE / MANAGE — with control themes
from **ISO/IEC 42001** (AI management systems). Each use case is tiered by
inherent risk, the governance controls required at that tier are derived
automatically, and the tool flags the specific gaps in the recorded control
posture — producing a per-use-case checklist and a portfolio-level summary.

## The problem it solves

Organisations are deploying AI faster than they are governing it. A chatbot,
a screening tool, and an autonomous fraud model often sit in the same
spreadsheet with the same (or no) controls, even though their risk profiles
differ enormously. This tool operationalises the first step of an AI
governance programme: **inventory → tier by inherent risk → require
proportionate controls → evidence the gaps**. It gives GRC teams a
repeatable, framework-mapped starting point for an AI risk register instead
of a blank page.

## How tiering works

Each use case is scored additively on five factors:

| Factor | Values (points) |
|---|---|
| Data sensitivity | public 0 · internal 1 · confidential 2 · restricted 3 |
| Autonomy | assistive 0 · semi-autonomous 2 · autonomous 3 |
| Human oversight | required 0 · spot-check 1 · none 3 |
| User impact | low 0 · medium 1 · high 3 |
| Model source | in-house 0 · third-party 1 |

Score → tier: **0–3 Low · 4–6 Moderate · 7–9 High · 10+ Critical**.
Required controls are cumulative by tier (12 controls in the catalogue,
each mapped to an AI RMF subcategory and an ISO/IEC 42001 theme). At High
tier and above, third-party models additionally require vendor due
diligence. In a real programme, Critical tier would also trigger executive
approval and board-level reporting before deployment.

## How to run

Demo mode (bundled fictional portfolio — 6 use cases):

```bash
python3 assess.py --demo
```

Assess your own inventory, in the same JSON format as
`data/use_cases.json`:

```bash
python3 assess.py --input my_use_cases.json
```

Requirements: Python 3.8+, standard library only.

## Demo output (actual run)

```
==========================================================================
AI GOVERNANCE RISK ASSESSMENT — NIST AI RMF / ISO-IEC 42001
==========================================================================
Use cases assessed: 6

--- HR Screening Assistant (People Operations)
    data_sensitivity=restricted (3), autonomy=semi-autonomous (2), human_oversight=spot-check (1), user_impact=high (3), model_source=third-party (1)
    Inherent risk score: 10  ->  Tier: CRITICAL
      [OK ] AI inventory registration & named owner  [GOVERN 1.1; ISO 42001: AIMS scope & responsibilities]
      [OK ] Documented risk assessment  [MAP 1.1 / MAP 5.1; ISO 42001: AI risk assessment process]
      [GAP] User disclosure that AI is in use  [GOVERN 4.2; ISO 42001: Transparency & communication]
      [OK ] Data governance & provenance review  [MAP 2.2; ISO 42001: Data for AI systems]
      [OK ] Pre-deployment performance evaluation  [MEASURE 2.6; ISO 42001: Verification & validation]
      [GAP] Ongoing monitoring & drift checks  [MANAGE 4.1; ISO 42001: Operation & monitoring]
      [OK ] Access & change control for models/prompts  [GOVERN 2.2; ISO 42001: Operational planning & control]
      [GAP] Periodic re-assessment  [MANAGE 4.3; ISO 42001: Performance evaluation / review]
      [GAP] Bias & fairness testing  [MEASURE 2.11; ISO 42001: Fairness & bias management]
      [GAP] Human oversight & override procedure  [MANAGE 2.4; ISO 42001: Human oversight of AI]
      [GAP] AI incident response process  [MANAGE 4.2; ISO 42001: Incident management]
      [GAP] Third-party model due diligence  [GOVERN 6.1; ISO 42001: Third-party relationships]
    >> 7 gap(s) requiring remediation

--- Customer Support Chatbot (Customer Experience)
    data_sensitivity=confidential (2), autonomy=semi-autonomous (2), human_oversight=spot-check (1), user_impact=medium (1), model_source=third-party (1)
    Inherent risk score: 7  ->  Tier: HIGH
      [OK ] AI inventory registration & named owner  [GOVERN 1.1; ISO 42001: AIMS scope & responsibilities]
      [OK ] Documented risk assessment  [MAP 1.1 / MAP 5.1; ISO 42001: AI risk assessment process]
      [GAP] User disclosure that AI is in use  [GOVERN 4.2; ISO 42001: Transparency & communication]
      [OK ] Data governance & provenance review  [MAP 2.2; ISO 42001: Data for AI systems]
      [OK ] Pre-deployment performance evaluation  [MEASURE 2.6; ISO 42001: Verification & validation]
      [OK ] Ongoing monitoring & drift checks  [MANAGE 4.1; ISO 42001: Operation & monitoring]
      [GAP] Access & change control for models/prompts  [GOVERN 2.2; ISO 42001: Operational planning & control]
      [GAP] Periodic re-assessment  [MANAGE 4.3; ISO 42001: Performance evaluation / review]
      [GAP] Bias & fairness testing  [MEASURE 2.11; ISO 42001: Fairness & bias management]
      [OK ] Human oversight & override procedure  [MANAGE 2.4; ISO 42001: Human oversight of AI]
      [GAP] AI incident response process  [MANAGE 4.2; ISO 42001: Incident management]
      [OK ] Third-party model due diligence  [GOVERN 6.1; ISO 42001: Third-party relationships]
    >> 5 gap(s) requiring remediation

--- Internal Code Assistant (Engineering)
    data_sensitivity=confidential (2), autonomy=assistive (0), human_oversight=required (0), user_impact=medium (1), model_source=third-party (1)
    Inherent risk score: 4  ->  Tier: MODERATE
      [OK ] AI inventory registration & named owner  [GOVERN 1.1; ISO 42001: AIMS scope & responsibilities]
      [OK ] Documented risk assessment  [MAP 1.1 / MAP 5.1; ISO 42001: AI risk assessment process]
      [OK ] User disclosure that AI is in use  [GOVERN 4.2; ISO 42001: Transparency & communication]
      [OK ] Data governance & provenance review  [MAP 2.2; ISO 42001: Data for AI systems]
      [OK ] Pre-deployment performance evaluation  [MEASURE 2.6; ISO 42001: Verification & validation]
      [OK ] Ongoing monitoring & drift checks  [MANAGE 4.1; ISO 42001: Operation & monitoring]
      [OK ] Access & change control for models/prompts  [GOVERN 2.2; ISO 42001: Operational planning & control]
      [OK ] Periodic re-assessment  [MANAGE 4.3; ISO 42001: Performance evaluation / review]

--- Fraud Detection Model (Risk & Payments)
    data_sensitivity=restricted (3), autonomy=autonomous (3), human_oversight=spot-check (1), user_impact=high (3), model_source=in-house (0)
    Inherent risk score: 10  ->  Tier: CRITICAL
      [OK ] AI inventory registration & named owner  [GOVERN 1.1; ISO 42001: AIMS scope & responsibilities]
      [OK ] Documented risk assessment  [MAP 1.1 / MAP 5.1; ISO 42001: AI risk assessment process]
      [GAP] User disclosure that AI is in use  [GOVERN 4.2; ISO 42001: Transparency & communication]
      [OK ] Data governance & provenance review  [MAP 2.2; ISO 42001: Data for AI systems]
      [OK ] Pre-deployment performance evaluation  [MEASURE 2.6; ISO 42001: Verification & validation]
      [OK ] Ongoing monitoring & drift checks  [MANAGE 4.1; ISO 42001: Operation & monitoring]
      [OK ] Access & change control for models/prompts  [GOVERN 2.2; ISO 42001: Operational planning & control]
      [GAP] Periodic re-assessment  [MANAGE 4.3; ISO 42001: Performance evaluation / review]
      [OK ] Bias & fairness testing  [MEASURE 2.11; ISO 42001: Fairness & bias management]
      [OK ] Human oversight & override procedure  [MANAGE 2.4; ISO 42001: Human oversight of AI]
      [OK ] AI incident response process  [MANAGE 4.2; ISO 42001: Incident management]
    >> 2 gap(s) requiring remediation

--- Meeting Notes Summarizer (IT Services)
    data_sensitivity=internal (1), autonomy=assistive (0), human_oversight=required (0), user_impact=low (0), model_source=third-party (1)
    Inherent risk score: 2  ->  Tier: LOW
      [OK ] AI inventory registration & named owner  [GOVERN 1.1; ISO 42001: AIMS scope & responsibilities]
      [OK ] Documented risk assessment  [MAP 1.1 / MAP 5.1; ISO 42001: AI risk assessment process]
      [OK ] User disclosure that AI is in use  [GOVERN 4.2; ISO 42001: Transparency & communication]

--- Marketing Content Generator (Marketing)
    data_sensitivity=public (0), autonomy=assistive (0), human_oversight=spot-check (1), user_impact=low (0), model_source=third-party (1)
    Inherent risk score: 2  ->  Tier: LOW
      [OK ] AI inventory registration & named owner  [GOVERN 1.1; ISO 42001: AIMS scope & responsibilities]
      [OK ] Documented risk assessment  [MAP 1.1 / MAP 5.1; ISO 42001: AI risk assessment process]
      [GAP] User disclosure that AI is in use  [GOVERN 4.2; ISO 42001: Transparency & communication]
    >> 1 gap(s) requiring remediation

==========================================================================
PORTFOLIO SUMMARY
==========================================================================
  Low       2 use case(s)
  Moderate  1 use case(s)
  High      1 use case(s)
  Critical  2 use case(s)
  Total control gaps: 15

Control coverage across the portfolio (required vs in place):
  AI inventory registration & named owner       6/6
  Documented risk assessment                    6/6
  User disclosure that AI is in use             2/6
  Data governance & provenance review           4/4
  Pre-deployment performance evaluation         4/4
  Ongoing monitoring & drift checks             3/4
  Periodic re-assessment                        1/4
  Bias & fairness testing                       1/3
  Human oversight & override procedure          2/3
  AI incident response process                  1/3
  Third-party model due diligence               1/2

Highest-tier gaps to remediate first:
  [Critical] HR Screening Assistant: User disclosure that AI is in use
  [Critical] HR Screening Assistant: Ongoing monitoring & drift checks
  [Critical] HR Screening Assistant: Periodic re-assessment
  [Critical] HR Screening Assistant: Bias & fairness testing
  [Critical] HR Screening Assistant: Human oversight & override procedure
  [Critical] HR Screening Assistant: AI incident response process
  [Critical] HR Screening Assistant: Third-party model due diligence
  [Critical] Fraud Detection Model: User disclosure that AI is in use
  [Critical] Fraud Detection Model: Periodic re-assessment
  [High] Customer Support Chatbot: User disclosure that AI is in use
  [High] Customer Support Chatbot: Access & change control for models/prompts
  [High] Customer Support Chatbot: Periodic re-assessment
  [High] Customer Support Chatbot: Bias & fairness testing
  [High] Customer Support Chatbot: AI incident response process
  [Low] Marketing Content Generator: User disclosure that AI is in use
```

## Reading the results

The demo portfolio tells a familiar story. The highest-risk system — the
**HR Screening Assistant** (Critical: restricted data, high user impact,
third-party model) — has the weakest posture: no bias testing on a tool
that influences employment decisions, no documented human override, and no
AI incident process. Meanwhile the portfolio-wide coverage table shows the
systemic gaps: **transparency (2/6)** and **periodic re-assessment (1/4)**
lag everywhere, which is exactly where an AI governance programme should
start.

## Design notes and limitations

- The scoring model is deliberately transparent and additive so any tier
  can be explained and challenged factor by factor. Real programmes should
  calibrate weights and thresholds to their regulatory context (e.g., EU
  AI Act prohibited/high-risk categories would override a points model for
  in-scope systems).
- Control requirements are cumulative by tier and based on the AI RMF
  subcategory structure; the ISO/IEC 42001 references are thematic mappings
  to management-system clauses/Annex A themes, not a conformity assessment.
- The tool consumes a self-reported control inventory (`controls_in_place`);
  it does not validate that controls operate effectively. Pair it with
  evidence review and testing — as with any GRC self-assessment.
- All sample organisations, systems, and data are fictional.

## License

MIT — see `LICENSE`.
