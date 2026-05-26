"""
Marsham Edge — Four-Trigger Detection Engine

Implements the four-trigger anomaly detection state machine:
    A: Statistical 95% envelope (gradual drift)
    B: Rate density threshold (acceleration phase)
    C: Geometric second-derivative spike (abrupt onset)
    D: Physics-informed ODE residual (pre-acceleration anomaly)

Two triggers must fire simultaneously for an alert to issue.
Single noisy sensors cannot generate alerts.

Five-state risk machine output:
    0/4 → Stable
    1/4 → Explanation Needed
    2/4 → Watching Brief (first actionable alert)
    3/4 → High Risk
    4/4 → Critical
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional
from scipy.integrate import odeint


RISK_STATES = {
    0: ("Stable", 0.0),
    1: ("Explanation Needed", 0.25),
    2: ("Watching Brief", 0.50),
    3: ("High Risk", 0.75),
    4: ("Critical", 1.00),
}


@dataclass
class TriggerResult:
    trigger_id: str
    fired: bool
    value: float
    threshold: float
    description: str


@dataclass
class DetectionResult:
    triggers: List[TriggerResult]
    trigger_count: int
    risk_state: str
    risk_score: float
    alert: bool
    trigger_ids_fired: List[str] = field(default_factory=list)
    prevention_simulator_activated: bool = False


class FourTriggerEngine:
    """
    Four-trigger detection engine for time-series anomaly detection.

    Parameters
    ----------
    envelope_pct : float
        Percentile for Trigger A envelope (default: 95)
    rate_window : int
        Window size in samples for Trigger B rate density (default: 20)
    rate_threshold : float
        Fraction of rate_window that must cross envelope for Trigger B (default: 0.3)
    ode_residual_threshold : float
        Z-score of ODE residual to fire Trigger D (default: 2.5)
    min_triggers_for_alert : int
        Minimum simultaneous triggers for alert (default: 2)
    """

    def __init__(
        self,
        envelope_pct: float = 95.0,
        rate_window: int = 20,
        rate_threshold: float = 0.3,
        ode_residual_threshold: float = 2.5,
        min_triggers_for_alert: int = 2,
    ):
        self.envelope_pct = envelope_pct
        self.rate_window = rate_window
        self.rate_threshold = rate_threshold
        self.ode_residual_threshold = ode_residual_threshold
        self.min_triggers_for_alert = min_triggers_for_alert
        self._baseline: Optional[np.ndarray] = None

    def fit_baseline(self, series: pd.Series) -> None:
        """Fit the expanding-window baseline from historical data."""
        self._baseline = series.values.astype(float)

    def _trigger_a(self, value: float, history: np.ndarray) -> TriggerResult:
        """Statistical 95% envelope on expanding window."""
        if len(history) < 10:
            return TriggerResult("A", False, value, np.nan, "Insufficient history")
        upper = np.percentile(history, self.envelope_pct)
        lower = np.percentile(history, 100 - self.envelope_pct)
        fired = value > upper or value < lower
        threshold = upper if value > np.median(history) else lower
        return TriggerResult(
            "A", fired, value, threshold,
            f"Statistical {self.envelope_pct}th-pct envelope"
        )

    def _trigger_b(self, window: np.ndarray, history: np.ndarray) -> TriggerResult:
        """Rate density: fraction of window samples outside envelope."""
        if len(history) < 10:
            return TriggerResult("B", False, 0.0, self.rate_threshold, "Insufficient history")
        upper = np.percentile(history, self.envelope_pct)
        lower = np.percentile(history, 100 - self.envelope_pct)
        crossings = np.mean((window > upper) | (window < lower))
        fired = crossings >= self.rate_threshold
        return TriggerResult(
            "B", fired, float(crossings), self.rate_threshold,
            f"Rate density over {self.rate_window}-sample window"
        )

    def _trigger_c(self, series: np.ndarray) -> TriggerResult:
        """Geometric second-derivative spike."""
        if len(series) < 3:
            return TriggerResult("C", False, 0.0, np.nan, "Insufficient samples")
        second_deriv = np.diff(np.diff(series))
        if len(second_deriv) == 0:
            return TriggerResult("C", False, 0.0, np.nan, "Insufficient samples")
        latest = abs(second_deriv[-1])
        threshold = 2.0 * np.std(second_deriv[:-1]) if len(second_deriv) > 1 else np.nan
        fired = not np.isnan(threshold) and latest > threshold
        return TriggerResult(
            "C", fired, float(latest), float(threshold) if not np.isnan(threshold) else 0.0,
            "Geometric second-derivative spike"
        )

    def _ode_model(self, y, t, decay_rate: float = 0.05):
        """Simple first-order ODE: dy/dt = -decay_rate * y (exponential relaxation)."""
        return [-decay_rate * y[0]]

    def _trigger_d(self, series: np.ndarray) -> TriggerResult:
        """Physics-informed ODE residual."""
        if len(series) < 10:
            return TriggerResult("D", False, 0.0, self.ode_residual_threshold, "Insufficient history")
        t = np.arange(len(series))
        y0 = [series[0]]
        predicted = odeint(self._ode_model, y0, t).flatten()
        # Normalise both to zero-mean for residual comparison
        residual = (series - series.mean()) - (predicted - predicted.mean())
        residual_z = np.abs(residual[-1]) / (np.std(residual[:-1]) + 1e-8)
        fired = residual_z > self.ode_residual_threshold
        return TriggerResult(
            "D", fired, float(residual_z), self.ode_residual_threshold,
            "Physics-informed ODE residual (pre-acceleration detection)"
        )

    def evaluate(self, series: pd.Series) -> DetectionResult:
        """
        Run all four triggers on the series and return the detection result.

        Parameters
        ----------
        series : pd.Series
            Time-series values (most recent = last element)

        Returns
        -------
        DetectionResult with trigger states, risk level, and alert flag
        """
        values = series.values.astype(float)
        history = self._baseline if self._baseline is not None else values[:-1]

        latest = values[-1]
        window = values[-self.rate_window:] if len(values) >= self.rate_window else values

        results = [
            self._trigger_a(latest, history),
            self._trigger_b(window, history),
            self._trigger_c(values),
            self._trigger_d(values),
        ]

        fired = [r for r in results if r.fired]
        trigger_count = len(fired)
        state_label, risk_score = RISK_STATES[min(trigger_count, 4)]
        alert = trigger_count >= self.min_triggers_for_alert

        return DetectionResult(
            triggers=results,
            trigger_count=trigger_count,
            risk_state=state_label,
            risk_score=risk_score,
            alert=alert,
            trigger_ids_fired=[r.trigger_id for r in fired],
            prevention_simulator_activated=(state_label == "Watching Brief"),
        )
