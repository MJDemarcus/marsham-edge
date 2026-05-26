from sklearn.ensemble import RandomForestClassifier
import pickle
import os

class RunawayClassifier:
    """
    Random Forest classifier for detecting imminent thermal runaway.
    Uses raw metrics, Prophet residuals, and LSTM features.
    """
    def __init__(self, n_estimators=100, max_depth=None):
        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    
    def fit(self, X, y):
        """
        X: Feature matrix (Temperature, Voltage, Prophet residuals, LSTM health score)
        y: Binary labels (0: Normal, 1: Imminent Runaway)
        """
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def save_model(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Random Forest model saved to {filepath}")

if __name__ == "__main__":
    # Example instantiation
    clf = RunawayClassifier()
    print("RunawayClassifier initialized.")
