
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_NAMES = ['N', 'E', 'S', 'W']

class ModelBasedAgent:
    """Maintains an internal model: its own (relative) position and heading,
    the cells it has visited, and the walls it has discovered. Uses that memory
    to avoid re-treading and to escape the loops a reflex agent falls into."""

    def __init__(self, start_heading=0):
        self.pos = (0, 0)             
        self.heading = start_heading  
        self.visited = {(0, 0)}
        self.known_walls = set()
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
       
       
       
        if self.last_action == 'move_forward':
            dx, dy = DIRECTIONS[self.heading]
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        elif self.last_action == 'turn_left':
            self.heading = (self.heading - 1) % 4
        elif self.last_action == 'turn_right':
            self.heading = (self.heading + 1) % 4
        self.visited.add(self.pos)

       
        fx, fy = DIRECTIONS[self.heading]
        forward_cell = (self.pos[0] + fx, self.pos[1] + fy)
        if percept['wall_ahead']:
            self.known_walls.add(forward_cell)

       
        action = self._decide(percept, forward_cell)
        self.last_action = action
        return action

    def _fresh(self, cell):
        """A cell worth going to: not visited and not a known wall."""
        return cell not in self.visited and cell not in self.known_walls

    def _decide(self, percept, forward_cell):
        if percept['food_here']:
            return 'suck'

        lx, ly = DIRECTIONS[(self.heading - 1) % 4]
        rx, ry = DIRECTIONS[(self.heading + 1) % 4]
        left_cell = (self.pos[0] + lx, self.pos[1] + ly)
        right_cell = (self.pos[0] + rx, self.pos[1] + ry)

        
        if not percept['wall_ahead'] and self._fresh(forward_cell):
            return 'move_forward'
        
        if self._fresh(left_cell):
            return 'turn_left'
        if self._fresh(right_cell):
            return 'turn_right'
        
        if not percept['wall_ahead']:
            return 'move_forward'
        return 'turn_left'