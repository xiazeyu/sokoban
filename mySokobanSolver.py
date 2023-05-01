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

import copy
import functools
import itertools
import math
import operator
import search
import sokoban

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

_actions_offset: list[list[int, int, str]] = [
    [-1, 0, 'h'], [1, 0, 'h'], [0, -1, 'v'], [0, 1, 'v']]
# Left, Right, Up, Down; v: vertical, h: horizontal
_moves: dict[tuple[int, int]] = {
    'Left': (-1, 0), 'Right': (1, 0), 'Up': (0, -1), 'Down': (0, 1)}
# (x,y) = (column,row)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team() -> list[tuple[int, str, str]]:
    """
    Returns
    -------
    list[tuple[int, str, str]]
        The list of the team members of this assessment submission as a list of
        triplet of the form (student_number, first_name, last_name).

    """
    return [(11262141, 'Tian-Ching', 'Lan'), (11398299, 'Zeyu', 'Xia')]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def _taboo_cells_solver(warehouse: sokoban.Warehouse) -> list[tuple[int, int]]:
    """
    The solver for taboo cells puzzles.

    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 

    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.

    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.

    Parameters
    ----------
    warehouse : sokoban.Warehouse
        a Warehouse object with the worker inside the warehouse.

    Returns
    -------
    list[tuple[int, int]]
        A list of tuple contains the coordinates of the cells identified as taboo cells.

    """

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
                # add new cell to frontier
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
        if corner_a not in taboo or corner_b not in taboo:
            # if either corner is not taboo, then the cells between them are not taboo
            continue
        if corner_a[0] == corner_b[0]:
            cell_x = corner_a[0]
            # x fixed to corner_a[0]
            # test if in-between cells are along a wall, without a target, continuously
            continuous_taboo = True

            for cell_y in range(min(corner_a[1], corner_b[1]) + 1, max(corner_a[1], corner_b[1])):
                if (((cell_x-1, cell_y) not in warehouse.walls  # along a left-side wall
                    and (cell_x+1, cell_y) not in warehouse.walls)  # along a right-side wall
                        or (cell_x, cell_y) in warehouse.targets + warehouse.walls):  # cell is a target or wall

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
                        or (cell_x, cell_y) in warehouse.targets + warehouse.walls):  # cell is a target or wall

                    continuous_taboo = False
                    break

            if continuous_taboo:
                for cell_x in range(min(corner_a[0], corner_b[0]) + 1, max(corner_a[0], corner_b[0])):
                    taboo.append((cell_x, cell_y))

    # deduplicate
    return list(set(taboo))


def replace_str_index(text: str, index: int, replacement: str) -> str:
    """
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

    """
    return f'{text[:index]}{replacement}{text[index+1:]}'


def replace_str_2d(text: str, index: tuple[int, int], replacement: str) -> list[str]:
    """
    Replace the string (in 2D addressing mode) with given char.
    Index starts at (0, 0).

    Parameters
    ----------
    text : str
        List of string.
    index : tuple[int, int]
        Tuple of index, representing x and y.
    replacement : str
        Single character.

    Returns
    -------
    list[str]
        Replaced string array.

    """
    text[index[1]] = replace_str_index(text[index[1]], index[0], replacement)
    return text


