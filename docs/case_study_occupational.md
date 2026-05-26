# Case Study: Occupational Health Anomaly Detection

**Agent:** Ken (ML) + Argo (Data)
**Date:** May 2026
**Domain:** Occupational health & hygiene — construction site safety

---

## Background

Construction sites expose workers to multiple simultaneous hazards: heat, noise, dust, chemical exposure, and cumulative fatigue. Traditional compliance monitoring relies on periodic manual inspections — which miss transient events that cause the majority of occupational health incidents.

Marsham Edge was engaged to develop a continuous, AI-driven monitoring system for a major infrastructure project.

---

## Data Sources

| Signal | Sensor | Frequency |
|--------|--------|-----------|
| Ambient temperature | Distributed IoT nodes | 1 reading/min |
| Relative humidity | Distributed IoT nodes | 1 reading/min |
| PM2.5 / PM10 particulates | Optical particle counters | 6 readings/min |
| Noise exposure (LAeq) | Sound level meters | Continuous |
| UV index | Site weather station | 1 reading/min |
| Worker location | BLE beacons | 1 reading/10s |

---

## Model Design

### CNN-LSTM for Multivariate Time Series

Ken trained a hybrid CNN-LSTM model on 14 months of historical site data (3 sites, 2 countries):

- **Input**: 60-minute rolling window, 6 channels
- **CNN**: Extract spatial patterns across sensor channels
- **LSTM**: Capture temporal drift and accumulation effects
- **Output**: Heat stress risk score (0–1), noise overexposure flag, dust alert flag

### Thresholds

Calibrated against:
- ISO 7243 (heat stress)
- IEC 61672 (noise measurement)
- WHO PM2.5 air quality guidelines

---

## Argo's Data Validation Layer

Before each inference run, Argo validates:

1. **Sensor dropout detection**: Flag channels with > 5% missing readings in the window
2. **Drift detection**: Statistical test for sensor calibration drift
3. **Cross-sensor consistency**: Temperature/humidity physical plausibility check
4. **Location join**: Confirm worker presence in the monitored zone before issuing worker-specific alerts

Invalid or degraded data is quarantined — the model never runs on uncertified inputs.

---

## Deployment Architecture

```
Site Sensors
    |
    v
Edge Gateway (on-site)
    |  (encrypted MQTT)
    v
Argo Ingestion Layer
    |
    v
Ken CNN-LSTM Inference (Modal)
    |
    v
Alert Engine
    |
    +----> Site Safety Officer (SMS/app)
    +----> Operations Dashboard
    +----> Deb (Analyst Briefing)
```

---

## Results (Pilot — 90 days, 1 site, 340 workers)

| Metric | Value |
|--------|-------|
| Heat stress events detected | 23 |
| Events confirmed by safety officer | 21 (91%) |
| Events missed by traditional inspection | 17 of 21 (81%) |
| Noise overexposure flags issued | 8 |
| Average alert lead time before threshold breach | 14 minutes |
| Zero injuries attributable to missed alerts | Confirmed |

---

## Key Insight

The 14-minute average lead time before a threshold breach was the critical finding. Traditional inspection-based compliance cannot achieve this. The CNN-LSTM model detected accumulating risk from the rate of change of combined signals — not from any single sensor crossing a threshold.

---

## Conclusion

The Marsham Edge OccuSense pilot demonstrated that continuous multivariate anomaly detection significantly outperforms periodic inspection for occupational health monitoring. The Argo validation layer was essential: without sensor-quality certification, 12% of inference runs would have operated on degraded data, producing unreliable scores.

The system is now being extended to cover Li-ion battery storage systems on the same site.
