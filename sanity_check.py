
'''

Quick "sanity check" script to test your submission 'mySokobanSolver.py'

This is not an exhaustive test program. It is only intended to catch major
syntactic blunders!

You should design your own test cases and write your own test functions.

Although a different script (with different inputs) will be used for 
marking your code, make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse
import time
import timeout_decorator

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
    print('<<  test_solve_weighted_sokoban >>')
    datasets = [
["./warehouses/warehouse_01.txt",
['Down', 'Left', 'Up', 'Right', 'Right', 'Right', 'Down',
 'Left', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right',
 'Up', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Down',
 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left',
 'Down', 'Left', 'Up', 'Up'],
 33],
["./warehouses/warehouse_8a.txt",
['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 
'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 
'Right', 'Right', 'Right', 'Right', 'Right', 'Right'],
431],
["./warehouses/warehouse_09.txt",
['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left',
 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up',
 'Right', 'Down', 'Right', 'Down', 'Down', 'Left', 'Up',
 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right',
 'Up', 'Left'],
396],
["./warehouses/warehouse_47.txt",
['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left',
 'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left',
 'Left', 'Left', 'Left', 'Up', 'Up', 'Right', 'Right',
 'Up', 'Right', 'Right', 'Right', 'Right', 'Down', 'Left',
 'Up', 'Left', 'Down', 'Down', 'Up', 'Up', 'Left', 'Left',
 'Down', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right',
 'Right', 'Right', 'Right', 'Right', 'Down', 'Right',
 'Right', 'Up', 'Left', 'Left', 'Left', 'Left', 'Left',
 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Up', 'Right',
 'Right', 'Right', 'Up', 'Right', 'Down', 'Down', 'Up',
 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down',
 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', 'Left',
 'Down', 'Left', 'Left', 'Up', 'Right', 'Right'] ,
179],
["./warehouses/warehouse_81.txt",
['Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Left',
 'Down', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right',
 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Up',
 'Left', 'Left', 'Down', 'Right', 'Up', 'Right', 'Up',
 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Down',
 'Right', 'Down', 'Down', 'Left', 'Down', 'Down', 'Right',
 'Up', 'Up', 'Up', 'Down', 'Left', 'Left', 'Up', 'Right'] ,
376],
["./warehouses/warehouse_5n.txt",
'Impossible',
None],
["./warehouses/warehouse_07.txt",
['Up', 'Up', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left',
 'Down', 'Down', 'Right', 'Up', 'Down', 'Right', 'Down',
 'Down', 'Left', 'Up', 'Down', 'Left', 'Left', 'Up', 'Left',
 'Up', 'Up', 'Right'],
26],
["./warehouses/warehouse_147.txt",
['Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down',
  'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down',
  'Right', 'Down', 'Down', 'Left', 'Down', 'Left', 'Left',
  'Up', 'Up', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right',
  'Up', 'Up', 'Left', 'Left', 'Left', 'Down', 'Left', 'Up',
  'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right',
  'Right', 'Right', 'Down', 'Right', 'Right', 'Right', 'Up',
  'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 'Left', 'Left',
  'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right',
  'Up', 'Left', 'Down', 'Left', 'Up', 'Up', 'Left', 'Up',
  'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Left',
  'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down',
  'Down', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Up',
  'Right', 'Up', 'Left', 'Left', 'Left', 'Down', 'Left', 'Up',
  'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right',
  'Right', 'Down', 'Right', 'Down', 'Right', 'Right', 'Up',
  'Left', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down',
  'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Right',
  'Right', 'Right', 'Right', 'Right', 'Right', 'Up', 'Right',
  'Right', 'Down', 'Down', 'Left', 'Down', 'Left', 'Left', 'Up',
  'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Left', 'Up',
  'Left', 'Left'],
521],
]
    for index, (warehouse, expected_answer, expected_cost) in enumerate(datasets):
        print(f'case {index}, {warehouse}')
        wh = Warehouse()
        wh.load_warehouse(warehouse)
        t0 = time.time()
        answer = solve_weighted_sokoban(wh)
        t1 = time.time()
        print('took {:.6f} seconds'.format(t1-t0))


        if answer == 'Impossible':
            if expected_answer == 'Impossible':
                print('Answer as expected, Impossible!  :-)\n')
            else:
                print(f'Your answer = {answer}, expected answer = {expected_answer}')
            continue

        answer, cost = answer
        if answer == expected_answer:
            print('Answer as expected, wow!  :-)\n')
        else:
            print('Steps are not the same, but don\'t worries!')

        if cost==expected_cost:
            print('Cost as expected!  :-)\n')
        else:
            print(f'Your cost = {cost}, expected cost = {expected_cost}')

        my_final = check_elem_action_seq(wh, answer)
        expected_final = check_elem_action_seq(wh, expected_answer)
        
        if my_final==expected_final:
            print('Final as expected!  :-)\n')
        else:
            print('unexpected answer!  :D\n')
            print('Expected ');print(expected_answer)
            print('But, received ');print(answer)
            print('Expected final ');print(expected_final)
            print('But, received final ');print(my_final)

def test_solve_weighted_sokoban_speed():
    datasets = [
        "01",
        "01_a",
        "03",
        "03_impossible",
        "07",
        "09",
        "101",
        "103",
        "105",
        "107",
        "109",
        "11",
        "111",
        "113",
        "115",
        "117",
        "119",
        "121",
        "123",
        "125",
        "127",
        "129",
        "13",
        "131",
        "133",
        "135",
        "137",
        "139",
        "141",
        "143",
        "145",
        "147",
        "149",
        "15",
        "151",
        "153",
        "155",
        "157",
        "159",
        "161",
        "163",
        "165",
        "167",
        "169",
        "17",
        "171",
        "173",
        "175",
        "177",
        "179",
        "181",
        "183",
        "185",
        "187",
        "189",
        "19",
        "191",
        "193",
        "195",
        "197",
        "199",
        "201",
        "203",
        "205",
        "21",
        "23",
        "25",
        "27",
        "29",
        "31",
        "33",
        "35",
        "37",
        "39",
        "41",
        "43",
        "45",
        "47",
        "49",
        "51",
        "53",
        "55",
        "57",
        "59",
        "5n",
        "61",
        "63",
        "65",
        "67",
        "69",
        "6n",
        "71",
        "73",
        "75",
        "77",
        "79",
        "81",
        "83",
        "85",
        "87",
        "89",
        "8a",
        "8b",
        "91",
        "93",
        "95",
        "97",
        "99",
    ]
    result = {}
    for index, dataset in enumerate(datasets):
        print('---------------------------')
        print(f'case {index}, {dataset}')
        wh_path=f'./warehouses/warehouse_{dataset}.txt'
        t0 = time.time()
        try:
            _perform_sokoban_speed_test(wh_path)
        except:
            print('Fail')
            result[dataset] = '-1'
            continue
        t1 = time.time()
        result[dataset] = t1-t0
        print('{:.6f} seconds'.format(t1-t0))
        print('---------------------------')

    print(result)

@timeout_decorator.timeout(seconds=360)
def _perform_sokoban_speed_test(warehouse):
    wh = Warehouse()
    wh.load_warehouse(warehouse)
    solve_weighted_sokoban(wh)


if __name__ == "__main__":
    print(my_team())  # should print your team

    test_solve_weighted_sokoban_speed()

    # test_taboo_cells() 
    # test_check_elem_action_seq()
    # test_solve_weighted_sokoban()
