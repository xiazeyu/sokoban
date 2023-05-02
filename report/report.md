## Sokoban Assignment

## Assessment 1 of CAB320

### Group Members

- Zeyu Xia (n11398299)
- Tian-Ching Lan (n11262141)

### Design

Designing an environment to run algorithms that solve Sokoban is a complex task that involves multiple steps. The first step is to simulate the Sokoban gaming environment with a data structure that can represent the game board, the position of the boxes, and the player. Then, functions that represent the player's movements and validate actions for each state are created.

Once the Sokoban environment is set up, the search algorithm can be used with the given structure in search.py. This structure includes methods and objects that handle what is contained in a Node, what edges a node can go to, and the strategy for exploring Nodes. These methods and objects are mostly used as provided, rather than being rebuilt.

The last step is to determine the parameters that drive informed search algorithms, which are usually functions. By providing a fit function that correctly evaluates the priority, the optimized algorithm can balance between time efficiency and correctness.

In this project, we provide two strategies for solving Sokoban. One is based on the cost of worker moves, and we can add heuristics to lower the priority of impassable or inefficient situations. The other is driven by box moves, iterating from box moves to find the lowest cost moves for the worker to push the box into the desired position. This approach takes advantage of the fact that box movements are usually simpler than worker movements, resulting in shorter running times and lower complexity.

Both modes will be compared in further reports, but only one will be named SokobanPuzzle for grading purposes.


#### State
There are two main objects used to simulate the play environment: Problem and State. The Problem object describes everything at the start of the game, including the worker, boxes, targets, and walls position, as well as the weight of the boxes in the order they appear.

The State object represents a game situation, such as when the worker moves up and pushes box A. Rather than creating a new Problem object, the simulation returns a new State. This approach is more resource-efficient since not all fields are modified during the simulation process, and storing duplicate data would be wasteful. In Sokoban, only the boxes and worker positions are movable, so only these fields are included in a State.

For usage, most operations in the Problem class are driven by State. For example, to evaluate valid moves, we need both the wall positions and worker position, which are stored in the State object. Additionally, the Heuristics used to evaluate the priority of each case are based on State.

Since a State only represents the current situation, there is no difference between the State of the box-driven model and the State of the worker-driven model.

#### Heuristics
Heuristics refer to functions that estimate the cost of the cheapest path from a given node to the goal node. With heuristics, a Dijkstra algorithm with a big O of (n^2) can become an A* algorithm with an O of (nlogn) by filtering out inefficient situations. However, the limitation of heuristics is that it is still not the actual correct cost, so if the weight of the heuristic evaluation is too high relative to the path costs, the algorithm may behave more like a greedy search, which will not always return the lowest cost solution.

There are five heuristics implemented in this project for both the box-driven model and the worker-driven model. These include no heuristics, heuristics based on the average Manhattan distance between targets and boxes, heuristics based on the Manhattan distance of each paired target and box, heuristics based on the average Dijkstra cost from boxes to targets, and heuristics based on the Dijkstra costs from paired boxes to targets.

[the description of each heuristics ]

#### Important Features

### Test

How to validate the code?

Did we create toy problems to verify that our code behave as expected?

### Performance and Limitations

