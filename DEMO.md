# Live Demo — Marsham Edge

## Live Application

**Streamlit App:** https://liguard.streamlit.app

**Lovable Frontend:** https://analyze-insight-express.lovable.app

---

## Modal API Endpoints

All endpoints are live and publicly reachable:

### Weight Update Endpoints

| Function | URL |
|----------|-----|
| LSTM weight update | `https://teakfinwisesupport--incremental-weight-updater-update-ls-f4582d.modal.run` |
| XGBoost weight update | `https://teakfinwisesupport--incremental-weight-updater-update-xg-c049a6.modal.run` |
| Random Forest weight update | `https://teakfinwisesupport--incremental-weight-updater-update-rf-445390.modal.run` |

### Prediction Endpoints

| Function | URL |
|----------|-----|
| LSTM prediction | `https://teakfinwisesupport--stock-prediction-predict-lstm.modal.run` |
| Tree-based prediction | `https://teakfinwisesupport--stock-prediction-predict-tree-based.modal.run` |

### Hyperparameter Tuning

| Function | URL |
|----------|-----|
| Start tuning job | `https://teakfinwisesupport--stock-hyperparameter-tuning-start-tuning.modal.run` |
| Check job status | `https://teakfinwisesupport--stock-hyperparameter-tuning-check-status.modal.run` |
| Get tuning results | `https://teakfinwisesupport--stock-hyperparameter-tuning-get-result.modal.run` |

---

## Sample Payload

### LSTM Prediction (POST)

```json
{
  "ticker": "BHP",
  "stock_data": [
    {"date": "2026-01-01", "close": 42.50},
    {"date": "2026-01-02", "close": 43.10}
  ]
}
```

### Response

```json
{
  "ticker": "BHP",
  "prediction": 43.85,
  "confidence_interval": [42.90, 44.80],
  "anomaly_score": 0.12,
  "model": "lstm"
}
```

---

## Screenshots

See `demo/screenshots/` for UI captures.
