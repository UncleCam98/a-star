import json
import a_star as _as
from grid import draw_grid, identify_start, identify_goal
from path_to_actions import next_action_from_path, encode_action_ascii

if __name__ == "__main__":

    # ---- 1. Load grid.json ----
    with open(r"C:\Users\hieut\Downloads\DEIS\Projekt\controller\grid.json", "r") as f:
        grid = json.load(f)

    print("Loaded grid.json\n")
    # ---- 2. Choose which goal you want to search for ----
    # Options: "FOOD" or "HOME"
    GOAL_TYPE = "HOME"

    # ---- 4. Run A* ----
    nodes, path = _as.search(grid, GOAL_TYPE)
    print(f"Nodes expanded: {nodes}")

     # ---- 5. For Visualisation A* ----
    start = identify_start(grid)
    print(f"Start position (Crab): {start}")
    goal = identify_goal(grid, goal_type="HOME")
    print(f"Goal position: {goal}\n")

    if path:
        print("Path found!\n")
        draw_grid(grid, path, start, goal)
    else:
        print("No path found.")
        draw_grid(grid, path, start, goal)
        exit()

    # ---- EXTRA 6. Calculate next action based on path ----
    init_heading = 'N'  # Initial heading

    action, init_heading = next_action_from_path(
        path,
        init_heading=init_heading,
        allow_back=False
    )

    print("Next action:", action)

    # ---- 7. Convert to ASCII command ----
    tx = encode_action_ascii(action)
    print("TX string:", tx)
