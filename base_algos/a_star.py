import numpy as np
from loguru import logger
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

def construct_path(path, start=0, goal=11):
    shortest_path = [goal]
    cur_node = goal
    while cur_node != start:
        cur_node = path[cur_node]
        shortest_path.insert(0, cur_node)
    return shortest_path

def a_star(start, goal, cost, weight, h=23, w=35):
    """
    Input: start int, goal int, cost 1D list, weight 1D list
    Output: cost 1D list, path 1D list
    path stores the shortest previous node
    """

    def l1_norm(x1, y1, x2, y2):
        return abs(x2-x1) + abs(y2-y1)

    def neibor_invalid(cur_idx, _dir, h, w):
        _neibor = cur_idx + _dir
        out_of_bound = True if _neibor < 0 or _neibor > h*w else False
        if not out_of_bound:
            un_reachable = True if (cur_idx // w) != (_neibor // w) and (cur_idx % w) != (_neibor % w) else False
        return out_of_bound or un_reachable

    node = Node(start, 0)
    priority_queue = PriorityQueue()
    priority_queue.insert(node)
    path = [0] * (h*w)

    # define four directions
    n = [0] * 4
    n[0] = -w
    n[1] = 1
    n[2] = w
    n[3] = -1

    while not priority_queue.isEmpty():
        cur_node = priority_queue.pop()
        cur_idx = cur_node.index

        if cur_idx == goal:
            return path, cost

        for i in range(4):
            _neibor_invalid = neibor_invalid(cur_idx, n[i], h, w)
            if _neibor_invalid:
                continue
            #logger.info(f"cur_idx: {cur_idx}, dir: {n[i]}, cost: {cost[cur_idx]}, weight: {weight[cur_idx + n[i]]}")
            neibor = cur_idx + n[i]
            if cost[cur_idx] + weight[neibor] < cost[neibor]:
                cost[neibor] = cost[cur_idx] + weight[neibor]
                g_x = cost[neibor]
                h_x = l1_norm(cur_idx // w, cur_idx % w, goal // w, goal % w) # heuristic cost
                node = Node(neibor, g_x + h_x)
                priority_queue.insert(node)
                path[neibor] = cur_idx
    
if __name__ == '__main__':
    weight = np.array([0, 2, 0, 1, 2, 2, 2, 1, 1, 2, 3, 0])
    cost = np.array([1000]*12)
    cost[0] = 0
    start = 0
    goal = 11
    path, cost = a_star(start, goal, cost, weight, 4, 3)    
    logger.info(cost)
    logger.info(construct_path(path))

