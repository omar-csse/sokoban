
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
from sokoban import Warehouse
from operator import eq, add, sub
import math
from search import astar_graph_search


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [ (9976353, 'Omar', 'Alqarni'), (9497862, 'Mohammed', 'Alsaeed'), (10368493, 'Sohyb', 'Qasem') ]

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

    def __init__(self, initial, warehouse, goal=None):
        
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse
        self.possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def value(self, state):
        return 1

    def result(self, state, action):
        return state[0] + action[0], state[1] + action[1]
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        for move in self.possible_moves:
            new_move = self.result(state, move)
            if new_move not in self.warehouse.boxes and new_move not in self.warehouse.walls:
                yield move

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_new_coords(position, x, y):
    if position is 'Right': x = x + 1
    elif position is 'Left': x = x - 1
    elif position is 'Up': y = y - 1
    else: y = y + 1

    return x, y

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
    x, y = warehouse.worker

    # loop through the actions in the list
    for position in action_seq:

        # get the new x and y based on the action postion
        newx, newy = get_new_coords(position, x, y)

        # check if the new postion (move) is a wall, if so return impossible to move
        if (newx, newy) in warehouse.walls:
            return 'Impossible'
        # else if the new postion (move) is a box
        elif (newx, newy) in warehouse.boxes:
            # check if the future postion of the box after shifting it is wall or another box, 
            # if so then it is impossible to move. because it hits a wall or a box
            if get_new_coords(position, newx, newy) in (warehouse.walls or warehouse.boxes):
                return 'Impossible'
            
            # otherwise, it is possible to shif the box. hence, update the box position to the new one
            warehouse.boxes.remove((newx, newy))
            warehouse.boxes.append( (get_new_coords(position, newx, newy)) )

        # update the x and y
        x = newx
        y = newy

    warehouse.worker = x, y
    return str(warehouse)


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
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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
    def h(n):
        return math.sqrt ( (n.state[1] - dst[1])**2 + (n.state[0] - dst[0])**2 )
    
    dst = (dst[1], dst[0])
    node = astar_graph_search(SokobanPuzzle(warehouse.worker, warehouse, dst), h)
    
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
    
    raise NotImplementedError()

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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -