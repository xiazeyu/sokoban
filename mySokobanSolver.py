
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
import copy


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11262141, 'Tian-Ching', 'Lan'), (11398299, 'Zeyu', 'Xia') ]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

actions_offset = [[-1,0,'h'], [1,0,'h'], [0,-1,'v'], [0,1,'v']]
# Left, Right, Up, Down; v: vertical, h: horizontal

def taboo_cells(warehouse, returnType = "str"):
    '''  
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
    taboo = []
    corner = []
    exploded = []
    frontier = [warehouse.worker]

    while frontier:
        current = frontier[0]
        exploded.append(current)
        
        wall_counter = {'v': 0, 'h': 0}
        
        for new_pos, new_dir in [((current[0] + offsetx, current[1] + offsety),
                                 direction) for offsetx, offsety, direction in actions_offset]:
            
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
                if (((cell_x-1, cell_y) not in warehouse.walls # along a left-side wall
                    and (cell_x+1, cell_y) not in warehouse.walls) # along a right-side wall
                    or (cell_x, cell_y) in warehouse.targets): # cell is a target
                    
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
                if (((cell_x, cell_y-1) not in warehouse.walls # along a down-side wall
                    and (cell_x, cell_y+1) not in warehouse.walls) # along a up-side wall
                    or (cell_x, cell_y) in warehouse.targets): # cell is a target
                    
                    continuous_taboo = False
                    break
            
            if continuous_taboo:
                for cell_x in range(min(corner_a[0], corner_b[0]) + 1, max(corner_a[0], corner_b[0])):
                    taboo.append((cell_x, cell_y))
                    
    returned = str(warehouse).replace("$"," ").replace("."," ").replace("@"," ").replace("!"," ").replace("*"," ")
    returned = returned.split('\n')
    
    for cell in taboo:
        replace_str_2d(returned, cell, 'X')
    
    if returnType == "str":
        return '\n'.join(returned)
    elif returnType == "list":
        return taboo


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes


    def __init__(self, warehouse):
        self.initial = warehouse
        self.taboo_cells = taboo_cells(warehouse, "list")

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        acts=['Up','Left','Down','Right']
        (x,y) = state.worker
        if (x - 1 , y) in state.walls or ((x-1 , y) in state.boxes and (x - 2,y) in state.walls + state.boxes + self.taboo_cells):
            acts.remove('Left')
        if (x + 1 , y) in state.walls or ((x+1 , y) in state.boxes and (x +2,y) in state.walls + state.boxes + self.taboo_cells):
            acts.remove('Right')
        if (x , y-1) in state.walls or ((x , y-1) in state.boxes and (x,y-2) in state.walls + state.boxes + self.taboo_cells):
            acts.remove('Up')
        if (x , y+1) in state.walls or ((x , y+1) in state.boxes and (x,y+2) in state.walls + state.boxes + self.taboo_cells):
            acts.remove('Down')
        return acts
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        for box in state.boxes:
            if box not in state.targets:
                return False
        return True
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        next_state = copy.copy(state)
        (x,y) = state.worker
        if action == 'Left':
            next_state.worker = (x-1,y)
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == next_state.worker:
                    next_state.boxes[index] =(boxX -1 , boxY)
        elif action == 'Up':
            next_state.worker = (x,y-1)  

            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == next_state.worker:
                    next_state.boxes[index] =(boxX, boxY-1)
        elif action == 'Down':
            next_state.worker = (x,y+1)
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == next_state.worker:
                    next_state.boxes[index] =(boxX , boxY+1)
        elif action == 'Right':
            next_state.worker =(x+1,y)
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == next_state.worker:
                    next_state.boxes[index] =(boxX +1 , boxY)
        return next_state
    
    def h(self, n):
        #to be done
        return 0
    
    
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
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
    
    ##         "INSERT YOUR CODE HERE"
    

    problem = SokobanPuzzle(warehouse)
    currentNode = search.Node(problem.initial)

    for planedAct in action_seq :
        if planedAct in problem.actions(currentNode.state):
            currentNode = currentNode.child_node(problem, planedAct)
        else:
            return "Impossible"
        
    return (currentNode.state.__str__())


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
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
    problem = SokobanPuzzle(warehouse)

    sol_ts = search.breadth_first_graph_search(problem)  # graph search version

    print (sol_ts)
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def replace_str_index(text, index, replacement):
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

def replace_str_2d(text, index, replacement):
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