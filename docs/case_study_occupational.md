# Case Study: Occupational Health & Regulatory Compliance — Mining Project

**Classification:** Anonymised (client: major mining operation, NSW, Australia)
**Agent lead:** Argo (data validation), Ken (detection), Deb (regulatory briefing)
**Date:** May 2026
**Domain:** Occupational health — silica dust exposure, mining

---

## Background

A mining client faced a regulatory compliance challenge following the tightening of silica dust exposure limits under revised NSW mining regulations. The new limits (0.025 mg/m3 TWA) were significantly lower than the previous standard, and the client's existing monitoring infrastructure — periodic manual sampling, quarterly audits — was not sensitive enough to demonstrate continuous compliance.

The client needed continuous, real-time monitoring with automatic alerting and regulatory-grade audit trails.

---

## Regulatory Context

Key regulatory provisions (NSW, 2025 revision):

- Respirable crystalline silica (RCS) TWA: 0.025 mg/m3 (reduced from 0.05 mg/m3)
- Mandatory continuous monitoring for enclosed drilling, cutting, and processing operations
- Audit trail requirements: timestamped readings, sensor calibration records, exposure event logs
- Worker exposure record: individual dose tracking for roles with >50% exposure probability

---

## What Argo Did

Argo ingested sensor streams from 14 monitoring nodes across three work zones:

- PM1.0, PM2.5, PM4.0, PM10 optical particle counters (1 reading/10 sec)
- Silica-specific XRF sensor at 3 high-risk points (1 reading/min)
- Worker location from BLE beacon network (1 reading/10 sec)
- Shift roster from site management system (API pull, hourly refresh)

**Validation tasks:**
- Sensor drift detection: statistical test applied to each sensor every 4 hours; 2 sensors flagged for calibration over the test period
- Cross-sensor consistency: PM2.5/PM4.0 ratio check (physically bounded — violations indicate sensor fault)
- Worker-location join: Ken receives individual exposure calculations only for workers confirmed present in the monitored zone during the sampling period
- Calibration record logging: every sensor reading tagged with calibration status at time of reading

**Data quality outcome:** 98.7% of readings certified clean over 30-day pilot. 1.3% quarantined (sensor calibration drift, 2 nodes). No data gaps > 8 minutes.

---

## What Ken Did

Ken ran the four-trigger detection engine on the combined dust + location dataset:

- **Trigger A:** Individual worker 8-hour TWA approaching 80% of 0.025 mg/m3 limit
- **Trigger B:** Zone-level PM2.5 rate density — sustained elevated readings in enclosed spaces
- **Trigger C:** Abrupt PM spike — explosive or mechanical event generating instantaneous high exposure
- **Trigger D:** Physics-informed ODE for dust dispersion — flags anomalies in how dust clears after source cessation (indicates ventilation failure before PM levels breach threshold)

**Key finding — Trigger D ventilation detection:**

On Day 14 of the pilot, Trigger D fired at 07:23 for Zone 2 (enclosed cutting bay). The ODE model for dust dispersion predicted that PM levels should have cleared within 8 minutes of the previous cutting cycle ending. By 07:23 they had not. Trigger A did not fire until 07:51 (28-minute lead time). Trigger B did not fire until 08:04 (41-minute lead time).

The ventilation system was found to have a partially blocked exhaust filter. Without Trigger D, workers would have been exposed for 41+ additional minutes before the first standard alert.

**Individual exposure events detected:**

| Metric | Value |
|--------|-------|
| Workers approaching TWA threshold (>80%) | 7 |
| Workers breaching TWA threshold | 1 |
| Exposure events detected by Trigger D before other triggers | 4 of 8 (50%) |
| Mean Trigger D lead time over next earliest trigger | 31 minutes |

---

## What Deb Delivered

Deb compiled three types of output over the 30-day pilot:

**1. Real-time alerts (Watching Brief → High Risk transitions):**
- 8 alerts delivered to site safety officer via WhatsApp
- Average delivery time from Ken detection to Deb delivery: 47 seconds
- Each alert included: zone, trigger attribution, affected workers, recommended immediate action

**2. Daily compliance summary:**
- Sent to client compliance team each morning at 06:00
- Included: previous day exposure stats, sensor status, calibration flags, top 3 workers by exposure dose

**3. Regulatory incident report (Day 14 ventilation event):**
- Full report delivered within 2 hours of event resolution
- Included: timeline, root cause (Trigger D ODE residual), exposure duration by worker, corrective action taken, regulatory notification recommendation

---

## Outcome

Client submitted the Trigger D ventilation detection finding to their regulator as evidence of proactive monitoring capability. The regulator acknowledged this as exceeding the continuous monitoring standard.

The 1 worker who breached the TWA threshold (Day 14) was removed from the zone at the High Risk alert. Exposure duration above threshold: 6 minutes. Under the previous quarterly audit regime, this breach would not have been detected or documented.

**Regulatory outcome:** Client received written confirmation of compliance with the revised standard. No enforcement action.

**Key finding:** The physics-informed ODE trigger (Trigger D) was decisive in 50% of exposure events. A system running only statistical and geometric triggers would have missed the ventilation fault until dust levels were already visibly elevated.
