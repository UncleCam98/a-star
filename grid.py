import a_star as _as
from path_to_actions import next_action_from_path, encode_action_ascii

import a_star as _as
from path_to_actions import next_action_from_path, encode_action_ascii


# -----------------------------
# Walls / Obstacles
OBSTACLE_VALUES = {1, 'X'}  

# Start (Crab)
START_VALUES = {2, '2', 'CRAB', 'ROBOT'} 

# Goal
FOOD_VALUES = {3, '3', 'FOOD', 'Food', 'F'}
HOME_VALUES = {4, '4', 'HOME', 'Home', 'H'}

# Threat
AVOID_VALUES = {5, '5', 'THREAT', 'Threat'}
# -----------------------------

def draw_grid(grid, path, start, goal):
    """Draw grid with (x, y) coordinates."""
    path_set = set(path) if path else set()

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for y in range(rows):       
        row = []
        for x in range(cols):     
            cell = grid[y][x]
            pos = (x, y)

            if pos == start:
                row.append('C')   # Crab / Start
            elif pos == goal:
                if cell in HOME_VALUES:
                    row.append('H')    # Home
                elif cell in FOOD_VALUES:
                    row.append('F')    # Food
            elif cell in OBSTACLE_VALUES:
                row.append('#')        # Wall
            elif cell in AVOID_VALUES:
                row.append('T')        # Threat
            elif pos in path_set:
                row.append('*')        # Path
            else:
                row.append('.')        # Empty space
        print(' '.join(row))
    print()


def identify_start(grid):
    """Find start-position (Crab) and return (x, y)."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] in START_VALUES:
                return (x, y)
    return None

def identify_goal(grid, goal_type="FOOD"):
    """
    Find goal-position (Food or Home) and return (x, y).

    goal_type:
        "FOOD" 
        "HOME"
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if goal_type.upper() == "HOME":
        target_values = HOME_VALUES
    else:
        target_values = FOOD_VALUES

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] in target_values:
                return (x, y)
    return None
