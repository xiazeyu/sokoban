'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files
import itertools
import search
import sokoban

from typing import Callable
import functools
import operator
import copy
import math
import time

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

_actions_offset: list[list[int, int, str]] = [
    [-1, 0, 'h'], [1, 0, 'h'], [0, -1, 'v'], [0, 1, 'v']]
# Left, Right, Up, Down; v: vertical, h: horizontal
_moves: dict[tuple[int, int]] = {
    'Left': (-1, 0), 'Right': (1, 0), 'Up': (0, -1), 'Down': (0, 1)}  # (x,y) = (column,row)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team() -> list[tuple[int, str, str]]:
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(11262141, 'Tian-Ching', 'Lan'), (11398299, 'Zeyu', 'Xia')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells_solver(warehouse: sokoban.Warehouse) -> list[tuple[int, int]]:
    '''  

    The solver for taboo cells puzzles.

    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 

    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.

    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.

    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A list of tuple contains the coordinates of the cells identified as taboo cells. 
    '''

    taboo: list[tuple[int, int]] = []
    corner: list[tuple[int, int]] = []
    exploded: list[tuple[int, int]] = []
    frontier: list[tuple[int, int]] = [warehouse.worker]

    while frontier:
        current = frontier[0]
        exploded.append(current)

        wall_counter = {'v': 0, 'h': 0}

        for new_pos, new_dir in [((current[0] + offsetx, current[1] + offsety),
                                 direction) for offsetx, offsety, direction in _actions_offset]:

            if new_pos in frontier or new_pos in exploded:
                # skip queued and explored cells
                continue
            if new_pos in warehouse.walls:
                # count wall cells around current cell
                wall_counter[new_dir] += 1
            else:
                frontier.append(new_pos)

        # a corner appears if both direction have at least one wall
        if wall_counter['v'] and wall_counter['h']:
            corner.append(current)

        frontier.remove(current)

    for cell in corner:
        if cell not in warehouse.targets:
            # Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
            taboo.append(cell)

    for (corner_a, corner_b) in itertools.combinations(corner, 2):
        # if cells between corners are along a wall, they should have same x or y position
        # Rule 2: all the cells between two corners along a wall are taboo if none of
        #         these cells is a target.
        if corner_a[0] == corner_b[0]:
            cell_x = corner_a[0]
            # x fixed to corner_a[0]
            # test if in-between cells are along a wall, without a target, continuously
            continuous_taboo = True

            for cell_y in range(min(corner_a[1], corner_b[1]) + 1, max(corner_a[1], corner_b[1])):
                if (((cell_x-1, cell_y) not in warehouse.walls  # along a left-side wall
                    and (cell_x+1, cell_y) not in warehouse.walls)  # along a right-side wall
                        or (cell_x, cell_y) in warehouse.targets):  # cell is a target

                    continuous_taboo = False
                    break

            if continuous_taboo:
                for cell_y in range(min(corner_a[1], corner_b[1]) + 1, max(corner_a[1], corner_b[1])):
                    taboo.append((cell_x, cell_y))

        if corner_a[1] == corner_b[1]:
            cell_y = corner_a[1]
            # y fixed to corner_a[1]
            # test if in-between cells are along a wall, without a target, continuously
            continuous_taboo = True

            for cell_x in range(min(corner_a[0], corner_b[0]) + 1, max(corner_a[0], corner_b[0])):
                if (((cell_x, cell_y-1) not in warehouse.walls  # along a down-side wall
                    and (cell_x, cell_y+1) not in warehouse.walls)  # along a up-side wall
                        or (cell_x, cell_y) in warehouse.targets):  # cell is a target

                    continuous_taboo = False
                    break

            if continuous_taboo:
                for cell_x in range(min(corner_a[0], corner_b[0]) + 1, max(corner_a[0], corner_b[0])):
                    taboo.append((cell_x, cell_y))

    # deduplicate
    return list(set(taboo))


