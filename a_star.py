import heapq
from collections import deque
from grid import draw_grid, identify_start, identify_goal

# 1 = wall
# 5 = threat that we must not pass through
OBSTACLE_VALUES = {1, 5}

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def isEmpty(self):
        return len(self.elements) == 0

    def add(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def remove(self):
        return heapq.heappop(self.elements)[1]


def is_free_for_robot(center, grid, robot_radius=1):
    """
    Checks if a robot that is (2*radius+1)x(2*radius+1)
    fits with its center at 'center' (x,y).
    """
    x, y = center
    rows, cols = len(grid), len(grid[0])

    for dy in range(-robot_radius, robot_radius + 1):
        for dx in range(-robot_radius, robot_radius + 1):
            nx, ny = x + dx, y + dy

            # Outside the map = invalid
            if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
                return False

            cell = grid[ny][nx]
            if cell in OBSTACLE_VALUES:  # wall or threat
                return False

    return True


def heuristic(a, b):
    """Manhattan distance in (x, y)."""
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def get_neighbors(pos, grid):
    """
    4-neighbors in (x, y) for a robot that is 3x3.
    Only positions where the ENTIRE 3x3 area is free are allowed.
    """
    x, y = pos
    rows, cols = len(grid), len(grid[0])
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            # Check that the robot fits with margin (3x3)
            if is_free_for_robot((nx, ny), grid, robot_radius=1):
                yield (nx, ny)


def find_nearest_valid(center, grid, robot_radius=1, max_search_radius=None):
    """
    If center is NOT valid for the robot (e.g., too close to a wall),
    find the nearest cell where is_free_for_robot == True.

    max_search_radius (Manhattan) can be set if you want to limit the search.
    Returns:
        (x,y) new center position or None if none is found.
    """
    if center is None:
        return None

    # If it is already valid, keep it
    if is_free_for_robot(center, grid, robot_radius=robot_radius):
        return center

    rows, cols = len(grid), len(grid[0])
    cx, cy = center

    q = deque()
    visited = set()

    q.append(center)
    visited.add(center)

    while q:
        x, y = q.popleft()

        # If position is valid for robot, return it
        if is_free_for_robot((x, y), grid, robot_radius=robot_radius):
            return (x, y)

        # Otherwise expand neighbors
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < cols and 0 <= ny < rows):
                continue

            if (nx, ny) in visited:
                continue

            # If we have max_search_radius, skip if too far away
            if max_search_radius is not None:
                if abs(nx - cx) + abs(ny - cy) > max_search_radius:
                    continue

            visited.add((nx, ny))
            q.append((nx, ny))

    # Didn't find any place where the robot fits
    return None


def search(grid, goaltype=None):
    """
    A* in (x, y) with 3x3 robot and auto-adjustment of start/goal
    if they are too close to a wall.

    grid: 2D list with e.g.:
        0 = free
        1 = wall
        2 = start / crab
        3 = food
        4 = home
        5 = threat
    goaltype:
        "FOOD" or "HOME" (depending on what you send from test.py)

    Returns:
        nodes_expanded, path (list of (x,y)) or (nodes_expanded, None)
    """
    start_raw = identify_start(grid)
    goal_raw = identify_goal(grid, goal_type=goaltype)

    if start_raw is None or goal_raw is None:
        # Could not find start or goal in the grid
        return 0, None

    # --- Adjust so the robot is not too close to a wall ---
    start = find_nearest_valid(start_raw, grid, robot_radius=1)
    goal = find_nearest_valid(goal_raw, grid, robot_radius=1)

    if start is None or goal is None:
        # No place nearby where the robot fits
        return 0, None

    pq = PriorityQueue()
    pq.add(start, 0)

    came_from = {start: None}
    g_score = {start: 0}
    nodes = 0

    while not pq.isEmpty():
        current = pq.remove()
        nodes += 1

        
        if current == goal:
            # Reconstruct path as a list of tuples
            path = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()

            # Convert to a queue
            path_queue = deque(path)
            return nodes, path_queue


        for nxt in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                f_score = tentative_g + heuristic(nxt, goal)
                came_from[nxt] = current
                pq.add(nxt, f_score)

    return nodes, None
