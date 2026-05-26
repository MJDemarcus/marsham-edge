# Detection Engine — Technical Reference

## Model Architecture

### Hybrid CNN-LSTM

The primary detection model combines:

- **CNN layers**: Extract local patterns and feature representations from time-series windows
- **LSTM layers**: Capture temporal dependencies and long-range correlations
- **Output**: Anomaly probability score (0–1) with confidence interval

```python
model = Sequential([
    Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(window, features)),
    MaxPooling1D(pool_size=2),
    LSTM(units=70, return_sequences=True, dropout=0.1),
    LSTM(units=70, dropout=0.1),
    Dense(1, activation='sigmoid')
])
```

### Ensemble

For robustness, the CNN-LSTM is run alongside:

- **XGBoost**: Gradient boosting on lagged features (n_lags=60)
- **Random Forest**: 500-tree ensemble, depth-limited to prevent overfitting

Ensemble vote weights: CNN-LSTM 60%, XGBoost 25%, RF 15%

## Training Pipeline

1. **Ingestion**: Argo validates and certifies the dataset
2. **Feature engineering**: 60-period lagged features, rolling statistics
3. **Normalisation**: Z-score per sensor channel
4. **Train/val split**: 80/20 time-series aware split
5. **Hyperparameter tuning**: Grid search via Modal async jobs (A10 GPU)
6. **Model storage**: Weights stored in Modal's persistent volume

## Anomaly Scoring

An anomaly is flagged when:

```
score > threshold AND confidence_interval_lower > threshold * 0.85
```

Default threshold: `0.65` (configurable per deployment)

## Supported Signal Types

| Domain | Signal | Sampling Rate |
|--------|--------|--------------|
| Li-ion thermal | Cell temperature, voltage delta, current | 1 Hz |
| Li-ion thermal | Gas sensor (CO, H2) | 0.1 Hz |
| Occupational | Ambient temperature, humidity | 0.017 Hz |
| Occupational | Noise exposure (dB) | 1 Hz |
| Occupational | Particulate matter (PM2.5, PM10) | 0.1 Hz |

## Performance Benchmarks

| Model | Precision | Recall | F1 | Latency |
|-------|-----------|--------|-----|---------|
| CNN-LSTM | 0.91 | 0.88 | 0.89 | 0.8s |
| XGBoost | 0.87 | 0.84 | 0.85 | 0.1s |
| Random Forest | 0.85 | 0.81 | 0.83 | 0.2s |
| Ensemble | 0.93 | 0.90 | 0.91 | 1.1s |

Benchmarked on held-out industrial test sets. GPU inference via Modal T4.
