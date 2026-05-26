# Integration Test Report — 22 May 2026

**Test conductor:** Argo (Data Agent)
**Reviewed by:** Ken (ML Agent), Deb (Orchestration Agent)
**Environment:** Production (Modal workspace: teakfinwisesupport)

---

## Scope

End-to-end integration test of the three-agent pipeline:
1. Data ingestion and validation (Argo)
2. Model inference (Ken via Modal)
3. Result delivery and briefing (Deb)

---

## Test Cases

### TC-01: LSTM Weight Update

| Parameter | Value |
|-----------|-------|
| Endpoint | `update-ls-f4582d.modal.run` |
| Method | POST |
| Payload | 90-day close price series (BHP.AX) |
| Expected | HTTP 200, weights updated |
| Result | **PASS** |
| Latency | 1.2s |

### TC-02: XGBoost Weight Update

| Parameter | Value |
|-----------|-------|
| Endpoint | `update-xg-c049a6.modal.run` |
| Method | POST |
| Payload | 90-day close price series (BHP.AX) |
| Expected | HTTP 200, weights updated |
| Result | **PASS** |
| Latency | 0.9s |

### TC-03: Random Forest Weight Update

| Parameter | Value |
|-----------|-------|
| Endpoint | `update-rf-445390.modal.run` |
| Method | POST |
| Payload | 90-day close price series (BHP.AX) |
| Expected | HTTP 200, weights updated |
| Result | **PASS** |
| Latency | 0.8s |

### TC-04: LSTM Prediction

| Parameter | Value |
|-----------|-------|
| Endpoint | `predict-lstm.modal.run` |
| Method | POST |
| Payload | 30-day close price series |
| Expected | HTTP 200, prediction with CI |
| Result | **PASS** |
| Latency | 1.4s |

### TC-05: Hyperparameter Tuning (Async)

| Parameter | Value |
|-----------|-------|
| Endpoint | `start-tuning.modal.run` |
| Method | POST |
| Model type | lstm |
| Expected | HTTP 200, run_id returned |
| Result | **PASS** |
| Latency | 0.3s (fire-and-forget) |

### TC-06: GPU Allocation Audit

**Finding:** All three weight-update functions had `gpu="T4"` specified but were using `debian_slim` image with no CUDA drivers. GPU slots were reserved but unutilised — models ran on CPU silently.

**Resolution:** Removed `gpu="T4"` from all three decorators. Redeployed. GPU cost eliminated. No functional change to outputs (confirmed by output comparison).

**Commit:** `88e4744` (kevinkyhalim/modal_me)

---

## Summary

| Test | Result |
|------|--------|
| TC-01 LSTM update | PASS |
| TC-02 XGBoost update | PASS |
| TC-03 RF update | PASS |
| TC-04 LSTM predict | PASS |
| TC-05 Async tuning | PASS |
| TC-06 GPU audit | FIXED |

**Overall: 5/5 PASS, 1 issue identified and resolved**
