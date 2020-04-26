
'''
    2020 CAB320 Sokoban assignment
The functions and classes defined in this module will be called by a marker script.
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.
You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the
interface and results in a fail for the test of your code.
This is not negotiable!
'''

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files
import search
import sokoban
from operator import eq, add, sub
import math
import itertools


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    '''
    return [ (9976353, 'Omar', 'Alqarni'), (9497862, 'Mohammed', 'Alsaeed'), (10368493, 'Sohyb', 'Qasem') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    '''
    Helper functions used through out the solution
    '''

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_new_coords(action, x, y):
    if action == 'Right': x = x + 1
    elif action == 'Left': x = x - 1
    elif action == 'Up': y = y - 1
    elif action == 'Down' : y = y + 1
    return x, y


def get_coords(move):
    if move == 'Right': return (1, 0)
    elif move == 'Left': return (-1, 0)
    elif move == 'Up': return (0, -1)
    elif move == 'Down': return (0, 1)


def get_move(action):
    if action == (1, 0): return 'Right'
    elif action == (-1, 0): return 'Left'
    elif action == (0, -1): return 'Up'
    elif action == (0, 1): return 'Down'


def get_prev_coords(action, x, y):
    if action == (1, 0): return x-1, y
    elif action == (-1, 0): return x+1, y
    elif action == (0, -1): return x, y+1
    elif action == (0, 1): return x, y-1


def do_move(a, b):
    return (a[0] + b[0], a[1] + b[1])


def get_goal_state(warehouse):
    return str(warehouse).replace('@', ' ').replace('$', ' ').replace('.', '*')


def get_heuristics_hashtable(warehouse):

    lines = warehouse.__str__().split("\n")

    allspaces = list(sokoban.find_2D_iterator(lines, " "))
    box_target = list(sokoban.find_2D_iterator(lines, "*"))
    player_target = list(sokoban.find_2D_iterator(lines, "!"))
    allcells = [*[warehouse.worker], *warehouse.boxes, *warehouse.targets, *allspaces, *box_target, *player_target]

    lookuptable = dict()
    for i, cell in enumerate(allcells):
        for i in range(len(warehouse.targets)):
            cell_target =  cell + (i, )
            lookuptable[cell_target] = manhattan_distance(cell, warehouse.targets[i])

    return lookuptable


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse
    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    # "INSERT YOUR CODE HERE"    
    warehouse = str(warehouse)  
    remove_cells = ["@", "$"]
    targets_cells = ["!", "*", "."]
    wall_cell = "#"
    taboo_cell = "X"

    #function to itirate through target cell and return true if similar 
    def targets_check(cell):
        if (cell in targets_cells) or (cell in taboo_cell):
            return True
        return False

    #Function use to pass two varables and remove cells from the warehouse
    def replace_cells(cells_to_remove, warehaouse_str):
        for i in range (0, len(cells_to_remove)):
            warehaouse_str = warehaouse_str.replace(cells_to_remove[i], ' ')
        return warehaouse_str

    #Check if cell still inside a warehouse
    def check_insidewarehouse(i):
        if (inside_warehouse == 1):
            for a in range (1, warehouse_width):
                if (warehouse[i+a] == '\n'):
                    return 0
                if (warehouse[i+a] != ' '):
                    return 1       
        return 0

    #Check if a cell is taboo
    def check_taboocell(i, cells):
        #compare up/down right and left walls
        if (inside_warehouse == 1) and (warehouse[i] in ' '):
            #check right and left sides for walls
            if (warehouse[i+1] in cells) or (warehouse[i-1] in cells):
                #check up and down sides for walls
                if (warehouse[i+warehouse_width] in  cells) or (warehouse[i-warehouse_width] in cells):
                    warehouse[i] = taboo_cell

    #Check if a cell is taboo == X
    def check_taboocell_corners(i, cells):

        #compare up/down right and left walls
        if (inside_warehouse == 1) and (warehouse[i] in ' '):
            a = 0
            along_wall = True
            along_wall_opposite = True
            taboo_cell_postion = []
            #check right and left sides for taboo cell
            while ((along_wall == True) or (along_wall_opposite == True)) and (warehouse[i-1] in cells):
                
                if (warehouse[i-warehouse_width+a] != wall_cell):
                    along_wall = False

                if (warehouse[i+warehouse_width+a] != wall_cell):
                    along_wall_opposite = False

                if (warehouse[i+a] in (wall_cell)) or (warehouse[i+a] in targets_cells):
                    taboo_cell_postion.clear()
                    return taboo_cell_postion
                elif (warehouse[i+a] in cells):
                    return taboo_cell_postion


                taboo_cell_postion.append(i+a)
                a+=1

            a = 0
            along_wall = True
            along_wall_opposite = True
            taboo_cell_postion = []    
                       
            #This second loop find the taboo cells between corners in a horizontal pattern    
            while ((along_wall == True) or (along_wall_opposite == True)) and (warehouse[i-warehouse_width] in cells):
                #Break if search exceeded the bounders
                if (i+(warehouse_width*a) > len(warehouse)):
                    break

                #Make sure along corners wall cell in both left and right direction
                if (warehouse[i+(warehouse_width*a) + 1] != wall_cell):
                    along_wall = False
                if (warehouse[(i+(warehouse_width*a)) - 1] != wall_cell):
                    along_wall_opposite = False

                #If other corner exist return the postion of all new virtical taboo cells if not return empty list
                if (warehouse[i+(warehouse_width*a)] in wall_cell) or (warehouse[i+(warehouse_width*a)] in targets_cells):
                    taboo_cell_postion.clear()
                    return taboo_cell_postion
                elif (warehouse[i+(warehouse_width*a)] in cells):
                    return taboo_cell_postion

                #Loop through and add each cell that could be taboo
                taboo_cell_postion.append(i+(warehouse_width*a))
                a+=1    

        return 0
                    
    #Remove both $,@ square from warehouse 
    warehouse = replace_cells(remove_cells, warehouse)

    #Find width of warehouse and save value in warehouse_width
    warehouse_width = 0
    while (1):
        if warehouse[warehouse_width] == '\n':
            warehouse_width+=1
            break
        warehouse_width+=1

    #Convert string to list to modifiy the warehouse
    warehouse = list(warehouse)

     # We have two condition 
     # 1-when inside warehaouse = 0 then cell is outside warehouse pre-enterning
     # 2-whenn inside warehouse = 1 then condisiton inside warehouse 
    inside_warehouse = 0
    
    #Rule 1 - Loop through the warehouse and find the taboo cells
    for i in range (warehouse_width, len(warehouse) - warehouse_width):
        #Check if cell is inside warehouse
        inside_warehouse = check_insidewarehouse(i)

        #Call function to check if a cell is taboo
        check_taboocell(i, wall_cell)

        #Check if cell enter the warehouse
        if (warehouse[i] == wall_cell) and ((warehouse[i+1] == ' ') or targets_check(warehouse[i+1])) and (inside_warehouse == 0):
            inside_warehouse = 1

    #Rule 2 - Loop through the warehouse and find the taboo cells between two Corners
    inside_warehouse = 0
    for i in range (warehouse_width, len(warehouse) - warehouse_width):
        #Check if cell is inside warehouse
        inside_warehouse = check_insidewarehouse(i)

         #Call function to check if a cell is taboo (between corners)
        list_taboocells = check_taboocell_corners(i, taboo_cell)
        if list_taboocells != 0:
            for n in list_taboocells:
                warehouse[n] = taboo_cell
                
        #Check if cell enter the warehouse
        if (warehouse[i] == wall_cell) and ((warehouse[i+1] == ' ') or targets_check(warehouse[i+1])) and (inside_warehouse == 0):
            inside_warehouse = 1

    #Convert back the list to string
    warehouse = ''.join(warehouse)
    
    #Remove target cells
    warehouse = replace_cells(targets_cells, warehouse)
    return warehouse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.
    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    def __init__(self, warehouse, allow_taboo_push=False, macro=False, push_costs=None):
        
        self.initial = str(warehouse)
        self.taboo_cells = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split('\n'), "X"))
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro
        self.possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.goal = get_goal_state(warehouse)
        self.heuristic_hashtable = get_heuristics_hashtable(warehouse)
        self.push_costs = push_costs
        self.box_index = None
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """

        warehouse = sokoban.Warehouse()
        warehouse.extract_locations(state.split("\n"))
        actions = []
        
        if self.macro:
            for box in warehouse.boxes:
                for move in self.possible_moves:
                    new_box_position = do_move(box, move)
                    new_worker_position = box[1] + (move[1] * -1), box[0] + (move[0] * -1)
                    can_go = can_go_there(warehouse, new_worker_position)
                    if can_go and new_box_position not in warehouse.walls and \
                        new_box_position not in warehouse.boxes and new_box_position not in self.taboo_cells:
                        actions.append(( (box[1], box[0]), get_move(move)))
        else:
            for move in self.possible_moves:
                new_worker_position = do_move(warehouse.worker, move)
                if new_worker_position not in warehouse.walls:
                    if new_worker_position not in warehouse.boxes:
                        actions.append(get_move(move))
                    else:
                        new_box_position = do_move(new_worker_position, move)
                        if new_box_position not in warehouse.walls and new_box_position not in warehouse.boxes:
                            if self.allow_taboo_push is True:
                                actions.append(get_move(move))
                            elif new_box_position not in self.taboo_cells: 
                                actions.append(get_move(move))
        
        return actions

    def result(self, state, action):

        warehouse = sokoban.Warehouse()

        if self.macro:
            warehouse.extract_locations(state.split('\n'))       
            box = action[0][1], action[0][0]
            moveCoords = get_coords(action[1])
            warehouse.worker = box
            self.box_index = warehouse.boxes.index(box)
            warehouse.boxes[self.box_index] = (do_move(box, moveCoords))
            return str(warehouse)
        else:
            warehouse = sokoban.Warehouse()
            warehouse_updated, box_index = check_elem_action(state, action)
            self.box_index = box_index
            warehouse.extract_locations(warehouse_updated.split("\n"))
            return str(warehouse)

    def goal_test(self, state):
        winning_state = state.replace('@', ' ')
        return self.goal == winning_state

    def path_cost(self, c, state1, action, state2):

        if self.push_costs is not None and self.box_index is not None:
            path_cost = self.push_costs[self.box_index]
            self.box_index = None
            return path_cost

        return c + 1

    def h(self, node):

        warehouse = sokoban.Warehouse()
        warehouse.extract_locations(node.state.split("\n"))
        heuristics = [self.heuristic_hashtable[ (*box,i) ] for i, box in enumerate(warehouse.boxes)]
        return min(heuristics)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action(wh, action):

    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(wh.__str__().split("\n"))
    x, y = warehouse.worker
    box_index = None

    newx, newy = get_new_coords(action, x, y)
    if (newx, newy) in warehouse.walls:
        return 'Impossible'
    elif (newx, newy) in warehouse.boxes:
        if get_new_coords(action, newx, newy) in (warehouse.walls or warehouse.boxes):
            return 'Impossible'
        
        box_index = warehouse.boxes.index((newx, newy))
        warehouse.boxes[box_index] = get_new_coords(action, newx, newy)

    x = newx
    y = newy
    warehouse.worker = x, y
    return warehouse.__str__(), box_index

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def check_elem_action_seq(wh, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object
    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    # "INSERT YOUR CODE HERE"
    # get the current x and y postion of te worker (player)
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(wh.__str__().split("\n"))
    x, y = warehouse.worker

    # loop through the actions in the list
    for action in action_seq:

        # get the new x and y based on the action postion
        newx, newy = get_new_coords(action, x, y)
        # check if the new postion (move) is a wall, if so return impossible to move
        if (newx, newy) in warehouse.walls:
            return 'Impossible'
        # else if the new postion (move) is a box
        elif (newx, newy) in warehouse.boxes:
            # check if the future postion of the box after shifting it is wall or another box, 
            # if so then it is impossible to move. because it hits a wall or a box
            if get_new_coords(action, newx, newy) in (warehouse.walls or warehouse.boxes):
                return 'Impossible'
            
            # otherwise, it is possible to shif the box. hence, update the box action to the new one
            box_index = warehouse.boxes.index((newx, newy))
            warehouse.boxes[box_index] = get_new_coords(action, newx, newy)

        # update the x and y
        x = newx
        y = newy

    warehouse.worker = x, y
    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object
    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    # "INSERT YOUR CODE HERE"

    astar_sol = search.astar_graph_search(SokobanPuzzle(warehouse))
    if astar_sol == [] or astar_sol is None: 
        return 'Impossible'
    else:
        return astar_sol.solution()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class CanGoThere(search.Problem):

    '''
    Check if can go from position A to position B
    '''

    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.warehouse = warehouse
        self.goal = goal
        self.possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
    def value(self, state):
        return 1

    def result(self, state, action):
        return state[0] + action[0], state[1] + action[1]
    
    def actions(self, state):
        for move in self.possible_moves:
            new_move = self.result(state, move)
            if new_move not in self.warehouse.boxes and new_move not in self.warehouse.walls:
                yield move

    def h(self, node):
        return math.sqrt((node.state[1] - self.goal[1])**2 + (node.state[0] - self.goal[0])**2)


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object
    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    ## "INSERT YOUR CODE HERE"

    dst = (dst[1], dst[0])
    node = search.astar_graph_search(CanGoThere(warehouse.worker, warehouse, dst))
    
    return node is not None
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 
    @param warehouse: a valid Warehouse object
    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    # "INSERT YOUR CODE HERE"
    
    astar_sol = search.astar_graph_search(SokobanPuzzle(warehouse, macro=True))
    if astar_sol == [] or astar_sol is None: 
        return 'Impossible'
    else:
        return astar_sol.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)
    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    astar_sol = search.astar_graph_search(SokobanPuzzle(warehouse, macro=False, push_costs=push_costs))
    if astar_sol == [] or astar_sol is None: 
        return 'Impossible'
    else:
        return astar_sol.solution()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -