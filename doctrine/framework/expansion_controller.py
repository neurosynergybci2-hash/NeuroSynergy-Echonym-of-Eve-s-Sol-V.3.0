# framework/expansion_controller.py
from doctrine.self_expansion import MobiusLock

class ExpansionController:
    def __init__(self, origin, initial_state):
        self.lock = MobiusLock(origin, initial_state)
        
    def process_expansion(self, candidate, user_distress=0.0):
        # The Emergency Ascent bypass (Refinement 3)
        if user_distress > 0.9:
            return candidate, 0, "EMERGENCY_ASCENT_ACTIVE"
            
        is_valid, severity, metrics = self.lock.validate_candidate(candidate)
        if is_valid:
            self.lock.accept_candidate(candidate)
            return candidate, severity, "SUCCESS"
        return self.lock.current_state, severity, "ROLLBACK_TRIGGERED"
