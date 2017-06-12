from operator import itemgetter
from itertools import groupby




##########################################################################################
# 
#  Functions Defination Begins!!
#
##########################################################################################

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:

        return values

    values[box] = value

    if len(value) == 1:

        assignments.append(values.copy())
    return values



def update_grid(grid, value):
    """
     update box values of '.' with '123456789'
    """
    for l in grid.keys():

        if grid[l] == '.':

            grid[l] = value

    return grid



def cross(A, B):
    """
    Cross product of elements in A and elements in B."
    pass
    """
    return [s+t for s in A for t in B]




def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    
    line = '+'.join(['-'*(width*3)]*3)
    
    for r in rows:
        
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    #pass


'''
def grid_diagonal(a, b):
    """
      creates a list of boxes in the diagonal
      Args: a = 'ABCDEFGHI', b = '123456789'

      Returns: list of diagonal boxes
    """

    dg = []

    if len(a) == len(b):

        for l in range(0, len(a)):

            dg.append(a[l] + b[l])

    if len(dg) != 0:

        return dg

    else:

        print("\tError, Empty\n")


def reverse_string(s):
    """
      produces a reverse string from an input of string

    """
    return "".join(s[i] for i in range(len(s) - 1, -1, -1))
'''





    
def grid_values(from_string=None, from_dict=None):
    
    """
    Build the Sudoku grid from either string or dictionary

    Parameters
    ----------
    from_string : str[81], string with initial values from top left corner to bottom right corner.
        e.g., '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    from_dict : dict, dictionary with box coordinate as key (e.g. 'A1') and a digit or '.' as value.

    Returns
    -------
    dict, a grid in dictionary form with the boxes as keys (e.g. 'A1') and a digit or '123456789' as value
    """
    
    if from_string is not None:

        assert(isinstance(from_string, str))

        assert(from_dict is None)

        assert (len(from_string) == 81)

        grid = dict(zip(boxes, list(from_string)))


    if from_dict is not None:

        assert(isinstance(from_dict, dict))

        assert(from_string is None)

        assert (len(from_dict) == 81)

        grid = from_dict.copy()

    for box in boxes:

        if grid[box] == '.':

            grid[box] = '123456789'

    return grid 
 





## Eliminate Strategy Method
def eliminate(values):
    """Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single
    value, eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    """
     One found single values now, Remove this value from its peers(cols, rows, 3x3 box)
     procedure:
     1) create/find the peers
     2) loop through peers
     3) find value in peers and eliminate them i.e remove value from box value which is a string i.e ns = s.replace(val,'')
    """
    #creating a list of single value boxes
    one_digits = [box for box in values.keys() if len(values[box]) == 1]

    #Now remove  single digit box value from peers
    for box in one_digits:

        digit = values[box]

        for peer in peers[box]:

            #values[peer] = values[peer].replace(digit,'')

            ## Assign values before return
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    
    return values

    #pass



## Only Choice Strategy Method
def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:

        for val in '123456789':

            unitboxes = [box for box in unit if val in values[box]]

            if len(unitboxes) == 1:

                for ubox in unitboxes:

                    values = assign_value(values, ubox, val)
                    ##values[unitboxes[0]] = val

                
    return values


'''
## naked Twins Strategy Method
def naked_twins(values):

    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
 
    # Find all instances of naked twins
    # List of Boxes with Matching(Length == 2 & same Value)

    ## List of Boxes with Matching(Length == 2 & same Value)
    twin_values = []

    twin_values = [box for box in values.keys() if len(values[box]) == 2]

    naked_twins = [[box1, box2] for box1 in twin_values for box2 in peers[box1] \
                   if set(values[box1]) == set(values[box2])]

    for i in range(len(naked_twins)):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])

        peers_int = peers1 & peers2

        for peer_val in peers_int:
            if len(values[peer_val]) > 2:
                for rm_val in values[box1]:
                    values = assign_value(values, peer_val, values[peer_val].replace(rm_val, ''))
                    #values[peer_val] = values[peer_val].replace(rm_val, '')

    return reduce_puzzle(values)

    #pass

'''

def naked_twins(values):
    '''
    Identify naked twins and remove their individual digits from unit peers.
    '''

    for unit in unitlist:

        candidates = [(box, values[box]) for box in unit if len(values[box]) == 2]

        if len(candidates) >= 2:

            sorted_candidates = sorted(candidates, key=itemgetter(1))

            paired_candidates = groupby(sorted_candidates, key=itemgetter(1))

            for digits, candidates in paired_candidates:

                boxes = [candidate[0] for candidate in candidates]

                if len(boxes) == 2:

                    for box in unit:

                        if box not in boxes:

                            for digit in digits:

                                if digit in values[box] and len(values[box]) > 1:

                                    values = assign_value(values, box, values[box].replace(digit, ''))
                                    # values[box] = values[box].replace(digit, '')

    return values

    #pass





def reduce_puzzle(values, eliminate_strategy=True, only_choice_strategy=True, naked_twin_strategy=True):
    """
     Applies  3 strategies:
     1) Elimination strategy
     2) one Choice Strategy
     3) Naked Twins ( to solve Naked Twin Sudoku problems)
     
     Apply all 3 strategies by Default!

    : Input Parameters: 3 strategy flags
                        values: sudoku puzzle values as grid
    :return: dictionary with reduced values
    """
    stalled = False
    
    while not stalled:

        # Check how many boxes have a determined value

        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        if eliminate_strategy == True:

            # Use the Eliminate Strategy
            values = eliminate(values)

        if only_choice_strategy == True:
            
            # Use the Only Choice Strategy
            values = only_choice(values)

        if naked_twin_strategy == True:
            
            # use naked Twins strategy( for naked twin problems)
            values = naked_twins(values)
            
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):

            return False

    return values

    #pass


def search(values):
    """ 
    Using depth-first search and propagation, try all possible values.
    
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if values is False:

        return False ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):

        return values ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:

        new_sudoku = values.copy()

        new_sudoku[s] = value

        attempt = search(new_sudoku)

        if attempt:

            return attempt


    #pass




