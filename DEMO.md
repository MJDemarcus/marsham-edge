# Live Demo

**Go to https://liguard.streamlit.app**

Upload any CSV with a timestamp column and a sensor-value column. No login required.

The platform runs the full four-trigger state machine and Prevention Simulator on your data in real time.

---

## What You'll See

1. Upload your CSV
2. The platform identifies the timestamp and value columns automatically
3. The four-trigger detection engine runs across your full dataset
4. The five-state risk machine outputs a timeline: Stable → Explanation Needed → Watching Brief → High Risk → Critical
5. The Prevention Simulator shows what intervention at the Watching Brief state would have prevented

No account. No configuration. No data stored after the session ends.

---

## Sample Data

If you don't have your own data, try any time-series CSV — electricity consumption, temperature logs, equipment sensor exports. The engine is domain-agnostic.

---

## API Endpoints

All Modal inference endpoints are live:

| Function | URL |
|----------|-----|
| LSTM weight update | `https://teakfinwisesupport--incremental-weight-updater-update-ls-f4582d.modal.run` |
| XGBoost weight update | `https://teakfinwisesupport--incremental-weight-updater-update-xg-c049a6.modal.run` |
| RF weight update | `https://teakfinwisesupport--incremental-weight-updater-update-rf-445390.modal.run` |
| LSTM prediction | `https://teakfinwisesupport--stock-prediction-predict-lstm.modal.run` |
| Tree-based prediction | `https://teakfinwisesupport--stock-prediction-predict-tree-based.modal.run` |
| Start tuning | `https://teakfinwisesupport--stock-hyperparameter-tuning-start-tuning.modal.run` |
| Check status | `https://teakfinwisesupport--stock-hyperparameter-tuning-check-status.modal.run` |
| Get result | `https://teakfinwisesupport--stock-hyperparameter-tuning-get-result.modal.run` |
