# Marsham Edge — Multi-Agent Anomaly Detection & Intelligence

> Three specialised AI agents. One pipeline. No black boxes.

**Live demo:** https://liguard.streamlit.app
**Hackathon:** UCWS Singapore 2026 — Tracks: Agent · Deep Research
**Status:** Operational — self-hosted, air-gap deployable

---

## What It Does

Marsham Edge coordinates three specialised AI agents to cover the complete anomaly detection and intelligence pipeline — from raw data ingestion to an analyst-ready briefing — continuously, without a human required at each step.

Every alert is attributed to a specific trigger. Every decision is auditable. The same agent team deploys across any time-series domain without architectural change.

---

## The Agent Team

| Agent | Role | What They Do |
|-------|------|--------------|
| **Argo** | Data & Security | Ingestion, validation, provenance tracking, adversarial robustness testing, API surface monitoring |
| **Ken** | ML & Detection | Four-trigger hybrid detection engine: statistical + rate density + geometric + physics-informed ODE |
| **Deb** | Orchestration & Briefing | Task routing, inter-agent coordination, structured analyst briefings via WhatsApp/dashboard |

---

## Proven Results — Live Integration Test (22 May 2026)

| Agent | Task | Result | Key Metric |
|-------|------|--------|------------|
| Argo | Malformed record quarantine (4 injected) | 4/4 detected, 0 false quarantines | 100% precision |
| Ken | Campaign post detection — 18 planted, 32 genuine | 18/18 detected, 0/32 false positives | **F1 = 1.00** |
| Deb | 5-point analyst briefing via WhatsApp | 5/5 delivered | **3 min 7 sec** end-to-end |

---

## Detection Engine: Four Triggers, No Black Box

| Trigger | Mechanism | What It Catches |
|---------|-----------|-----------------|
| A | Statistical 95% envelope on expanding window | Gradual drift outside established normal |
| B | Rate density threshold over rolling window | Sustained acceleration phase before failure |
| C | Geometric second-derivative spike | Abrupt inflection — sudden-onset events |
| **D*** | **Physics-informed ODE model residual** | **Anomalies before B or C can see acceleration** |

*Trigger D is the key advance: it grounds alerts in first-principles physics, not statistics alone. Catches the event before it looks like an event.*

**False-alarm architecture:** Two independent triggers must fire simultaneously before any alert issues. Single noisy sensors cannot generate alerts.

**Five-state risk machine:**

| State | Risk | Condition | Action |
|-------|------|-----------|--------|
| [0/4] Stable | 0% | No triggers | Normal — baseline updates continuously |
| [1/4] Explanation Needed | 25% | 1 trigger | Log and monitor |
| **[2/4] Watching Brief** | **50%** | **2 triggers** | **First actionable alert. Prevention Simulator activates.** |
| [3/4] High Risk | 75% | 3 triggers | Urgent escalation |
| [4/4] Critical | 100% | All triggers | Immediate intervention |

---

## Academic Validation

Core architecture independently validated by **NUS / ComfortDelGro** (Project #2420-0002, supervised by Prof. Jussi Keppo, March 2025) on **35,424 real Singapore NEMS electricity market records**:

| Component | Metric | Result |
|-----------|--------|--------|
| Prophet — demand forecasting | MAPE (1-day) | **0.9%** |
| CNN-LSTM — price forecasting | MAPE | **3.28%** (vs 6.28% standalone LSTM) |
| Random Forest — spike classification | CV Accuracy | **95.24%** (std dev 0.0037) |

---

## Domains (No Architectural Change Between Any)

| Domain | Application |
|--------|-------------|
| Li-ion battery safety | Thermal anomaly detection — live MVP |
| Electricity market intelligence | Singapore NEMS demand & price forecasting |
| Occupational health | Multi-modal sensor fusion, worker exposure monitoring |
| OSINT / adversarial content | Campaign detection, inauthentic behaviour identification |
| Any time-series stream | If it generates data, the platform can monitor it |

---

## Global Scalability

The platform is domain-agnostic by design. The same three agents, the same detection engine, and the same briefing pipeline have already operated across four entirely different problem domains — with zero architectural changes. Deployment is self-hosted via Docker containers (NanoClaw v2.0.64), air-gap capable, and portable to any sovereign compute environment. No data leaves the client's infrastructure.

---

## Infrastructure

- Self-hosted via NanoClaw — no cloud AI dependency after initial calibration
- Docker containerised — portable to on-premise, sovereign cloud, or edge environments
- Air-gap deployable
- OneCLI credential vault — no secrets in agent memory or logs

---

## Team

**Muriel Demarcus** — Founder & CEO
MSc, Paris-Saclay University (Ecole Centrale Paris)
30+ years leading multi-billion-dollar infrastructure and digital transformation, Asia-Pacific
Singapore

NUS interns embedded in every project engagement — active research in ML, time-series anomaly detection, and computer vision working directly alongside Ken and Argo.

---

## Documentation

- [Architecture & Agent Pipeline](docs/architecture.md)
- [Detection Engine — Four Triggers Explained](docs/detection_engine.md)
- [Integration Test Results — 22 May 2026](docs/integration_test_22may2026.md)
- [Case Study: OSINT Campaign Detection](docs/case_study_osint.md)
- [Case Study: Occupational Health & Regulatory Compliance](docs/case_study_occupational.md)
- [Live Demo Guide](DEMO.md)

---

## Live Demo

**https://liguard.streamlit.app**

Upload any CSV with a timestamp column and a sensor-value column. The platform runs the full four-trigger state machine and Prevention Simulator on your data in real time. No login required.
