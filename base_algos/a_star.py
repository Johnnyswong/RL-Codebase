import numpy as np
from loguru import logger
from tools import *
"""
implementation for a star algorithm to solve a maze problem
author: junninghuang
"""
class PriorityQueue(object): 
    def __init__(self): 
        self.queue = [] 
  
    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 
  
    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == 0
  
    # for inserting an element in the queue 
    def insert(self, data): 
        self.queue.append(data) 
  
    # for popping an element based on Priority 
    def pop(self): 
        try: 
            _min = 0
            for i in range(len(self.queue)): 
                if self.queue[i].value < self.queue[_min].value: 
                    _min = i 
            item = self.queue[_min] 
            del self.queue[_min] 
            return item 
        except IndexError: 
            print() 
            exit() 

class Node(object):
    def __init__(self, index, value=0):
        self.index = index
        self.value = value

def search_act(cur_node, prev_node):
    for i in range(4):
        if prev_node + n[i] == cur_node:
            return i

def construct_path_policy(path, start=0, goal=11):
    shortest_path = [goal]
    policy = []
    cur_node = goal
    next_node = goal
    while cur_node != start:
        cur_node = path[cur_node]
        shortest_path.insert(0, cur_node)
        policy.insert(0, search_act(next_node, cur_node))
        next_node = cur_node
    return shortest_path, policy

def a_star(start, goal, cost, weight, heuristic_type="l1_norm"):
    """
    Input: start int, goal int, cost 1D list, weight 1D list
    Output: cost 1D list, path 1D list
    path stores the shortest previous node
    """

    heuristic_func = eval(heuristic_type)

    node = Node(start, 0)
    priority_queue = PriorityQueue()
    priority_queue.insert(node)
    path = [0] * (h*w)

    while not priority_queue.isEmpty():
        cur_node = priority_queue.pop()
        cur_idx = cur_node.index

        if cur_idx == goal:
            return path, cost

        for i in range(4):
            _neibor_invalid = neibor_invalid(cur_idx, n[i], h, w)
            if _neibor_invalid:
                continue
            neibor = cur_idx + n[i]
            if cost[cur_idx] + weight[neibor] < cost[neibor]:
                cost[neibor] = cost[cur_idx] + weight[neibor]
                g_x = cost[neibor]
                h_x = heuristic_func(cur_idx // w, cur_idx % w, goal // w, goal % w) # heuristic cost
                node = Node(neibor, g_x + h_x)
                priority_queue.insert(node)
                path[neibor] = cur_idx
    
if __name__ == '__main__':
    weight = np.array([0, 2, 0, 1, 2, 2, 2, 1, 1, 2, 3, 0])
    weight += 1
    cost = np.array([1000]*12)
    cost[0] = 0
    start = 0
    goal = 11
    # define four directions
    h, w = 4, 3
    n = [0] * 4
    n[0] = -w
    n[1] = 1
    n[2] = w
    n[3] = -1

    path, cost = a_star(start, goal, cost, weight)    
    ss_path, policy = construct_path_policy(path)
    display(weight, ss_path, h, w) 

