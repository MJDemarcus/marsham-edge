"""
Marsham Edge Detection Models

Usage:
    from models import CNNLSTMDetector, FourTriggerEngine, PreventionSimulator

    detector = CNNLSTMDetector(sequence_length=60)
    detector.fit(training_series)

    engine = FourTriggerEngine()
    engine.fit_baseline(historical_series)
    result = engine.evaluate(live_series)

    if result.prevention_simulator_activated:
        simulator = PreventionSimulator()
        briefing = simulator.briefing_summary(result.risk_score)
"""

from .cnn_lstm_detector import CNNLSTMDetector
from .detection_engine import FourTriggerEngine, DetectionResult, RISK_STATES
from .prevention_simulator import PreventionSimulator

__all__ = [
    "CNNLSTMDetector",
    "FourTriggerEngine",
    "DetectionResult",
    "RISK_STATES",
    "PreventionSimulator",
]
__version__ = "1.0.0"
