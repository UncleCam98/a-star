# next_action.py
# Compute ONE action at a time from grid + A* path, in (x,y). No diagonals.

# Cardinal directions as (dx, dy). y grows downwards.
DIR_VECT = {
    'N': (0, -1),
    'E': (1,  0),
    'S': (0,  1),
    'W': (-1, 0),
}
# Reverse mapping
VECT_DIR = {
    (0, -1): 'N',
    (1,  0): 'E',
    (0,  1): 'S',
    (-1, 0): 'W',
}

# Define turn mappings
TURN_RIGHT = {'N':'E','E':'S','S':'W','W':'N'}
TURN_LEFT  = {'N':'W','W':'S','S':'E','E':'N'}

def desired_direction(a, b):
    """Return 'N','E','S','W' for a step from cell a(x,y) to b(x,y)."""
    dx, dy = b[0]-a[0], b[1]-a[1]
    d = VECT_DIR.get((dx, dy))
    if d is None:
        raise ValueError(f"Non-cardinal step in path: {(dx,dy)}")
    return d

def turns_needed(curr, target):
    """Minimal turn sequence from curr→target."""
    if curr == target:
        return []
    if TURN_RIGHT[curr] == target:
        return ['RIGHT']
    if TURN_LEFT[curr] == target:
        return ['LEFT']
    return ['AROUND']  # 180°

def next_action_from_path(path, init_heading='N', allow_back=False):
    """
    Given a path [(x,y), ...] and current heading, return ONE action.
    Possible actions:
      ('TURN','LEFT'|'RIGHT'|'AROUND') or ('FORWARD',1) or ('BACK',1) or ('STOP',None)
    """
    if not path or len(path) < 2:
        return ('STOP', None), init_heading

    # Next waypoint is the very next cell on the path
    curr = path[0]
    nxt  = path[1]
    need_dir = desired_direction(curr, nxt)

    # Determine turns required from current heading
    need = turns_needed(init_heading, need_dir)

    if need == ['AROUND'] and allow_back:
        # Prefer BACK 1 instead of 180° + FWD 1 (optional)
        return ('BACK', 1), init_heading  # heading unchanged when backing
    elif need:
        # Turn once (only ONE action per call)
        turn = need[0]
        # Update heading after the chosen turn
        new_heading = (TURN_RIGHT[init_heading] if turn=='RIGHT'
                       else TURN_LEFT[init_heading] if turn=='LEFT'
                       else TURN_RIGHT[TURN_RIGHT[init_heading]])
        return ('TURN', turn), new_heading
    else:
        # Already facing the right way: move one cell
        return ('FORWARD', 1), init_heading

# Determine code commands for actions to use in C program
def encode_action_ascii(action):
    """
    Map action to simple ASCII for your C program.
      ('TURN','LEFT')   -> 'TL;90'
      ('TURN','RIGHT')  -> 'TR;90'
      ('TURN','AROUND') -> 'TR;180'   # or your preferred convention
      ('FORWARD',1)     -> 'F;1'
      ('BACK',1)        -> 'B;1'
      ('STOP',None)     -> 'STOP'
    """
    kind, val = action
    if kind == 'FORWARD':
        return f"F;{val}"
    if kind == 'BACK':
        return f"B;{val}"
    if kind == 'TURN':
        deg = 180 if val == 'AROUND' else 90
        return f"{'TR' if val!='LEFT' else 'TL'};{deg}"
    return "STOP"
