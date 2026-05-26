"""
Marsham Edge - Li-ion Battery Thermal Runaway Detection

Real-world MVP for early detection of thermal runaway precursors in Li-ion
battery systems. Uses the four-trigger detection engine adapted for
electrochemical signal profiles.
"""

from .anomaly_detection import AnomalyDetector
from .runaway_classifier import RunawayClassifier
from .tr_prediction_pipeline import ThermalRunawayPipeline
from .early_warning_system import EarlyWarningSystem
