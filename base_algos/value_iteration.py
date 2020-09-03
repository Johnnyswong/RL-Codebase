from loguru import logger
from tools import *

def value_iteration(v_opt_table, r_table, terminals):
    for i in range(iters):
        v_opt_table_prev = v_opt_table
        for state in range(len(v_opt_table)):
            if terminals[state]:
                continue
            v_tmp = []
            for action in range(4):
                next_state = state + n[action] # deterministic transition
                next_state_invalid = neibor_invalid(state, n[action], h, w)
                if next_state_invalid:
                    next_state = state
                v_tmp.append(r_table[next_state] + (1-terminals[state])*gamma*v_opt_table_prev[next_state])
            v_opt = max(v_tmp)
            v_opt_table[state] = v_opt
    return v_opt_table

def generate_policy(v_opt_table, terminals):
    policy = np.array([[0]*4]*len(v_opt_table))
    for state in range(len(v_opt_table)):
        v_tmp = []
        for action in range(4):
            next_state = state + n[action] # deterministic transition
            next_state_invalid = neibor_invalid(state, n[action], h, w)
            if next_state_invalid:
                next_state = state
            v_tmp.append(r_table[next_state] + (1-terminals[state])*gamma*v_opt_table[next_state])
        opt_action = np.argmax(v_tmp)
        policy[state][:] = 0.
        policy[state][opt_action] = 1.
    return policy

if __name__ == '__main__':
    gamma = 1.
    iters = 30
    h, w = 4, 3
    v_opt_table = [0] * h * w
    r_table = np.array([0, 2, 0, 1, 2, 2, 2, 1, 1, 2, 3, 0]) 
    r_table += 1
    r_table = r_table * -1 / 3 
    terminals = np.zeros(h*w)
    terminals[-1] = 1

    # define action content
    n = [0] * 4
    n[0] = -w
    n[1] = 1
    n[2] = w
    n[3] = -1
    v_opt_table = value_iteration(v_opt_table, r_table, terminals)
    policy = generate_policy(v_opt_table, terminals)
    ss_path = generate_path(policy, terminals, n, h, w)
    r_table = np.array([0, 2, 0, 1, 2, 2, 2, 1, 1, 2, 3, 0]) 
    r_table += 1
    display(r_table, ss_path, h, w)
