"""
Marsham Edge — Prevention Simulator

Activated automatically when the detection engine reaches Watching Brief (2/4 triggers).
Models three intervention scenarios forward in time and returns probability distributions
for the risk state at T+30min, T+60min, T+120min.

Output is passed to Deb for inclusion in the analyst briefing.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict
from scipy.integrate import odeint


@dataclass
class SimulationScenario:
    name: str
    description: str
    intervention_strength: float  # 0.0 = none, 1.0 = maximum


@dataclass
class SimulationResult:
    scenario: str
    horizons_minutes: List[int]
    risk_probabilities: List[float]  # P(escalation) at each horizon
    expected_state: List[str]
    recommendation: str


SCENARIOS = [
    SimulationScenario("no_action", "No intervention — monitor only", 0.0),
    SimulationScenario("standard", "Standard mitigation protocol", 0.5),
    SimulationScenario("aggressive", "Aggressive intervention — full shutdown/isolation", 1.0),
]

HORIZONS = [30, 60, 120]


class PreventionSimulator:
    """
    Monte Carlo forward simulation of risk state under three intervention scenarios.

    Uses a stochastic ODE model with Brownian noise to simulate how the
    underlying anomaly signal evolves under different intervention strengths.

    Parameters
    ----------
    n_simulations : int
        Number of Monte Carlo paths per scenario (default: 500)
    dt : float
        Time step in minutes (default: 1.0)
    noise_scale : float
        Brownian motion noise scale (default: 0.05)
    """

    def __init__(
        self,
        n_simulations: int = 500,
        dt: float = 1.0,
        noise_scale: float = 0.05,
    ):
        self.n_simulations = n_simulations
        self.dt = dt
        self.noise_scale = noise_scale

    def _simulate_path(
        self,
        initial_risk: float,
        intervention_strength: float,
        horizon: int,
    ) -> np.ndarray:
        """Simulate a single risk trajectory using SDE: dR = -k*I*R*dt + sigma*dW"""
        steps = int(horizon / self.dt)
        k = 0.02  # natural decay rate
        path = np.zeros(steps + 1)
        path[0] = initial_risk
        noise = np.random.normal(0, self.noise_scale * self.dt**0.5, steps)
        for t in range(steps):
            drift = -k * intervention_strength * path[t] * self.dt
            path[t + 1] = np.clip(path[0] + drift + noise[t] * (1 - intervention_strength * 0.5), 0.0, 1.0)
            # Momentum: risk tends to continue in its current direction
            if t > 0:
                momentum = 0.1 * (path[t] - path[t - 1])
                path[t + 1] = np.clip(path[t + 1] + momentum, 0.0, 1.0)
        return path

    def _risk_to_state(self, risk: float) -> str:
        if risk < 0.15:
            return "Stable"
        elif risk < 0.35:
            return "Explanation Needed"
        elif risk < 0.60:
            return "Watching Brief"
        elif risk < 0.80:
            return "High Risk"
        else:
            return "Critical"

    def simulate(self, current_risk_score: float) -> List[SimulationResult]:
        """
        Run the Prevention Simulator from the current risk score.

        Parameters
        ----------
        current_risk_score : float
            Current risk score from the detection engine (0.0–1.0)
            At Watching Brief, this will be 0.50.

        Returns
        -------
        List of SimulationResult, one per scenario
        """
        np.random.seed(42)
        results = []

        for scenario in SCENARIOS:
            horizon_probs = []
            horizon_states = []

            for horizon in HORIZONS:
                paths = np.array([
                    self._simulate_path(
                        current_risk_score,
                        scenario.intervention_strength,
                        horizon,
                    )
                    for _ in range(self.n_simulations)
                ])
                final_risks = paths[:, -1]
                p_escalation = float(np.mean(final_risks > 0.60))  # P(High Risk or Critical)
                expected_risk = float(np.median(final_risks))
                horizon_probs.append(round(p_escalation, 3))
                horizon_states.append(self._risk_to_state(expected_risk))

            # Recommendation logic
            if scenario.name == "no_action":
                rec = f"P(escalation to High Risk) at T+30: {horizon_probs[0]:.0%}. Intervention recommended."
            elif scenario.name == "standard":
                rec = f"Standard protocol reduces P(escalation) to {horizon_probs[0]:.0%} at T+30."
            else:
                rec = f"Aggressive intervention reduces P(escalation) to {horizon_probs[0]:.0%} at T+30."

            results.append(SimulationResult(
                scenario=scenario.description,
                horizons_minutes=HORIZONS,
                risk_probabilities=horizon_probs,
                expected_state=horizon_states,
                recommendation=rec,
            ))

        return results

    def briefing_summary(self, current_risk_score: float) -> Dict:
        """
        Return a structured dict suitable for Deb's analyst briefing.
        """
        sim_results = self.simulate(current_risk_score)
        return {
            "current_risk_score": current_risk_score,
            "current_state": self._risk_to_state(current_risk_score),
            "scenarios": [
                {
                    "scenario": r.scenario,
                    "T+30_p_escalation": r.risk_probabilities[0],
                    "T+60_p_escalation": r.risk_probabilities[1],
                    "T+120_p_escalation": r.risk_probabilities[2],
                    "expected_state_T+30": r.expected_state[0],
                    "recommendation": r.recommendation,
                }
                for r in sim_results
            ],
        }
