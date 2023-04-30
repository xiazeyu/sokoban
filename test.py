#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:05:06 2023

@author: zeyuxia
"""

from sokoban import Warehouse
from mySokobanSolver import SokobanPuzzle
from search import FIFOQueue

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