class SimpleReflexAgent:
    """Pure condition-action rules. No __init__, no memory of the past."""

    def sense_and_act(self, percept: dict) -> str:
        if percept['food_here']:          
            return 'suck'
        elif percept['wall_ahead']:      
            return 'turn_left'
        else:                             
            return 'move_forward'