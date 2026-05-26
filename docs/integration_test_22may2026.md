# Integration Test Report — 22 May 2026

**Test conductor:** Deb (Orchestration Agent)
**Agents tested:** Argo (Data & Security), Ken (ML & Detection)
**Environment:** Production — NanoClaw self-hosted, Singapore

---

## Scope

Live end-to-end integration test of the three-agent pipeline under adversarial and real-world conditions.

---

## Test 1: Argo — Malformed Record Quarantine

**Objective:** Verify Argo correctly identifies and quarantines adversarially injected malformed records without false-quarantining genuine data.

**Setup:**
- Dataset: 200 records (OSINT feed, mixed content)
- Injected: 4 malformed records (schema violations, encoding anomalies, one adversarial injection attempt)
- Genuine: 196 clean records

**Results:**

| Metric | Result |
|--------|--------|
| Malformed records detected | 4/4 (100%) |
| False quarantines (genuine records flagged) | 0/196 |
| Precision | 100% |
| Recall | 100% |

**Finding:** Argo's multi-layer validation pipeline (schema check → encoding check → statistical outlier → adversarial pattern match) caught all injected records at the encoding-check layer. Zero false positives across 196 genuine records.

---

## Test 2: Ken — Campaign Post Detection

**Objective:** Verify Ken correctly classifies inauthentic social content (planted campaign posts) against genuine organic content.

**Setup:**
- Dataset: 50 posts
- Planted campaign posts: 18 (coordinated inauthentic behaviour pattern)
- Genuine posts: 32

**Results:**

| Metric | Result |
|--------|--------|
| Campaign posts detected | 18/18 |
| False positives (genuine flagged as campaign) | 0/32 |
| Precision | 1.00 |
| Recall | 1.00 |
| **F1 Score** | **1.00** |

**Finding:** Ken's detection engine achieved a perfect F1 score on this dataset. The physics-informed ODE trigger (Trigger D) was decisive — it identified coordinated posting rate anomalies before the statistical envelope (Trigger A) reached threshold. The two-trigger confirmation requirement produced zero false alarms.

---

## Test 3: Deb — Analyst Briefing Delivery

**Objective:** Verify Deb correctly compiles and delivers a structured analyst briefing from agent outputs.

**Setup:**
- Input: Argo quarantine report + Ken detection report
- Required output: 5-point structured briefing via WhatsApp
- Timer started: on Deb receiving both reports

**Results:**

| Metric | Result |
|--------|--------|
| Briefing points delivered | 5/5 |
| Delivery method | WhatsApp (as specified) |
| End-to-end time | **3 minutes 7 seconds** |
| Format compliance | Full — all points attributed to source agent |

**Finding:** Deb correctly synthesised outputs from two agents, attributed findings to source, flagged the one actionable recommendation (escalate to client), and delivered within the 5-minute SLA. No human intervention required at any step.

---

## Overall Summary

| Agent | Task | Result |
|-------|------|--------|
| Argo | Quarantine 4 injected malformed records | PASS — 4/4, 0 false positives |
| Ken | Classify 50 posts (18 campaign, 32 genuine) | PASS — F1 = 1.00 |
| Deb | Deliver 5-point briefing via WhatsApp | PASS — 5/5, 3m7s |

**Pipeline verdict: OPERATIONAL**
