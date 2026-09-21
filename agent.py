# agent.py  -  Lab 03: Uninformed Search (BFS / DFS / UCS)
from collections import deque
import heapq
import math

STEP_ACTIONS = {
    (0, 1): 'Up',
    (0, -1): 'Down',
    (-1, 0): 'Left',
    (1, 0): 'Right',
}


class SearchAgent:

    def __init__(self, active_algo='BFS'):
        self.plan = []
        # Lab 03 starts with BFS; pass DFS or UCS to compare strategies.
        self.active_algo = active_algo

    
    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:                                  
            start = tuple(percept['agent_pos'])
            foods = [tuple(f) for f in percept['all_food']]
            if not foods:
                return 'suck'                              
            walls = set(tuple(w) for w in percept['walls'])
            grid = percept['grid_size']
            goal = self._closest_food(start, foods)

            if self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, goal, walls, grid)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, goal, walls, grid)
            # A* combines the travel cost with a heuristic estimate to the goal.
            elif self.active_algo == 'AStar':
                self.plan = self.astar_search(start, goal, walls, grid)
            else:
                self.plan = self.bfs_search(start, goal, walls, grid)

            if not self.plan:
                return 'suck'                             
        return self.plan.pop(0)                            

    
    def _closest_food(self, start, foods):
        """Pick the food with the smallest Manhattan distance to the agent."""
        return min(foods, key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1]))

    # Heuristic for 4-way grid movement: horizontal distance plus vertical distance.
    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    # Straight-line heuristic, useful for comparing distance estimates.
    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

    def _neighbors(self, pos, walls, grid):
        """Legal 4-connected moves from pos as (action, new_pos) pairs."""
        w, h = grid
        x, y = pos
        out = []
        for (dx, dy), action in STEP_ACTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in walls:
                out.append((action, (nx, ny)))
        return out

    
    def bfs_search(self, start, goal, walls, grid):
        frontier = deque([(start, [])])
        reached = {start}                                 
        while frontier:
            pos, path = frontier.popleft()                 
            if pos == goal:
                return path
            for action, npos in self._neighbors(pos, walls, grid):
                if npos not in reached:
                    reached.add(npos)
                    frontier.append((npos, path + [action]))
        return []                                          # goal unreachable

    
    def dfs_search(self, start, goal, walls, grid):
        frontier = [(start, [])]
        reached = {start}
        while frontier:
            pos, path = frontier.pop()                     
            if pos == goal:
                return path
            for action, npos in self._neighbors(pos, walls, grid):
                if npos not in reached:
                    reached.add(npos)
                    frontier.append((npos, path + [action]))
        return []

    
    def ucs_search(self, start, goal, walls, grid):
        counter = 0                                        
        frontier = [(0, counter, start, [])]               
        best = {start: 0}
        while frontier:
            cost, _, pos, path = heapq.heappop(frontier)   
            if pos == goal:
                return path
            for action, npos in self._neighbors(pos, walls, grid):
                new_cost = cost + 1                        
                if npos not in best or new_cost < best[npos]:
                    best[npos] = new_cost
                    counter += 1
                    heapq.heappush(frontier, (new_cost, counter, npos, path + [action]))
        return []

    def astar_search(self, start_pos, goal_pos, walls, grid_size,
                     heuristic_type='manhattan'):
        """Find a shortest path using f(n) = g(n) + h(n)."""
        heuristic = (self.euclidean_distance if heuristic_type == 'euclidean'
                     else self.manhattan_distance)
        start_h = heuristic(start_pos, goal_pos)
        # Priority entries hold (f-cost, g-cost, state, action path).
        frontier = [(start_h, 0, start_pos, [])]
        reached_states = set()
        best_cost = {start_pos: 0}

        while frontier:
            _, g_cost, current_pos, path_taken = heapq.heappop(frontier)
            if current_pos in reached_states:
                continue
            if current_pos == goal_pos:
                return path_taken
            reached_states.add(current_pos)

            for action, neighbor in self._neighbors(current_pos, walls, grid_size):
                if neighbor in reached_states:
                    continue
                new_g_cost = g_cost + 1
                if new_g_cost < best_cost.get(neighbor, float('inf')):
                    best_cost[neighbor] = new_g_cost
                    new_f_cost = new_g_cost + heuristic(neighbor, goal_pos)
                    heapq.heappush(
                        frontier,
                        (new_f_cost, new_g_cost, neighbor, path_taken + [action]),
                    )
        return []  # No route exists to the selected food pellet.
