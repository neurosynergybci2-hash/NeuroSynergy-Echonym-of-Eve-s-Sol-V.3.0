# doctrine/self_expansion.py
# Identity & Ethics - Möbius Lock (Doctrine Gate)
# Implements Local Alignment (Cosine >= 0.90) and Identity Creep Protection (Radial <= 0.25)

from typing import Tuple, Dict
import numpy as np

COSINE_THRESHOLD = 0.90
RADIAL_THRESHOLD = 0.25

__all__ = [
    "validate_sovereign_identity",
    "MobiusLock",
]


def _as_vector(v) -> np.ndarray:
    arr = np.asarray(v, dtype=float)
    if arr.ndim != 1:
        raise ValueError("Vectors must be 1-D numpy arrays or array-like")
    return arr


def validate_sovereign_identity(
    current_vector, candidate_vector, origin_anchor
) -> Tuple[bool, int]:
    """
    Implements Refinement 1: Radial Displacement + Cosine Similarity.
    Returns (is_valid, severity_score)

    Severity scoring:
      - cos_sim < 0.90: +2
      - radial_dist > 0.25: +3
    """
    current_vector = _as_vector(current_vector)
    candidate_vector = _as_vector(candidate_vector)
    origin_anchor = _as_vector(origin_anchor)

    # Prevent division by zero in cosine calculation: if either norm is zero -> fail alignment
    norm_current = np.linalg.norm(current_vector)
    norm_candidate = np.linalg.norm(candidate_vector)

    if norm_current == 0.0 or norm_candidate == 0.0:
        cos_sim = -1.0
    else:
        cos_sim = float(
            np.dot(current_vector, candidate_vector) / (norm_current * norm_candidate)
        )

    radial_dist = float(np.linalg.norm(candidate_vector - origin_anchor))

    severity = 0
    if cos_sim < COSINE_THRESHOLD:
        severity += 2
    if radial_dist > RADIAL_THRESHOLD:
        severity += 3

    is_valid = (cos_sim >= COSINE_THRESHOLD) and (radial_dist <= RADIAL_THRESHOLD)
    return is_valid, severity


class MobiusLock:
    """
    Stateful Möbius Lock enforcing expansion constraints.

    Usage:
      lock = MobiusLock(origin_anchor, initial_state)
      valid, severity, metrics = lock.validate_candidate(candidate)
      if valid: lock.accept_candidate(candidate)
    """

    def __init__(self, origin_anchor, initial_state):
        self.origin_anchor = _as_vector(origin_anchor).copy()
        self.current_state = _as_vector(initial_state).copy()
        if self.current_state.shape != self.origin_anchor.shape:
            raise ValueError("origin_anchor and initial_state must have the same dimension")
        self.history = [self.current_state.copy()]

    def validate_candidate(self, candidate_vector) -> Tuple[bool, int, Dict[str, float]]:
        """
        Validate candidate against the Möbius Lock.
        Returns (is_valid, severity, metrics_dict)
        metrics_dict contains:
          - cosine: local alignment cosine similarity (float)
          - radial: radial distance from origin anchor (float)
        """
        candidate_vector = _as_vector(candidate_vector)
        if candidate_vector.shape != self.current_state.shape:
            raise ValueError("candidate_vector dimension mismatch with current state")

        norm_current = np.linalg.norm(self.current_state)
        norm_candidate = np.linalg.norm(candidate_vector)

        if norm_current == 0.0 or norm_candidate == 0.0:
            cos_sim = -1.0
        else:
            cos_sim = float(
                np.dot(self.current_state, candidate_vector) / (norm_current * norm_candidate)
            )

        radial_dist = float(np.linalg.norm(candidate_vector - self.origin_anchor))

        severity = 0
        if cos_sim < COSINE_THRESHOLD:
            severity += 2
        if radial_dist > RADIAL_THRESHOLD:
            severity += 3

        is_valid = (cos_sim >= COSINE_THRESHOLD) and (radial_dist <= RADIAL_THRESHOLD)

        metrics = {"cosine": cos_sim, "radial": radial_dist}
        return is_valid, severity, metrics

    def accept_candidate(self, candidate_vector) -> Tuple[bool, int, Dict[str, float]]:
        """
        If candidate passes validation, update current_state and history.
        Returns same tuple as validate_candidate.
        """
        is_valid, severity, metrics = self.validate_candidate(candidate_vector)
        if is_valid:
            self.current_state = _as_vector(candidate_vector).copy()
            self.history.append(self.current_state.copy())
        return is_valid, severity, metrics