def taboo_cells(warehouse: sokoban.Warehouse) -> str:
    """
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

    Parameters
    ----------
    warehouse : sokoban.Warehouse
        a Warehouse object with the worker inside the warehouse.

    Returns
    -------
    str
        A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.

    """
    taboo = _taboo_cells_solver(warehouse)

    returned = str(warehouse).replace("$", " ").replace(
        ".", " ").replace("@", " ").replace("!", " ").replace("*", " ")
    returned = returned.split('\n')

    for cell in taboo:
        replace_str_2d(returned, cell, 'X')

    return '\n'.join(returned)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class State:

    def __init__(self, worker: tuple[int, int] = None, boxes: list[tuple[int, int]] = None) -> None:
        self.worker = worker
        self.boxes = copy.copy(boxes)

    def copy(self, worker: tuple[int, int] = None, boxes: list[tuple[int, int]] = None):
        """
        Generate a independent copy of the state.

        Parameters
        ----------
        worker : tuple[int, int], optional
            The location of worker. The default is None.
        boxes : list[tuple[int, int]], optional
            The location of boxes. The default is None.

        Returns
        -------
        clone : State
            The cloned state.

        """
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
    """
    Calculate the Manhattan distance between two points.

    Parameters
    ----------
    a : tuple[int, int]
        first cell location.
    b : tuple[int, int]
        second cell location.

    Returns
    -------
    int
        The Manhattan distance between two points.

    """
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
        self.taboo_cells = _taboo_cells_solver(warehouse)
        self.weights = warehouse.weights
        self.targets = warehouse.targets
        self.walls = warehouse.walls
        self.ncols = warehouse.ncols
        self.nrows = warehouse.nrows

    def in_range(self, cell: tuple[int, int]) -> bool:
        """
        Check if a cell is in the warehouse.

        Parameters
        ----------
        cell : tuple[int, int]
            The cell to be checked.

        Returns
        -------
        bool
            True if the cell is in the warehouse, False otherwise.

        """
        # x < self.ncols, y < self.nrows
        return 0 <= cell[0] < self.ncols and 0 <= cell[1] < self.nrows

    def actions(self, state: State) -> list[tuple[int, str]]:
        """
        Return the list of boxes' actions that can be executed in the given state.

        Each action consists of a box index and a direction.

        Parameters
        ----------
        state : State
            The state to be checked.

        Returns
        -------
        list[tuple[int, str]]
            The list of boxes' actions that can be executed in the given state.

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
                assert self.in_range((x+dx, y+dy))
                # if not self.in_range((x+dx, y+dy)):
                #     # proability of this happening is very low
                #     # a box cannot be pushed out of the warehouse
                #     moves.pop(name)
                #     continue
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
                if self.worker_cost(state)[x-dx][y-dy] == math.inf:
                    # a box cannot be pushed into a cell that is unreachable by the worker
                    moves.pop(name)
                    continue

            all_moves.extend([(idx, name) for name in moves])

        return all_moves

    def goal_test(self, state: State) -> bool:
        """
        Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.

        Parameters
        ----------
        state : State
            The state to be checked.

        Returns
        -------
        bool
            True if the state is a goal, False otherwise.

        """
        for box in state.boxes:
            if box not in self.targets:
                return False
        return True

    def path_cost(self, c: int, state1: State, action: tuple[int, str], state2: State = None) -> int:
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.

        Parameters
        ----------
        c : int
            The cost to get up to state1.
        state1 : State
            The state to be checked.
        action : tuple[int, str]
            The action to be checked.
        state2 : State, optional
            The following state. This option is not used. The default is None.

        Returns
        -------
        int
            The cost of a solution path that arrives at state2 from state1 via action.

        """

        assert action in self.actions(state1)
        # assert state2 == self.result(state1, action)

        box_idx, direction = action

        dx, dy = _moves[direction]
        box_start = state1.boxes[box_idx]
        worker_end_x, worker_end_y = (box_start[0]-dx, box_start[1]-dy)
        cost = self.worker_cost(state1)
        worker_dist_cost = cost[worker_end_x][worker_end_y]

        return c + worker_dist_cost + 1 + self.weights[box_idx]

    def result(self, state: State, action: tuple[int, str]) -> State:
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        Parameters
        ----------
        state : State
            The state to be checked.
        action : tuple[int, str]
            The action to be checked.

        Returns
        -------
        State
            The state that results from executing the given action in the given state.

        """
        assert action in self.actions(state)

        box_idx, direction = action

        next_worker = state.boxes[box_idx]
        dx, dy = _moves[direction]
        next_box = (next_worker[0]+dx, next_worker[1]+dy)
        next_state = state.copy(worker=next_worker)
        next_state.boxes[box_idx] = next_box

        return next_state

    def value(self, state: State) -> int:
        """
        For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value.

        This method is not used in this problem.

        It will raise an exception if called.

        Parameters
        ----------
        state : State
            The state to be checked.

        Raises
        ------
        NotImplementedError
            This method is not implemented.

        Returns
        -------
        int
            The value of the given state.

        """
        raise NotImplementedError()

    def parse_goal_node(self, goal_node: search.Node) -> tuple[list[str], int]:
        """
        Export the full steps represented by a specific goal node.
        For example, goal node could be obtained by calling 
        goal_node = breadth_first_tree_search(problem)

        Parameters
        ----------
        goal_node : search.Node
            The goal node to be parsed.

        Returns
        -------
        (tuple[list[str], int])
            A tuple of (path, cost) where path is a list of actions.

        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        answer = []
        if goal_node is None:
            return 'Impossible'

        cost = goal_node.path_cost

        for node in goal_node.path():
            # print(node)
            if node.action is not None:
                parent_state = node.parent.state
                _, action_direction = node.action
                ldx, ldy = _moves[action_direction]

                start = parent_state.worker
                end_box = node.state.worker
                end = end_box[0]-ldx, end_box[1]-ldy
                cost_map = self.worker_cost(parent_state)
                assert len(cost_map) == self.ncols
                assert len(cost_map[0]) == self.nrows
                mid_path = []
                assert self.in_range(start)
                assert self.in_range(end)
                while end != start:
                    # find the direction of the move
                    for direction in _moves:
                        dx, dy = _moves[direction]
                        if not self.in_range((end[0]-dx, end[1]-dy)):
                            # out of range
                            continue
                        assert cost_map[end[0]][end[1]] != math.inf
                        if cost_map[end[0]-dx][end[1]-dy] == cost_map[end[0]][end[1]] - 1:
                            # find the direction
                            mid_path.append(direction)
                            assert cost_map[end[0]-dx][end[1]-dy] != math.inf
                            end = (end[0]-dx, end[1]-dy)
                            break
                answer.extend(reversed(mid_path))
                answer.append(action_direction)

        return answer, cost

    def worker_cost(self, state: State) -> list[list[int]]:
        """
        Return a 2D array of the cost of moving the worker to each position.

        This method is memoized.

        Parameters
        ----------
        state : State
            The state to be checked.

        Returns
        -------
        list[list[int]]
            A 2D array of the cost of moving the worker to each position.

        """
        dist_func = search.memoize(self._dist_map, slot='worker_cost')
        start = state.worker
        return dist_func(state, start)

    def print_worker_cost(self, state: State) -> None:
        """
        Print the worker cost map.

        Parameters
        ----------
        state : State
            The state to be checked.

        Returns
        -------
        None
            None.

        """
        wc = self.worker_cost(state)
        print('y\\x', end='\t')
        for x in range(self.ncols):
            print(x, end='\t')
        print()
        for y_index in range(self.nrows):
            print(y_index, end='\t')
            for x_index in range(self.ncols):
                # print((x_index, y_index), end='\t')
                print(wc[x_index][y_index], end='\t')
            print()

    def _dist_map(self, state: State, start: tuple[int, int]) -> list[list[int]]:
        """
        Return a 2D array of the cost of moving the worker to each position.

        Using Dijkstra's algorithm.

        Parameters
        ----------
        state : State
            The state to be checked.
        start : tuple[int, int]
            The start position.

        Returns
        -------
        list[list[int]]
            A 2D array of the cost of moving to each position from the start position.

        """
        # initialize
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
                if not self.in_range((x + dx, y + dy)):
                    # out of range
                    continue
                if (x + dx, y + dy) in self.walls or (x + dx, y + dy) in state.boxes:
                    # wall or box
                    continue
                if final[x + dx][y + dy]:
                    # already in final
                    continue
                if dist[x + dx][y + dy] > dist[x][y] + 1:
                    # update
                    dist[x + dx][y + dy] = dist[x][y] + 1
                    final[x + dx][y + dy] = True
                    Q.append(((x + dx, y + dy), dist[x + dx][y + dy]))

        return dist
    
    def no_heuristic(self, node: search.Node) -> int:
        # no heuristic
        # this becomes uniform_cost_search
        return 0

    def h(self, node: search.Node) -> int:
        """
        Heuristic for goal state.

        h = manhattan distance from each box to the closest goal.

        Parameters
        ----------
        node : search.Node
            The node to be checked.

        Returns
        -------
        int
            The heuristic value.

        """
        return self.no_heuristic(node)
        return sum(self._box_dist(node.state, box) for box in node.state.boxes)
        # [list(zip(boxes, _)) for _ in itertools.permutations(goals)]
        # state = node.state
        # costs = [0]
        # tempCombination = {}
        # for targetX, targetY in self.targets:
        #     for index, (boxX, boxY) in enumerate(state.boxes):
        #         tempCombination[(targetX, targetY), (boxX, boxY)] = (
        #             abs(targetX - boxX) + abs(targetY - boxY)) * self.weights[index]
        # # print(tempCombination)
        # Combinations = [[]]
        # for i in range(len(self.targets) - 1):
        #     for (target, box) in tempCombination.keys():
        #         placed = False
        #         for index, combinationList in enumerate(Combinations):
        #             Found = False
        #             for (CombinationTarget, CombinationBox) in combinationList:
        #                 if target == CombinationTarget or box == CombinationBox:
        #                     Found = True
        #                     break
        #             if not Found:
        #                 Combinations[index].append((target, box))
        #                 costs[index] += tempCombination[(target, box)]
        #                 placed = True
        #                 break

        #         if not placed:
        #             Combinations.append([(target, box)])
        #             costs.append(tempCombination[(target, box)])
        # return min(costs)


