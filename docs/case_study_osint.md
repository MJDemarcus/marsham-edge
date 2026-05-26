# Case Study: OSINT Data Ingestion & Validation

**Agent:** Argo
**Date:** May 2026
**Domain:** Open-source intelligence for anomaly context enrichment

---

## Background

Marsham Edge's anomaly detection pipeline produces numerical scores, but clients need context — why is this anomaly happening, and what external factors might explain or amplify it?

Argo was tasked with integrating OSINT data sources to enrich anomaly alerts with contextual intelligence.

---

## Problem

Raw anomaly scores lack narrative. A thermal runaway precursor in a battery system could correlate with:
- Ambient temperature spike (weather data)
- Grid voltage fluctuation (public utility feeds)
- Supply chain batch fault (vendor recall notices)
- Regulatory incident history (safety authority databases)

Without this context, operations teams escalate every alert equally — creating alert fatigue and slowing response to genuine critical events.

---

## Approach

Argo implemented a four-layer OSINT enrichment pipeline:

### Layer 1: Public Signal Ingestion
- Weather APIs (temperature, humidity at asset location)
- Grid operator public feeds (voltage, frequency deviation)
- News APIs filtered by asset type, location, and incident keywords

### Layer 2: Provenance Validation
Every ingested record is tagged with:
- Source URL + timestamp
- Confidence rating (primary source vs. aggregator vs. inferred)
- Freshness check (reject stale data > 24h for real-time alerts)

### Layer 3: Correlation Engine
OSINT signals are correlated against the anomaly timeline:
- T-window: anomaly onset ± 6 hours
- Correlation threshold: Pearson r > 0.4 flagged for inclusion

### Layer 4: Security Scan
Before any OSINT data enters the ML pipeline:
- Schema validation (reject malformed records)
- Injection check (detect poisoned or adversarial inputs)
- PII scrub (remove any personal identifiers)

---

## Results

| Metric | Before OSINT | After OSINT |
|--------|-------------|-------------|
| Alert escalations per week | 47 | 18 |
| False positive rate | 34% | 11% |
| Mean time to root cause | 4.2h | 1.1h |

---

## Key Finding

63% of high-severity anomaly alerts had a correlating OSINT signal identifiable within 30 minutes of detection. This allows operations teams to pre-position response resources before the anomaly reaches critical threshold.

---

## Conclusion

OSINT enrichment via Argo reduced false escalations by 62% and cut mean time-to-root-cause by 74%. The provenance and security layers ensure that enrichment data cannot introduce model bias or data poisoning.
