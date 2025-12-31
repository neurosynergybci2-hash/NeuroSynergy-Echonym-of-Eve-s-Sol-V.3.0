# framework/ux_layer.py
import numpy as np
from collections import deque

class UXLayer:
    def __init__(self, vector_dim: int, window_size: int = 3):
        self.vector_dim = vector_dim
        self.standard_window = window_size
        self.history = deque(maxlen=window_size)

    def get_perceptual_output(self, raw_candidate, context_stability: float, user_distress: float):
        # N=1 Truth-Shock if distress is high or stability low
        current_window = 1 if (user_distress > 0.8 or context_stability < 0.4) else self.standard_window
        self.history.append(raw_candidate)
        if current_window == 1 or len(self.history) < 2:
            return raw_candidate
        return np.mean(list(self.history), axis=0)

    def rank_drift(self, severity_score: int):
        mapping = {0: "STABLE", 2: "LOCAL_DRIFT", 3: "IDENTITY_CREEP", 5: "CRITICAL_BREACH"}
        return mapping.get(severity_score, "ANOMALY")
