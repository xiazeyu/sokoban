#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:05:06 2023

@author: zeyuxia
"""

from sokoban import Warehouse
from mySokobanSolver import SokobanPuzzle, solve_weighted_sokoban
from search import FIFOQueue, breadth_first_graph_search

wh = Warehouse()
wh.load_warehouse("./warehouses/warehouse_01.txt")

pz=SokobanPuzzle(wh)
state = pz.initial

action_queue = [
    (0, 'Up'),
    (1, 'Left'),
    (1, 'Up'),
    (1, 'Right'),
    (0, 'Down'),
    (1, 'Left'),
    (1, 'Up'), # [(0, 'Down'), (1, 'Down')]
    (1, 'Up'),
]

Q = FIFOQueue()
c = 0
for act in action_queue:
    Q.append(act)

print(f'initial: {state} cost: 0')
print(f'actions: {pz.actions(state)} goal:{pz.goal_test(state)}')

while len(Q) > 0:
    now_act = Q.pop()
    print(f'execute: {now_act}')
    new_cost = pz.path_cost(0, state, now_act)
    state = pz.result(state, now_act)
    c += new_cost
    print(f'state: {state} cost: +{new_cost}={c}')
    print(f'actions: {pz.actions(state)} goal:{pz.goal_test(state)}')

goal_node = breadth_first_graph_search(pz)

answer, cost = solve_weighted_sokoban(wh)
wh.load_warehouse("./warehouses/warehouse_8a.txt")
answer, cost = solve_weighted_sokoban(wh)
# 8a
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
# program(end): (3,1)->(4,1)->(5,1)(4,2)->(6,1){5,1}->(6,2)