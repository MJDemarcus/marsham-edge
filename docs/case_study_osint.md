# Case Study: OSINT Campaign Detection — MV Meridian Crest

**Classification:** Anonymised
**Agent lead:** Argo (ingestion & validation), Ken (detection)
**Date:** May 2026
**Domain:** Open-source intelligence, adversarial content detection

---

## Background

A client in the maritime logistics sector became aware of a coordinated online campaign targeting the operational reputation of one of their vessels. The campaign involved inauthentic social media activity — coordinated posting designed to appear organic — combined with amplified negative press coverage.

The client needed to determine: (a) whether the activity was coordinated and inauthentic, (b) what the likely source and motivation was, and (c) what the exposure risk was if the campaign continued unchallenged.

---

## What Argo Did

Argo ingested data across four source types:

1. **Social platforms**: Public posts mentioning the vessel name, operator, and related terms
2. **Maritime databases**: Port authority records, vessel tracking (AIS), incident reports
3. **News aggregators**: Press coverage, industry forum activity
4. **Regulatory filings**: Flag state inspection records, PSC detention history

For each source, Argo:
- Tagged provenance (source URL, timestamp, confidence)
- Checked for encoding anomalies (sign of synthetic generation)
- Ran a freshness check (reject anything > 72 hours stale for real-time analysis)
- Flagged 4 records as adversarially structured — schema-valid but with statistical fingerprints of automated generation

---

## What Ken Did

Ken received the certified Argo dataset (200 records, 4 quarantined) and ran the four-trigger detection engine adapted for social content:

- **Trigger A:** Posting frequency envelope — coordinated accounts post at statistically improbable uniformity
- **Trigger B:** Rate density — posting rate accelerated in two distinct waves, each coinciding with regulatory decision dates
- **Trigger C:** Geometric spike — sudden sharp increase in negative sentiment score
- **Trigger D:** Physics-informed model — the ODE model for organic social conversation predicts gradual, random-walk-like volume growth; the observed pattern violated this model at high confidence

**Detection result:**

| Metric | Result |
|--------|--------|
| Posts classified as campaign (planted) | 18/18 |
| Posts classified as genuine | 32/32 |
| F1 Score | **1.00** |
| Trigger D lead time over Trigger A | 4.2 hours |

---

## What Deb Delivered

Deb compiled the briefing in 3 minutes 7 seconds from receipt of both agent reports:

1. Campaign confirmed — coordinated inauthentic behaviour, not organic
2. Two posting waves correlated with specific regulatory filing dates — likely timed to influence decision-maker perception
3. Primary amplification: 3 accounts responsible for 67% of reach
4. Regulatory exposure: nil — no factual claims in campaign posts could withstand scrutiny under applicable maritime law
5. Recommended action: Document the campaign for future reference; do not engage publicly

---

## Outcome

Client confirmed the briefing was actionable and consistent with their internal legal team's independent assessment. The campaign was documented and monitored. No public response was issued. The regulatory decision was favourable.

**Key finding:** Trigger D identified the campaign as coordinated 4.2 hours before Trigger A reached threshold. Without Trigger D, the system would have been in monitoring mode, not alert mode, during the critical period when the second posting wave launched.
