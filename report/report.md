## Sokoban Assignment

## Assessment 1 of CAB320

### Group Members

- Zeyu Xia (n11398299)
- Tian-Ching Lan (n11262141)

### Design

Designing an environment to run algorithms that solve Sokoban is a complex task that involves multiple steps. 

The first step is to simulate the Sokoban gaming environment with a data structure that can represent the game board and the position of the boxes and the player. Then, the functions that represent operation from the gamer is be created such as validate actions for each case (state) or the result of taking an operation.

After the environment of Sokoban had been successfully set up, the search algorithm was ready to be used in the given structure. the given structure in search.py includes methods and objects that handle what is contained in a Node, what edges can a node go to, and the strategy of how Nodes be explored. This is complex but provided so we were mostly using, not rebuilding these methods and objects. 

The last part of development is to figure out the parameter that drives informed search algorithms, which are usually functions. By providing a fit function that correctly evaluates the priority the optimised algorithm which has a balance between time efficiency and correctness will be activated.


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