class SokobanPuzzleWorker(SokobanPuzzle):
    # Only for check_elem_action_seq and BFS test
    def actions(self, state: State) -> list[str]:
        """
        Return the list of boxes' actions that can be executed in the given state.

        NOTE: this action DID NOT filter out the actions that will lead to a taboo state.

        Each action consists of a box index and a direction.

        Parameters
        ----------
        state : State
            The state to be checked.

        Returns
        -------
        list[tuple[int, str]]
            The list of boxes' actions that can be executed in the given state.

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

    def path_cost(self, c: int, state1: State, action: str, state2: State = None) -> int:
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.

        Parameters
        ----------
        c : int
            The cost to get up to state1.
        state1 : State
            The state to be checked.
        action : tuple[int, str]
            The action to be checked.
        state2 : State, optional
            The following state. This option is not used. The default is None.

        Returns
        -------
        int
            The cost of a solution path that arrives at state2 from state1 via action.

        """
        assert action in self.actions(state1)
        x, y = state1.worker
        dx, dy = _moves[action]
        for index, (box_x, box_y) in enumerate(state1.boxes):
            if (box_x, box_y) == (x+dx, y+dy):
                return c + self.weights[index] + 1

        return c + 1

    def result(self, state: State, action: str) -> State:
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        Parameters
        ----------
        state : State
            The state to be checked.
        action : tuple[int, str]
            The action to be checked.

        Returns
        -------
        State
            The state that results from executing the given action in the given state.

        """
        assert action in self.actions(state)
        x, y = state.worker
        dx, dy = _moves[action]
        next_state = state.copy(worker=(x+dx, y+dy))
        for index, (box_x, box_y) in enumerate(state.boxes):
            if (box_x, box_y) == next_state.worker:
                next_state.boxes[index] = (box_x + dx, box_y + dy)
        return next_state

    def parse_goal_node(goal_node: search.Node) -> tuple[list[str], int]:
        """
        Export the full steps represented by a specific goal node.
        For example, goal node could be obtained by calling 
        goal_node = breadth_first_tree_search(problem)

        Parameters
        ----------
        goal_node : search.Node
            The goal node to be parsed.

        Returns
        -------
        (tuple[list[str], int])
            A tuple of (path, cost) where path is a list of actions.

        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        answer = []
        if goal_node is None:
            return 'Impossible'

        cost = goal_node.path_cost
        for node in goal_node.path():
            if node.action is not None:
                answer.append(node.action)
        return answer, cost

    def h(self, node: search.Node) -> int:
        """
        Heuristic for goal state.

        h = manhattan distance from each box to the closest goal.

        Parameters
        ----------
        node : search.Node
            The node to be checked.

        Returns
        -------
        int
            The heuristic value.

        """
        # [list(zip(boxes, _)) for _ in itertools.permutations(goals)]
        state = node.state
        costs = [0]
        tempCombination = {}
        for targetX, targetY in self.targets:
            for index, (boxX, boxY) in enumerate(state.boxes):
                tempCombination[(targetX, targetY), (boxX, boxY)] = (
                    abs(targetX - boxX) + abs(targetY - boxY)) * self.weights[index]
        # print(tempCombination)
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


