
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11262141, 'Tian-Ching', 'Lan'), (11398299, 'Zeyu', 'Xia') ]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
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
    ##         "INSERT YOUR CODE HERE"    
    exploded = []
    corner = []
    taboo = []
    frontier = [warehouse.worker]
    while frontier:
        (currentX,currentY) = frontier[0]
        exploded.append((currentX,currentY))
        couldGo = [(currentX,currentY-1), (currentX,currentY+1),(currentX-1,currentY), (currentX+1,currentY)]
        #up,down,left,right
        sideToWall = 0
        for (actionX,actionY) in couldGo:
            if (actionX,actionY) in frontier or (actionX,actionY) in exploded:
                continue
                #if already in frontier or exploded, remove to avoid loop
            if (actionX,actionY) in warehouse.walls:
                sideToWall += 1
                #check if walk to wall
            else:
                frontier.append((actionX,actionY))
            #if not wall or expold    
        if sideToWall >=2 and (currentX,currentY) not in warehouse.targets:
            corner.append((currentX,currentY))
            
        frontier.remove((currentX,currentY))
    taboo = corner
    
    for ((corner1X,corner1Y),(corner2X,corner2Y)) in itertools.combinations_with_replacement(corner,2):
        #[((corner1X,corner1Y),(corner2X,corner2Y)), ((corner1X,corner1Y),(corner3X,corner3Y))]
        if corner1X == corner2X:
            isTaboo = True
            for checkWallY in range(min(corner1Y,corner2Y)+1, max(corner1Y,corner2Y)) :
                if (((corner1X+1,checkWallY) not in warehouse.walls and (corner1X-1,checkWallY) not in warehouse.walls)) or (corner1X,checkWallY) in warehouse.targets or (corner1X,checkWallY) in warehouse.boxes:
                    isTaboo = False
                    break
            if isTaboo:
                for checkWallY in range(min(corner1Y,corner2Y)+1, max(corner1Y,corner2Y)):
                    taboo.append((corner1X,checkWallY))
        elif  corner1Y == corner2Y:
            isTaboo = True
            for checkWallX in range(min(corner1X,corner2X)+1, max(corner1X,corner2X)) :
                if ((checkWallX, corner1Y+1) not in warehouse.walls and (checkWallX,checkWallY-1) not in warehouse.walls) or (checkWallX,checkWallY+1) in warehouse.targets or (checkWallX,checkWallY) in warehouse.boxes:
                    isTaboo = False
                    break
            if isTaboo:
                for checkWallX in range(min(corner1X,corner2X)+1, max(corner1X,corner2X)):
                    taboo.append((checkWallX,corner1X))
    returned = warehouse.__str__()              
    for (tabooX,tabooY) in taboo:
        returned = returned[:(warehouse.ncols+1) * tabooY + tabooX] + 'X' + returned[(warehouse.ncols+1) * tabooY + tabooX + 1:]
    returned = returned.replace("."," ")
    returned = returned.replace("@"," ")
    returned = returned.replace("$"," ")
    returned = returned.replace("*"," ")
    
    
    return returned
    
    
    

    
    

    
    
    # print(returned) 


   

    
        



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

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """

        acts=['Up','Left','Down','Right']
        (x,y) = state.worker
        if (x - 1 , y) in state.walls or ((x-1 , y) in state.boxes and (x - 2,y) in state.walls + state.boxes):
            acts.remove('Left')
        if (x + 1 , y) in state.walls or ((x+1 , y) in state.boxes and (x +2,y) in state.walls + state.boxes):
            acts.remove('Right')
        if (x , y-1) in state.walls or ((x , y-1) in state.boxes and (x,y-2) in state.walls + state.boxes):
            acts.remove('Up')
        if (x , y+1) in state.walls or ((x , y+1) in state.boxes and (x,y+2) in state.walls + state.boxes):
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
        (x,y) = state.worker
        if action == 'Left':
            state.worker = (x-1,y)
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == state.worker:
                    state.boxes[index] =(boxX -1 , boxY)
        elif action == 'Up':
            state.worker = (x,y-1)  
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == state.worker:
                    state.boxes[index] =(boxX, boxY-1)
        elif action == 'Down':
            state.worker = (x,y+1)
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == state.worker:
                    state.boxes[index] =(boxX , boxY+1)
        elif action == 'Right':
            state.worker =(x+1,y)
            for index, (boxX, boxY) in  enumerate(state.boxes):
                if (boxX, boxY) == state.worker:
                    state.boxes[index] =(boxX +1 , boxY)

        return state
    
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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

