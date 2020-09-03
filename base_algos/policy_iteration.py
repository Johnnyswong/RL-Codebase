from tools import *
import numpy as np 
from loguru import logger
import copy

def policy_evaluation(v_table, r_table, policy, terminals):
    for i in range(iters):
        v_table_last = copy.copy(v_table) # v table in last iteration
        for state in range(len(v_table)):
            v_tmp = 0
            if terminals[state]:
                continue
            for action in range(4):
                next_state = state + n[action] # deterministic transition    
                next_state_invalid = neibor_invalid(state, n[action], h, w)
                if next_state_invalid:
                    next_state = state
                v_tmp += policy[state][action]*(r_table[next_state] + (1-terminals[next_state]) * gamma * v_table_last[next_state]) # deterministic transition
            v_table[state] = v_tmp
    return v_table

def policy_improvement(v_table, r_table, policy, terminals):
    for state in range(len(v_table)):
        q_choice = []
        for action in range(4):
            next_state = state + n[action]
            next_state_invalid = neibor_invalid(state, n[action], h, w)
            if next_state_invalid:
                next_state = state
            q_choice.append(r_table[next_state] + (1-terminals[next_state]) * gamma * v_table[next_state])
        opt_action = np.argmax(q_choice)
        policy[state][:] = 0
        policy[state][opt_action] = 1
    return policy

if __name__ == '__main__':
    h, w = 4, 3
    r_table = np.array([0, 2, 0, 1, 2, 2, 2, 1, 1, 2, 3, 0])
    r_table += 1
    r_table = r_table * -1 / 3
    terminals = np.zeros(h*w)
    terminals[-1] = 1

    v_table = [0] * h * w
    policy = np.array([[0.25]*4]*h*w)
    iters = 30
    gamma = 1.0

    # define action content
    n = [0] * 4
    n[0] = -w
    n[1] = 1
    n[2] = w
    n[3] = -1

    v_table = policy_evaluation(v_table, r_table, policy, terminals)
    policy = policy_improvement(v_table, r_table, policy, terminals)
    ss_path = generate_path(policy, terminals, n, h, w)
    r_table = np.array([0, 2, 0, 1, 2, 2, 2, 1, 1, 2, 3, 0])
    r_table += 1
    display(r_table, ss_path, h, w)