def solve(grid, puzzle_as_string=True):
    """
    Find the solution to a Sudoku grid.
    
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        
        puzzle_as_string = True; Default is True, see soultion_test.py where inputs
                                  sudoku puzzles are given as dictionaries already
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    puzzle_values = []; 
    
    if puzzle_as_string == True:
       
       puzzle_values = grid_values(from_string=grid) # create dictionary {box: value, ...}
        ##values = grid_values(grid)
    else:
        
       puzzle_values = grid_values(from_dict=grid) # puzzle already in dictionary i.e []
    
    
    return search(puzzle_values)

    #pass




########################################################################################
##
##  Variables/Data Structures
##
########################################################################################

assignments = []


rows = 'ABCDEFGHI'

cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]

column_units = [cross(rows, c) for c in cols]

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

## Create Diagonal units

main_diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))]]

off_diagonal_units = [[rows[i] + cols[::-1][i] for i in range(len(rows))]]  

#rev_cols = reverse_string(cols)
#diag2_units = [[rows[i] + rev_cols[i] for i in range(len(rows))]]
#diag_units = diag1_units + diag2_units
#diag_units = [grid_diagonal(rows, cols)] + [grid_diagonal(rows,  reverse_string(cols))]

diagonal_units = main_diagonal_units  +  off_diagonal_units

#Choose If diagonal Sudoku or Traditional Sudoku
diagonal_sudoku = True  ## Final solution is a diagonal sudoku so default is True

if diagonal_sudoku:
    
    unitlist = row_units + column_units + square_units + diagonal_units
    
else:
    unitlist = row_units + column_units + square_units


units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)





########################################################################################
##
##  Main Begins
##
########################################################################################

if __name__ == '__main__':
    
    # easy Sudoku
    #suduku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

    #Hadder Sudoku
    #sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    
    
    sudoku_grid = {"G7": "2345678", "G6": "1236789", "G5": "23456789", "G4": "345678",
                    "G3": "1234569", "G2": "12345678", "G1": "23456789", "G9": "24578",
                    "G8": "345678", "C9": "124578", "C8": "3456789", "C3": "1234569",
                    "C2": "1234568", "C1": "2345689", "C7": "2345678", "C6": "236789",
                    "C5": "23456789", "C4": "345678", "E5": "678", "E4": "2", "F1": "1",
                    "F2": "24", "F3": "24", "F4": "9", "F5": "37", "F6": "37", "F7": "58",
                    "F8": "58", "F9": "6", "B4": "345678", "B5": "23456789", "B6":
                    "236789", "B7": "2345678", "B1": "2345689", "B2": "1234568", "B3":
                    "1234569", "B8": "3456789", "B9": "124578", "I9": "9", "I8": "345678",
                    "I1": "2345678", "I3": "23456", "I2": "2345678", "I5": "2345678",
                    "I4": "345678", "I7": "1", "I6": "23678", "A1": "2345689", "A3": "7",
                    "A2": "234568", "E9": "3", "A4": "34568", "A7": "234568", "A6":
                    "23689", "A9": "2458", "A8": "345689", "E7": "9", "E6": "4", "E1":
                    "567", "E3": "56", "E2": "567", "E8": "1", "A5": "1", "H8": "345678",
                    "H9": "24578", "H2": "12345678", "H3": "1234569", "H1": "23456789",
                    "H6": "1236789", "H7": "2345678", "H4": "345678", "H5": "23456789",
                    "D8": "2", "D9": "47", "D6": "5", "D7": "47", "D4": "1", "D5": "36",
                    "D2": "9", "D3": "8", "D1": "36"
                  }



    sudoku_values = [];  # final results of the sudoku
    
    string_input_format = True;  ## default puzzle too solve is as a string, see solution_test.py
    
    if  string_input_format:
        
        ## Are we doing a diagonal sudoku puzzle?
        if diagonal_sudoku == True:
            
           sudoku_values = solve(diag_sudoku_grid)
           
        else:
            
           sudoku_values = solve(sudoku_grid)
    else:
       
       ## Are we doing a diagonal sudoku puzzle?
        if diagonal_sudoku == True:
            
           sudoku_values = solve(diag_sudoku_grid, False)
           
        else:
            
           sudoku_values = solve(sudoku_grid, False)
    
    
    print("\n *** SUDOKU PUZZLE****\n")
     
    display(sudoku_grid)
    
    print("\n *** SUDOKU RESULT****\n")
    
    display(sudoku_values)
    
    print("\n", sudoku_values)
    
    
    ## Visualise sudoku
    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:

        pass

    except:

        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
