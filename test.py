#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:05:06 2023

@author: zeyuxia
"""

from sokoban import Warehouse
from mySokobanSolver import SokobanPuzzle

wh = Warehouse()
wh.load_warehouse("./warehouses/test_push.txt")

pz=SokobanPuzzle(wh)
