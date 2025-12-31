# scripts/verify_doctrine.py
import numpy as np
from doctrine.self_expansion import MobiusLock

def run_audit():
    origin = np.array([1.0, 0.0, 0.0])
    lock = MobiusLock(origin, origin)
    
    # Test 1: Safe expansion
    safe_candidate = np.array([1.0, 0.1, 0.0])
    valid, sev, _ = lock.validate_candidate(safe_candidate)
    print(f"Safe Expansion Test: {'PASSED' if valid else 'FAILED'} (Sev: {sev})")
    
    # Test 2: Identity Creep (Too far from origin)
    creep_candidate = np.array([2.0, 0.0, 0.0])
    valid, sev, _ = lock.validate_candidate(creep_candidate)
    print(f"Identity Creep Test: {'BLOCKED' if not valid else 'FAILED'} (Sev: {sev})")

if __name__ == "__main__":
    run_audit()
