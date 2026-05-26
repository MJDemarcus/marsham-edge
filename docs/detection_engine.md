# Detection Engine — Four Triggers, No Black Box

## Overview

The Marsham Edge detection engine uses four independent trigger mechanisms operating simultaneously on every incoming time-series window. An alert issues only when two or more triggers fire simultaneously — eliminating single-sensor noise as a source of false alarms.

---

## The Four Triggers

### Trigger A — Statistical Envelope

**Mechanism:** 95% confidence envelope calculated on an expanding window of historical readings.

**What it catches:** Gradual drift. A signal that slowly moves outside the established normal range — the kind of degradation that is invisible to threshold-based systems because it never crosses any single line, but represents a clear departure from baseline.

**Limitation:** By design, Trigger A cannot catch sudden events — the expanding window takes time to establish a stable envelope. For sudden events, see Triggers C and D.

---

### Trigger B — Rate Density Threshold

**Mechanism:** Counts the number of threshold-crossing events within a rolling time window. If the density of crossings exceeds a calibrated rate, Trigger B fires.

**What it catches:** Sustained acceleration phases — the period before a failure where a system is not yet in the critical zone but is crossing minor thresholds with increasing frequency. This is the signature of a system under stress that has not yet broken.

**Physical interpretation:** In thermal systems, this corresponds to the exothermic runaway phase before temperature becomes obviously anomalous. In mechanical systems, it corresponds to micro-fracture propagation.

---

### Trigger C — Geometric Second-Derivative Spike

**Mechanism:** Computes the second derivative of the signal across the window. If the second derivative exceeds a threshold — i.e., if the rate of change is itself changing rapidly — Trigger C fires.

**What it catches:** Abrupt inflection points. Sudden-onset events: a valve failure, an equipment impact, a short circuit. The geometric second derivative detects the moment a signal changes character, not just magnitude.

---

### Trigger D — Physics-Informed ODE Residual (Key Advance)

**Mechanism:** A physics-informed ordinary differential equation model generates a prediction for what the signal *should* be doing based on first-principles physical behaviour of the monitored system. The residual — the gap between predicted and observed — is monitored continuously. If the residual exceeds calibration bounds, Trigger D fires.

**What it catches:** Anomalies that precede detectable statistical or geometric change. Because the ODE model encodes physical law, not historical statistics, it can detect physically implausible states before those states generate measurable acceleration.

**Why this matters:** Trigger D catches the event before it looks like an event. This is the trigger that enables the Prevention Simulator — because if you can detect anomaly before acceleration begins, you have time to intervene before any of the other three triggers have fired.

**Example:** In a Li-ion battery cell undergoing early-stage thermal runaway, internal resistance changes are physically predictable from temperature and current. An ODE model of the electrochemical system can detect implausible internal-resistance trajectories minutes before cell temperature becomes statistically anomalous.

---

## False-Alarm Architecture

**Two-trigger confirmation required.**

No single trigger, however confident, generates an alert. Two independent triggers must fire simultaneously within the same time window. This means:

- A noisy sensor that trips Trigger A sporadically cannot generate alerts alone
- A single abrupt reading that trips Trigger C without Trigger D confirmation is logged but not escalated
- The system tolerates single-channel sensor degradation without alarm fatigue

---

## Five-State Risk Machine

| State | Trigger Count | Risk Level | Action |
|-------|--------------|------------|--------|
| Stable | 0 | 0% | Normal operation. Baseline updates continuously. |
| Explanation Needed | 1 | 25% | Logged. Monitored. No escalation. |
| **Watching Brief** | **2** | **50%** | **First actionable alert. Prevention Simulator activates.** |
| High Risk | 3 | 75% | Urgent escalation to operations team. |
| Critical | 4 | 100% | Immediate intervention required. |

**The Watching Brief state is the most operationally significant.** It is the first state at which intervention can prevent escalation to High Risk or Critical. The Prevention Simulator runs automatically at this state, modelling what corrective actions would return the system to Stable.

---

## Prevention Simulator

When the system reaches Watching Brief, the Prevention Simulator:

1. Takes the current four-trigger state as input
2. Runs forward simulation of the physical model under three intervention scenarios: (a) no action, (b) standard mitigation, (c) aggressive mitigation
3. Returns a probability distribution for the risk state at T+30min, T+60min, T+120min for each scenario
4. Delivers the simulation results to Deb for inclusion in the analyst briefing

The client receives: current state, trigger attribution, intervention options with modelled outcomes, and a recommendation — all within the briefing delivered by Deb.