def check_elem_action_seq(warehouse: sokoban.Warehouse, action_seq: list[str]) -> str:
    """
    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    Parameters
    ----------
    warehouse : sokoban.Warehouse
        a valid Warehouse object.
    action_seq : list[str]
        a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    Returns
    -------
    str
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()

    """

    problem = SokobanPuzzleWorker(warehouse)
    state = problem.initial

    for planed_act in action_seq:
        if planed_act in problem.actions(state):
            state = problem.result(state, planed_act)
        else:
            return "Impossible"

    return str(warehouse.copy(worker=state.worker, boxes=state.boxes))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse: sokoban.Warehouse) -> tuple[list[str], int]:
    """
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.

    Parameters
    ----------
    warehouse : sokoban.Warehouse
        a valid Warehouse object.

    Returns
    -------
    (tuple[list[str], int])
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C
    str
        If puzzle cannot be solved 
            return 'Impossible', None

    """
    mode = 'astar_worker'

    if mode == 'bfs_worker':
        problem = SokobanPuzzleWorker(warehouse)
        goal_node = search.breadth_first_graph_search(problem)
        print('BFS Worker Solver')
        return SokobanPuzzleWorker.parse_goal_node(goal_node)

    elif mode == 'astar_worker':
        problem = SokobanPuzzleWorker(warehouse)
        goal_node = search.astar_graph_search(problem)
        print('A* Worker Solver')
        return SokobanPuzzleWorker.parse_goal_node(goal_node)

    if mode == 'bfs_box':
        problem = SokobanPuzzle(warehouse)
        goal_node = search.breadth_first_graph_search(problem)
        print('BFS Box Solver')
        return problem.parse_goal_node(goal_node)

    if mode == 'astar_box':
        problem = SokobanPuzzle(warehouse)
        goal_node = search.astar_graph_search(problem)
        print('A* Box Solver')
        return problem.parse_goal_node(goal_node)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
