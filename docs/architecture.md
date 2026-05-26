# System Architecture — Marsham Edge

## Overview

Marsham Edge is a three-agent AI system built for continuous anomaly detection in heavy industry environments. The system is designed to operate without human intervention at each processing step.

```
User / Client
      |
      v
  [Deb] — Orchestration Agent
      |
      +----------+----------+
      |                     |
  [Argo]               [Ken]
  Data Agent          ML Agent
  Validation          CNN-LSTM
  Security            Inference
  Provenance          Scoring
```

## Agent Roles

### Deb — Operations & Orchestration
- Receives requests from clients and internal triggers
- Coordinates task delegation between Argo and Ken
- Manages calendar, communications, and reporting
- Delivers analyst briefings to stakeholders

### Ken — Machine Learning
- Runs hybrid CNN-LSTM anomaly detection models
- Handles hyperparameter tuning via async Modal jobs
- Outputs anomaly scores with confidence intervals
- Supports: LSTM, XGBoost, Random Forest models
- Infrastructure: Modal serverless GPU (T4/A10)

### Argo — Data Security & Validation
- Ingests raw data from sensors, APIs, OSINT sources
- Validates schema, provenance, and completeness
- Detects data poisoning and injection attempts
- Returns clean, certified datasets to Ken

## Deployment

| Layer | Technology |
|-------|------------|
| Inference | Modal (Python 3.11, serverless GPU) |
| Frontend | Lovable (React/TypeScript) |
| Backend API | Supabase Edge Functions |
| Orchestration | NanoClaw multi-agent framework |
| Models | TensorFlow/Keras, XGBoost, scikit-learn |

## Data Flow

```
Raw Signal
    |
    v
[Argo: Ingest + Validate]
    |
    v
[Ken: Feature Engineering]
    |
    v
[Ken: CNN-LSTM Inference]
    |
    v
[Ken: Anomaly Score + CI]
    |
    v
[Deb: Analyst Briefing]
    |
    v
Client / Alert System
```

## Security Model

- All data validated for provenance before model ingestion
- No raw PII stored — signals are anonymised at source
- Air-gap deployable: all Modal endpoints callable from isolated networks
- Audit log maintained by Argo for every ingestion event
