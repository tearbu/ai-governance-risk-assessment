#!/usr/bin/env python3
"""AI governance risk assessment tool.

Assesses AI use cases against the NIST AI Risk Management Framework
(AI RMF: GOVERN / MAP / MEASURE / MANAGE), with control themes drawn from
ISO/IEC 42001 (AI management systems). Each use case is scored on data
sensitivity, autonomy, human oversight, user impact, and model sourcing to
produce an inherent risk tier (Low / Moderate / High / Critical). The tier
determines which governance controls are required; the tool compares that
requirement against the controls recorded as in place and reports the
gaps, per use case and across the portfolio.

All sample data is fictional. Run with --demo for the bundled portfolio,
or --input with your own use-case inventory in the same JSON format.

Standard library only. This tool supports — and does not replace — a
formal AI risk assessment by accountable owners.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Scoring model (points are additive; higher = more inherent risk)
# ---------------------------------------------------------------------------

SCORES = {
    "data_sensitivity": {"public": 0, "internal": 1, "confidential": 2,
                          "restricted": 3},
    "autonomy": {"assistive": 0, "semi-autonomous": 2, "autonomous": 3},
    "human_oversight": {"required": 0, "spot-check": 1, "none": 3},
    "user_impact": {"low": 0, "medium": 1, "high": 3},
    "model_source": {"in-house": 0, "third-party": 1},
}

TIER_ORDER = ["Low", "Moderate", "High", "Critical"]


def tier_for(score):
    if score <= 3:
        return "Low"
    if score <= 6:
        return "Moderate"
    if score <= 9:
        return "High"
    return "Critical"


# ---------------------------------------------------------------------------
# Control catalogue: name -> (NIST AI RMF function, ISO/IEC 42001 theme)
# ---------------------------------------------------------------------------

CONTROLS = {
    "AI inventory registration & named owner":
        ("GOVERN 1.1", "AIMS scope & responsibilities"),
    "Documented risk assessment":
        ("MAP 1.1 / MAP 5.1", "AI risk assessment process"),
    "User disclosure that AI is in use":
        ("GOVERN 4.2", "Transparency & communication"),
    "Data governance & provenance review":
        ("MAP 2.2", "Data for AI systems"),
    "Pre-deployment performance evaluation":
        ("MEASURE 2.6", "Verification & validation"),
    "Ongoing monitoring & drift checks":
        ("MANAGE 4.1", "Operation & monitoring"),
    "Access & change control for models/prompts":
        ("GOVERN 2.2", "Operational planning & control"),
    "Periodic re-assessment":
        ("MANAGE 4.3", "Performance evaluation / review"),
    "Bias & fairness testing":
        ("MEASURE 2.11", "Fairness & bias management"),
    "Human oversight & override procedure":
        ("MANAGE 2.4", "Human oversight of AI"),
    "AI incident response process":
        ("MANAGE 4.2", "Incident management"),
    "Third-party model due diligence":
        ("GOVERN 6.1", "Third-party relationships"),
}

# Controls required per tier (cumulative). Third-party due diligence is
# additionally required at High+ whenever the model is third-party.
REQUIRED_BY_TIER = {
    "Low": [
        "AI inventory registration & named owner",
        "Documented risk assessment",
        "User disclosure that AI is in use",
    ],
    "Moderate": [
        "Data governance & provenance review",
        "Pre-deployment performance evaluation",
        "Ongoing monitoring & drift checks",
        "Access & change control for models/prompts",
        "Periodic re-assessment",
    ],
    "High": [
        "Bias & fairness testing",
        "Human oversight & override procedure",
        "AI incident response process",
    ],
    "Critical": [
        # No additional standing controls; Critical adds executive
        # approval & board-level reporting expectations (see README), and
        # third-party due diligence via the conditional rule below.
    ],
}


def required_controls(use_case, tier):
    required = []
    for t in TIER_ORDER[: TIER_ORDER.index(tier) + 1]:
        required.extend(REQUIRED_BY_TIER[t])
    if (TIER_ORDER.index(tier) >= TIER_ORDER.index("High")
            and use_case["model_source"] == "third-party"
            and "Third-party model due diligence" not in required):
        required.append("Third-party model due diligence")
    return required


def score_use_case(use_case):
    breakdown = {factor: SCORES[factor][use_case[factor]]
                 for factor in SCORES}
    return sum(breakdown.values()), breakdown


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--demo", action="store_true",
                        help="assess the bundled fictional AI portfolio")
    parser.add_argument("--input", help="path to a use-cases JSON file")
    args = parser.parse_args(argv)

    if args.demo:
        path = Path(__file__).parent / "data" / "use_cases.json"
    elif args.input:
        path = Path(args.input)
    else:
        parser.error("use --demo or --input")

    use_cases = json.loads(path.read_text(encoding="utf-8"))

    print("=" * 74)
    print("AI GOVERNANCE RISK ASSESSMENT — NIST AI RMF / ISO-IEC 42001")
    print("=" * 74)
    print(f"Use cases assessed: {len(use_cases)}")
    print()

    tier_counts = Counter()
    total_gaps = 0
    control_demand = Counter()   # control -> # use cases requiring it
    control_met = Counter()      # control -> # of those with it in place
    critical_gaps = []

    for uc in use_cases:
        score, breakdown = score_use_case(uc)
        tier = tier_for(score)
        tier_counts[tier] += 1
        required = required_controls(uc, tier)
        in_place = set(uc.get("controls_in_place", []))
        gaps = [c for c in required if c not in in_place]

        print(f"--- {uc['name']} ({uc['owner']})")
        detail = ", ".join(f"{k}={v} ({breakdown[k]})" for k, v in
                           ((f, uc[f]) for f in SCORES))
        print(f"    {detail}")
        print(f"    Inherent risk score: {score}  ->  Tier: {tier.upper()}")
        for control in required:
            mark = "OK " if control in in_place else "GAP"
            rmf, iso = CONTROLS[control]
            print(f"      [{mark}] {control}  [{rmf}; ISO 42001: {iso}]")
            control_demand[control] += 1
            if control in in_place:
                control_met[control] += 1
        if gaps:
            total_gaps += len(gaps)
            for g in gaps:
                critical_gaps.append((tier, uc["name"], g))
            print(f"    >> {len(gaps)} gap(s) requiring remediation")
        print()

    print("=" * 74)
    print("PORTFOLIO SUMMARY")
    print("=" * 74)
    for tier in TIER_ORDER:
        print(f"  {tier:<9} {tier_counts.get(tier, 0)} use case(s)")
    print(f"  Total control gaps: {total_gaps}")
    print()
    print("Control coverage across the portfolio (required vs in place):")
    for control, demand in control_demand.most_common():
        print(f"  {control:<45} {control_met[control]}/{demand}")
    print()
    print("Highest-tier gaps to remediate first:")
    for tier, name, gap in sorted(
            critical_gaps, key=lambda x: -TIER_ORDER.index(x[0])):
        print(f"  [{tier}] {name}: {gap}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
