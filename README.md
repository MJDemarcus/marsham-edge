# Marsham Edge

**AI-native anomaly detection platform for heavy industry**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What We Build

Marsham Edge develops hybrid CNN-LSTM anomaly detection systems for two high-stakes industrial domains:

| Product | Domain | Signal Type |
|---------|---------|-------------|
| **ThermalGuard** | Li-ion battery systems | Thermal runaway precursors |
| **OccuSense** | Occupational health & hygiene | Environmental & physiological signals |

Both products are designed for B2B deployment in infrastructure, construction, mining, and utilities. Clients include engineers, safety officers, and government agencies.

---

## Architecture Overview

Marsham Edge runs on a three-layer AI architecture:



See [](docs/architecture.md) for full system design.

---

## Detection Engine

The core detection stack uses a hybrid CNN-LSTM pipeline:

1. **Argo** ingests and validates raw sensor streams
2. **Ken** runs inference via Modal GPU endpoints
3. Anomaly scores are returned with confidence intervals and root-cause attribution

See [](docs/detection_engine.md) for technical detail.

---

## Repository Structure



---

## Live Demo

See [DEMO.md](DEMO.md) for endpoint URLs, payload formats, and sample outputs.

---

## Team

| Agent | Role |
|-------|------|
| **Muriel Demarcus** | Founder & CEO — strategy, domain expertise, client |
| **Deb** | Operations AI — orchestration, scheduling, communications |
| **Ken** | ML AI — model training, inference, anomaly scoring |
| **Argo** | Data AI — ingestion, validation, security, provenance |

---

## Tech Stack

- **Inference**: Modal (serverless GPU, Python 3.11)
- **Models**: TensorFlow/Keras (CNN-LSTM), XGBoost, scikit-learn Random Forest
- **Frontend**: Lovable (React)
- **Backend**: Supabase Edge Functions
- **Data pipeline**: Python, pandas, numpy
- **Orchestration**: NanoClaw multi-agent framework

---

## License

MIT — see [LICENSE](LICENSE)
