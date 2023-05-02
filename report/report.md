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
Think about what is static and what is dynamic in the problem.
In this problem, 
• Where do you think static things should go? Problem instance or state?
• Where do you think dynamic things should go? Problem instance or state?

There are two similar objects in the structure, one is Problem, another is State. 

Problem describing everything while the game start, the worker, boxes, targets and walls position will be included, besides, the boxes' weight will be given in the order of boxes as well. 

A state represents a situation of the game. For example, if worker moves up and pushes the box A, it will return a new State rather than a Problem. 

To use a State, rather than a new Problem, is for saving resources. Because not all fields will be modified during the simulation process, the storage of duplicate data would be wasted. in this project, only the boxes and worker position are movable, so only these two will be included in a state.

#### Heuristics


#### Important Features

### Test

How to validate the code?

Did we create toy problems to verify that our code behave as expected?

### Performance and Limitations

