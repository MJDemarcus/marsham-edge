# System Architecture — Three-Agent Pipeline

## Overview

Marsham Edge is a three-agent AI system. The agents are not assistants — they are specialists with defined ownership of distinct pipeline stages. No agent duplicates another's function. The pipeline is: **Argo → Ken → Deb → Analyst**.

---

## Agent Roles

### Argo — Data & Security Agent

**Owns:** Everything that touches raw data before it enters the detection engine.

**Responsibilities:**
- Data ingestion from sensor streams, APIs, OSINT sources, and client uploads
- Schema validation — reject records that don't conform to expected structure
- Provenance tracking — every record tagged with source, timestamp, and confidence rating
- Adversarial robustness testing — detect injection attempts, poisoned records, and encoding anomalies
- API surface monitoring — continuously check that upstream data sources are returning valid, non-degraded feeds
- Quarantine and audit logging — every rejected record logged with rejection reason

**Output:** A certified, clean dataset with provenance metadata attached. Ken never receives data that Argo has not signed off.

**Rule:** Argo does not run detection. If Argo flags something suspicious, it quarantines and reports to Deb — it does not attempt to classify or score.

---

### Ken — ML & Detection Agent

**Owns:** Everything between clean data and anomaly scores.

**Responsibilities:**
- Feature engineering from certified Argo output
- Running the four-trigger detection engine (A: statistical, B: rate density, C: geometric, D: physics ODE)
- Operating the five-state risk machine
- Running the Prevention Simulator when the Watching Brief state is reached
- Hyperparameter tuning via Modal async GPU jobs (A10 GPU, up to 3-hour jobs)
- Continuous model weight updates as new data arrives

**Infrastructure:** Modal serverless GPU (T4 for inference, A10 for tuning). Python 3.11, TensorFlow/Keras, XGBoost, scikit-learn.

**Output:** Anomaly score, trigger attribution (which of A/B/C/D fired), risk state, Prevention Simulator results, confidence intervals.

**Rule:** Ken does not communicate directly with clients or with Argo. Ken sends outputs to Deb.

---

### Deb — Orchestration & Briefing Agent

**Owns:** Task routing, inter-agent coordination, and all client-facing communication.

**Responsibilities:**
- Receiving requests from clients and internal systems
- Delegating data tasks to Argo and detection tasks to Ken
- Routing certified data from Argo to Ken
- Compiling Ken's detection outputs into structured analyst briefings
- Delivering briefings via WhatsApp, email, or dashboard
- Managing calendar, scheduling, and administrative tasks

**Output:** Analyst-ready briefing: current state, trigger attribution, intervention options with modelled outcomes, recommended action.

**Rule:** Deb is the only agent that communicates with clients. Argo and Ken do not talk to each other or to clients directly. All routing passes through Deb.

---

## Pipeline Flow

```
Client Request
      |
      v
   [Deb]
   Receives & routes
      |
      v
   [Argo]
   Ingests, validates, certifies
      |
  Certified dataset
      |
      v
   [Ken]
   Detection engine + risk machine
      |
  Anomaly score + trigger attribution
      |
      v
   [Deb]
   Compiles briefing
      |
      v
   Analyst / Client
   Structured briefing with recommendations
```

---

## Communication Protocol

- **Deb → Argo:** Task assignment (what to ingest, from where, by when)
- **Argo → Deb:** Certified dataset + quarantine report
- **Deb → Ken:** Certified dataset + detection task specification
- **Ken → Deb:** Detection results + Prevention Simulator output
- **Deb → Client:** Structured briefing

Argo and Ken have no direct communication channel. This is intentional — it ensures that data provenance and detection outputs are always routed through an orchestration layer that maintains the full audit trail.

---

## Deployment

| Layer | Technology |
|-------|------------|
| Agent runtime | NanoClaw v2.0.64 (self-hosted Docker) |
| ML inference | Modal serverless GPU (Python 3.11) |
| Frontend | Lovable (React/TypeScript) |
| Backend API | Supabase Edge Functions |
| Credential vault | OneCLI (no secrets in agent memory or logs) |
| Air-gap capability | Yes — all Modal endpoints callable from isolated networks |

---

## Security Architecture

- No raw data stored in agent memory after task completion
- All credentials managed by OneCLI credential vault — agents never see plaintext secrets
- Argo maintains audit log of every ingestion event, quarantine decision, and provenance tag
- Air-gap deployable: the full pipeline can operate in a sovereign compute environment with no outbound internet dependency post-calibration