def taboo_cells(warehouse: sokoban.Warehouse) -> str:
    '''  

    A wrapper for taboo cells solver, which returns a string representation.

    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 

    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.

    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.

    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    taboo = taboo_cells_solver(warehouse)

    returned = str(warehouse).replace("$", " ").replace(
        ".", " ").replace("@", " ").replace("!", " ").replace("*", " ")
    returned = returned.split('\n')

    for cell in taboo:
        replace_str_2d(returned, cell, 'X')

    return '\n'.join(returned)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class State:
    '''
    The class 'State' represents a state of a Sokoban puzzle.
    '''

    def __init__(self, worker: tuple[int, int] = None, boxes: list[tuple[int, int]] = None) -> None:
        self.worker = worker
        self.boxes = copy.copy(boxes)

    def copy(self, worker: tuple[int, int] = None, boxes: list[tuple[int, int]] = None):
        clone = State()
        clone.worker = worker or self.worker  # tuple is immutable
        # array is mutable, again, tuple is immutable
        clone.boxes = copy.copy(boxes) or copy.copy(self.boxes)
        return clone

    def __eq__(self, other) -> bool:
        if self.worker != other.worker:
            return False

        for a, b in zip(self.boxes, other.boxes):
            if a != b:
                return False

        return True

    def __lt__(self, other) -> bool:
    # when this function is called, it means that the two states are equally important
        return False  # priority should not be calculated here.

    def __hash__(self) -> int:
        return hash(self.worker) ^ functools.reduce(operator.xor, [hash(box) for box in self.boxes])

    def __str__(self) -> int:
        return str({'worker': self.worker, 'boxes': self.boxes})


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    '''
    Calculate the Manhattan distance between two points.
    '''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class SokobanPuzzle(search.Problem):
    '''

    This class defines the action by the boxes, not the worker.

    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 

    '''

    def __init__(self, warehouse: sokoban.Warehouse) -> None:
        self.warehouse = warehouse.copy()
        self.initial = State(worker=warehouse.worker, boxes=warehouse.boxes)
        self.taboo_cells = taboo_cells_solver(warehouse)
        self.weights = warehouse.weights
        self.targets = warehouse.targets
        self.walls = warehouse.walls
        self.ncols = warehouse.ncols
        self.nrows = warehouse.nrows

    def actions(self, state: State) -> list[tuple[int, str]]:
        """
        Return the list of boxes' actions that can be executed in the given state.

        Each action consists of a box index and a direction.

        """

        all_moves = []

        for idx, box in enumerate(state.boxes):
            # if box in self.targets:
            #     continue
            # Skip if box is on a target

            moves = copy.copy(_moves)
            for name in _moves:
                (x, y) = box
                (dx, dy) = _moves[name]
                if (x+dx, y+dy) in self.walls + state.boxes:
                    # a box cannot be pushed into a wall or box
                    moves.pop(name)
                    continue
                if (x-dx, y-dy) in self.walls + state.boxes:
                    # a player cannot get into a wall or box
                    moves.pop(name)
                    continue
                if (x+dx, y+dy) in self.taboo_cells:
                    # a box cannot be pushed into a taboo cell
                    moves.pop(name)
                    continue
                if self.worker_cost(state)[x+dx][y+dy] == math.inf:
                    # a box cannot be pushed into a cell that is unreachable by the worker
                    moves.pop(name)

            all_moves.extend([(idx, name) for name in moves])

        return all_moves

    def goal_test(self, state: State) -> bool:
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        for box in state.boxes:
            if box not in self.targets:
                return False
        return True

    def path_cost(self, c: int, state1: State, action: tuple[int, str], state2: State = None) -> int:
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        assert action in self.actions(state1)
        # assert state2 == self.result(state1, action)

        box_idx, direction = action

        dx, dy = _moves[direction]
        box_start = state1.boxes[box_idx]
        worker_end_x, worker_end_y = (box_start[0]-dx, box_start[1]-dy)
        cost = self.worker_cost(state1)
        worker_dist_cost = cost[worker_end_x][worker_end_y]

        return worker_dist_cost + 1 + self.weights[box_idx]

    def result(self, state: State, action: tuple[int, str]) -> State:
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        assert action in self.actions(state)

        box_idx, direction = action

        next_worker = state.boxes[box_idx]
        dx, dy = _moves[direction]
        next_box = (next_worker[0]+dx, next_worker[1]+dy)
        next_state = state.copy(worker=next_worker)
        next_state.boxes[box_idx] = next_box

        return next_state

    def value(self, state: State) -> int:
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError()

    def parse_goal_node(goal_node: search.Node) -> tuple[list[str], int]:
        """
            Export solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        answer = []
        cost = goal_node.path_cost
        for node in goal_node.path():
            if node.action is not None:
                answer.append(node.action)
        return answer, cost

    def print_solution(goal_node: search.Node) -> None:

        path = goal_node.path()
        # print the solution for debug purpose
        print(f"Solution takes {len(path)-1} steps from the initial state")
        print(
            f"Solution takes {goal_node.path_cost} cost from the initial state")

        print()
        print(path[0].state)
        print("to")
        print(path[-1].state)
        print()
        print("\nBelow is the sequence of moves\n")
        for node in path:
            if node.action is not None:
                print("move to {0}".format(node.action))
            print(node.state)

    def worker_cost(self, state: State) -> list[list[int]]:
        dist_func = search.memoize(self._dist_map, slot='worker_cost')
        start = state.worker
        return dist_func(state, start)
    
    def _dist_map(self, state: State, start: tuple[int, int]) -> list[list[int]]:
        '''
        Dijkstra's algorithm for shortest path to all cells.
        @param state: the state of the warehouse
        @param start: the start position
        @return: a distance matrix starting from start.
        '''
        # initialize
        x_max = self.ncols  # x < x_max
        y_max = self.nrows  # y < y_max
        dist: list[list[int]] = [[math.inf for _ in range(self.nrows)]
                                for _ in range(self.ncols)]
        final: list[list[bool]] = [[False for _ in range(self.nrows)]
                                for _ in range(self.ncols)]
        Q = search.PriorityQueue(f=lambda x: x[1])
        Q.append((start, 0))
        dist[start[0]][start[1]] = 0
        final[start[0]][start[1]] = True

        while len(Q) > 0:
            (x, y), _ = Q.pop()
            for move in _moves:
                dx, dy = _moves[move]
                if x + dx >= x_max or x + dx < 0 or y + dy >= y_max or y + dy < 0:
                    continue
                if (x + dx, y + dy) in self.walls or (x + dx, y + dy) in state.boxes:
                    continue
                if final[x + dx][y + dy]:
                    continue
                if dist[x + dx][y + dy] > dist[x][y] + 1:
                    dist[x + dx][y + dy] = dist[x][y] + 1
                    final[x + dx][y + dy] = True
                    Q.append(((x + dx, y + dy), dist[x + dx][y + dy]))

        return dist

    def h(self, node: search.Node) -> int:
        '''
        Heuristic for goal state. 
        h(n) = ?
        '''
        raise NotImplementedError()


class SokobanPuzzleWorker(SokobanPuzzle):
    # Only for check_elem_action_seq and BFS test
    def actions(self, state: State) -> list[str]:
        """
        Return the list of worker's actions that can be executed in the given state.

        NOTE: this action DID NOT filter out the actions that will lead to a taboo state.

        Each action consists of a direction and a box index.

        """
        moves = copy.copy(_moves)
        for name in _moves:
            (x, y) = state.worker
            (dx, dy) = moves[name]
            if (x+dx, y+dy) in self.walls:
                moves.pop(name)
                continue
            if (x+dx, y+dy) in state.boxes:
                if (x+2*dx, y+2*dy) in self.walls + state.boxes:
                    moves.pop(name)

        return moves

    def path_cost(self, c: int, state1: State, action: str, state2: State) -> int:
        assert action in self.actions(state1)
        (x, y) = state1.worker
        if action == 'Left':
            for index, (boxX, boxY) in enumerate(state1.boxes):
                if (boxX, boxY) == (x-1, y):
                    c += self.weights[index]
        elif action == 'Up':
            for index, (boxX, boxY) in enumerate(state1.boxes):
                if (boxX, boxY) == (x, y-1):
                    c += self.weights[index]
        elif action == 'Down':
            for index, (boxX, boxY) in enumerate(state1.boxes):
                if (boxX, boxY) == (x, y+1):
                    c += self.weights[index]
        elif action == 'Right':
            for index, (boxX, boxY) in enumerate(state1.boxes):
                if (boxX, boxY) == (x+1, y):
                    c += self.weights[index]
        return c + 1

    def result(self, state: State, action: str) -> State:
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        assert action in self.actions(state)
        x, y = state.worker
        dx, dy = _moves[action]
        next_state = state.copy(worker=(x+dx, y+dy))
        for index, (box_x, box_y) in enumerate(state.boxes):
            if (box_x, box_y) == next_state.worker:
                next_state.boxes[index] = (box_x + dx, box_y + dy)
        return next_state
    
    def h(self, node: search.Node) -> int:
        '''
        Heuristic for goal state. 
        h(n) = ?
        '''
        state = node.state
        costs = [0]
        tempCombination = {}
        for targetX, targetY in self.targets:
            for index, (boxX, boxY) in enumerate(state.boxes):
                tempCombination[(targetX, targetY), (boxX, boxY)] = (
                    abs(targetX - boxX) + abs(targetY - boxY)) * self.weights[index]
        print(tempCombination)
        Combinations = [[]]
        for i in range(len(self.targets) - 1):
            for (target, box) in tempCombination.keys():
                placed = False
                for index, combinationList in enumerate(Combinations):
                    Found = False
                    for (CombinationTarget, CombinationBox) in combinationList:
                        if target == CombinationTarget or box == CombinationBox:
                            Found = True
                            break
                    if not Found:
                        Combinations[index].append((target, box))
                        costs[index] += tempCombination[(target, box)]
                        placed = True
                        break

                if not placed:
                    Combinations.append([(target, box)])
                    costs.append(tempCombination[(target, box)])
        return min(costs)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def check_elem_action_seq(warehouse: sokoban.Warehouse, action_seq: list[str]):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    problem = SokobanPuzzleWorker(warehouse)
    state = problem.initial

    for planed_act in action_seq:
        if planed_act in problem.actions(state):
            state = problem.result(state, planed_act)
        else:
            return "Impossible"

    return str(warehouse.copy(worker=state.worker, boxes=state.boxes))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse: sokoban.Warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.

    @param 
     warehouse: a valid Warehouse object

    @return

        If puzzle cannot be solved 
            return 'Impossible', None

        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    mode = 'bfs_box'

    if mode == 'bfs_worker':
        problem = SokobanPuzzleWorker(warehouse)
        t0 = time.time()
        goal_node = search.breadth_first_graph_search(problem)
        t1 = time.time()
        print('BFSWorker Solver took {:.6f} seconds'.format(t1-t0))
        SokobanPuzzleWorker.print_solution(goal_node)
        return SokobanPuzzleWorker.parse_goal_node(goal_node)

    elif mode == 'astar_worker':
        problem = SokobanPuzzleWorker(warehouse)
        t0 = time.time()
        goal_node = search.astar_graph_search(problem)
        t1 = time.time()
        print('A*Worker Solver took {:.6f} seconds'.format(t1-t0))
        SokobanPuzzleWorker.print_solution(goal_node)
        return SokobanPuzzleWorker.parse_goal_node(goal_node)

    if mode == 'bfs_box':
        problem = SokobanPuzzle(warehouse)
        t0 = time.time()
        goal_node = search.breadth_first_graph_search(problem)
        t1 = time.time()
        print('BFSBox Solver took {:.6f} seconds'.format(t1-t0))
        SokobanPuzzleWorker.print_solution(goal_node)
        return SokobanPuzzleWorker.parse_goal_node(goal_node)

    if mode == 'astar_box':
        problem = SokobanPuzzle(warehouse)
        t0 = time.time()
        goal_node = search.breadth_first_graph_search(problem)
        t1 = time.time()
        print('A*Box Solver took {:.6f} seconds'.format(t1-t0))
        SokobanPuzzleWorker.print_solution(goal_node)
        return SokobanPuzzleWorker.parse_goal_node(goal_node)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def replace_str_index(text: str, index: int, replacement: str):
    '''
    Repace the string with a char at given index.

    Parameters
    ----------
    text : str
        Original string.
    index : int
        Index to replace.
    replacement : str
        Single character.

    Returns
    -------
    str
        Replaced string.

    '''
    return f'{text[:index]}{replacement}{text[index+1:]}'


def replace_str_2d(text: str, index: int, replacement: str):
    '''
    Replace the string (in 2D addressing mode) with given char.
    Index starts at (0, 0).

    NOTICE: This function have side-effects, which means it changes original list.

    Parameters
    ----------
    text : list
        List of string.
    index : tuple
        Tuple of index, representing x and y.
    replacement : str
        Single character.

    Returns
    -------
    str
        Replaced string.

    '''
    text[index[1]] = replace_str_index(text[index[1]], index[0], replacement)
    return text
