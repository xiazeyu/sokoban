#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:05:06 2023

@author: zeyuxia
"""

from sokoban import Warehouse
from mySokobanSolver import SokobanPuzzle
from search import FIFOQueue, breadth_first_graph_search

wh = Warehouse()
wh.load_warehouse("./warehouses/test_push.txt")
wh.load_warehouse("./warehouses/warehouse_8a.txt")

pz=SokobanPuzzle(wh)
state = pz.initial

action_queue = [
    (1, 'Left'),
    (0, 'Down'),
    (0, 'Right'),
    (0, 'Right'),
    (0, 'Right'),
    (1, 'Left'),
    (1, 'Down'),
    (1, 'Left'),
    (0, 'Right'),
    (0, 'Right'),
    (0, 'Right'),
    (0, 'Right'),
    (0, 'Right'),
]

Q = FIFOQueue()
c = 0
for act in action_queue:
    Q.append(act)

while len(Q) > 0:
    now_act = Q.pop()
    new_cost = pz.path_cost(0, state, now_act)
    print(f'actions: {pz.actions(state)} goal:{pz.goal_test(state)}')
    print(f'execute: {now_act}')
    print(f'state: {state} cost: +{new_cost}={c}')
    c += new_cost
    state = pz.result(state, now_act)


print(f'actions: {pz.actions(state)} goal:{pz.goal_test(state)}')
print(f'execute: {now_act}')
print(f'state: {state} cost={c}')

goal_node = breadth_first_graph_search(pz)

# [(<Node {'worker': (6, 3), 'boxes': [(3, 2), (5, 2)]}>, None),
#  (<Node {'worker': (3, 2), 'boxes': [(3, 3), (5, 2)]}>, (0, 'Down')),
#  (<Node {'worker': (3, 3), 'boxes': [(2, 3), (5, 2)]}>, (0, 'Left')),
#  (<Node {'worker': (5, 2), 'boxes': [(2, 3), (6, 2)]}>, (1, 'Right')),
#  (<Node {'worker': (6, 2), 'boxes': [(2, 3), (7, 2)]}>, (1, 'Right')),
#  (<Node {'worker': (7, 2), 'boxes': [(2, 3), (8, 2)]}>, (1, 'Right')),
#  (<Node {'worker': (8, 2), 'boxes': [(2, 3), (8, 3)]}>, (1, 'Down')),
#  (<Node {'worker': (8, 3), 'boxes': [(2, 3), (9, 3)]}>, (1, 'Right')),
#  (<Node {'worker': (9, 3), 'boxes': [(2, 3), (10, 3)]}>, (1, 'Right')),
#  (<Node {'worker': (10, 3), 'boxes': [(2, 3), (11, 3)]}>, (1, 'Right'))]

# node:<Node {'worker': (3, 2), 'boxes': [(3, 3), (5, 2)]}>
# parent: <Node {'worker': (6, 3), 'boxes': [(3, 2), (5, 2)]}>
# action: (0, 'Down')
# start->end: (6,3)->(3,1)
# program: (3,1)