import numpy as np
from loguru import logger
import copy
import time

def neibor_invalid(cur_idx, _dir, h, w): 
    _neibor = cur_idx + _dir
    out_of_bound = True if _neibor < 0 or _neibor >= h*w else False
    if not out_of_bound:
        un_reachable = True if (cur_idx // w) != (_neibor // w) and (cur_idx % w) != (_neibor % w) else False
    return out_of_bound or un_reachable  

def l1_norm(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

def l2_norm(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def display_once(array):
    _str = ""
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            _obj = array[i][j]
            if _obj == 0:
                _obj = " "
            elif _obj == -1:
                _obj = "P"
            else:
                _obj = str(_obj)
            _str += _obj + " "
        _str += "\n"
    logger.info(chr(27) + "[2J")
    logger.info(f"\n{_str}")
    time.sleep(1.0)
    return 0

def display(maze, path, h, w):
    rew_sum = 0
    for i in range(len(path)):
        _maze = copy.copy(maze)
        _maze[path[i]] = -1
        _maze = _maze.reshape(h, w)
        rew_sum += maze[path[i]]
        display_once(_maze)
    logger.info(f"Total reward: {rew_sum}")
    return 0

def generate_path(policy, terminals, n, h, w):
    """
    Input: rl policy: [state[action]]
           terminals: [state]
           n: [action]
           
    Output:
           [state]
    """
    terminal_state = np.where(terminals==1)[0][0]
    cur_state = 0
    path = [cur_state]
    while cur_state != terminal_state:
        opt_action = np.where(policy[cur_state]==1)[0][0]
        next_state = cur_state + n[opt_action]
        if neibor_invalid(cur_state, n[opt_action], h, w):
            next_state = cur_state
        path.append(next_state)
        cur_state = next_state
    return path
