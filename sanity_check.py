
'''

Quick "sanity check" script to test your submission 'mySokobanSolver.py'

This is not an exhaustive test program. It is only intended to catch major
syntactic blunders!

You should design your own test cases and write your own test functions.

Although a different script (with different inputs) will be used for 
marking your code, make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse


try:
    from fredSokobanSolver import taboo_cells, solve_weighted_sokoban, check_elem_action_seq
    print("Using Fred's solver")
except ModuleNotFoundError:
    from mySokobanSolver import taboo_cells, solve_weighted_sokoban, check_elem_action_seq, my_team
    print("Using submitted solver")

    
def test_taboo_cells():
    datasets = [
["./warehouses/warehouse_01.txt",
'''####  
#X #  
#  ###
#   X#
#   X#
#XX###
####  '''],
["./warehouses/taboo_test_01.txt",
'''####  
#XX#  
## ###
#X  X#
#X  X#
#X ###
####  '''],
["./warehouses/taboo_test_02.txt",
'''   # # # # #  
 ##X#X#X#X# # 
#XXXXXXXXXXXX#
#XX#X#X#X#X#X#
### # # # # # '''],
["./warehouses/taboo_test_03.txt",
'''########
#X     #
########'''],
["./warehouses/taboo_test_04.txt",
'''########
#XXXXXX#
#X     #
#X     #
#X    X#
########'''],
    ]
    for index, (warehouse, expected_answer) in enumerate(datasets):
        wh = Warehouse()
        wh.load_warehouse(warehouse)
        answer = taboo_cells(wh)
        fcn = test_taboo_cells    
        print('<<  Testing {} >>'.format(fcn.__name__))
        if answer==expected_answer:
            print(fcn.__name__, f' passed for {index}!  :-)\n')
        else:
            print(fcn.__name__, f' failed for {index}!  :-(\n')
            print('Expected ');print(expected_answer)
            print('But, received ');print(answer)

def test_check_elem_action_seq():
    datasets = [
["./warehouses/warehouse_01.txt",
['Right', 'Right','Down'],
'''####  
# .#  
#  ###
#*   #
#  $@#
#  ###
####  '''],
["./warehouses/warehouse_01.txt",
['Right', 'Right','Right'],
'Impossible'],
]
    for index, (warehouse, input, expected_answer) in enumerate(datasets):
        wh = Warehouse()
        wh.load_warehouse(warehouse)
        answer = check_elem_action_seq(wh, input)
        print(f'<<  check_elem_action_seq, test {index}>>')
        if answer==expected_answer:
            print(f'Test {index} passed!  :-)\n')
        else:
            print(f'Test {index} failed!  :-(\n')
            print('Expected ');print(expected_answer)
            print('But, received ');print(answer)

def test_solve_weighted_sokoban():
    datasets = [
["./warehouses/warehouse_01.txt",
['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 
'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 
'Right', 'Right', 'Right', 'Right', 'Right', 'Right'],
431],
]
    for index, (warehouse, expected_answer, expected_cost) in enumerate(datasets):
        wh = Warehouse()
        wh.load_warehouse(warehouse)
        # first test
        answer, cost = solve_weighted_sokoban(wh)
        print('<<  test_solve_weighted_sokoban >>')
        if cost==expected_cost:
            print(' Cost as expected!  :-)\n')
        else:
            print(f'Your cost = {cost}, expected cost = {expected_cost}')

        my_final = check_elem_action_seq(wh, answer)
        expected_final = check_elem_action_seq(wh, expected_answer)
        
        if my_final==expected_final:
            print(' Answer as expected!  :-)\n')
        else:
            print('unexpected answer!  :D\n')
            print('Expected ');print(expected_answer)
            print('But, received ');print(answer)
            print('Expected final ');print(expected_final)
            print('But, received final ');print(my_final)
            print('Check that you pushed the right box onto the left target!')

if __name__ == "__main__":
    print(my_team())  # should print your team

    test_taboo_cells() 
    test_check_elem_action_seq()
    test_solve_weighted_sokoban()
