"""
    Sudoku constraint propagation class

    Author: Ed Polanco
    Email:  ed.polanco@outlook.com
"""

from solver import ConstraintSolver
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.table import Table
 
class Sudoku(ConstraintSolver):
    """
        Class for solving sudoku puzzle using constraint propagation.  
        Inherits from 'ConstrainSolver' base class that uses 'elimination'
        and 'only_choice' algorithms to solve constraint problems. 

        Parameter
        ------------
        grid: str
            A string representing a sudoku grid.
            Example board as string: '5.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3' 
            The '.' represents a blank cell.  The first character represnts the top left most cell and
            the second character the cell to the right of the top left most cell..etc.

            Its corresponding board would be as follows:
            5 . . |. . . |. . . 
            . . . |. . 6 |2 . . 
            . . 1 |. . . |. 7 . 
            ------+------+------
            . . 6 |. . 8 |. . . 
            3 . . |. 9 . |. . 7 
            . . . |6 . . |4 . . 
            ------+------+------
            . 4 . |. . . |8 . . 
            . . 5 |2 . . |. . . 
            . . . |. . . |. . 3 

        diagonal: bool [False]
            Add diagonal boxes as a constraint.
    """
    def __init__(self,grid:str, diagonal:bool = False):
        
        #represents the rows in a sudoku grid
        self.__rows = 'ABCDEFGHI'

        #represents the columns in a sudoku grid
        self.__cols = '123456789' 

        #create unit values variable to represent the possible values for sudoku cell 
        self.__unit_values = self.__cols

        #get all the box combinations in a sudoko grid (81 boxes)
        self.__boxes = self.__cross(self.__rows, self.__cols)

        #get all the row combinations boxes in a sudoko grid
        row_units = [ self.__cross(r, self.__cols) for r in self.__rows]

        #get all the column combinations boxes in a sudoko grid
        column_units = [self.__cross(self.__rows, c) for c in self.__cols]

        #get all the possible squares combination in sudoko grid
        square_units = [self.__cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        
        #combined all the sudoko unit into one list
        unitlist = row_units + column_units + square_units

        if diagonal:
            #get all the possible diagonal box combination in sudoko grid
            diagonal_units = self.__diagonal(self.__rows,self.__cols)
            unitlist += diagonal_units

        #create dictionary of all units that a given box is part of.
        box_groups = dict((s, [u for u in unitlist if s in u]) for s in self.__boxes)
        
        #create a dictionary to look up all the cells constraint that a given cell is part of.
        peers = dict((s, set(sum(box_groups[s],[]))-set([s])) for s in self.__boxes)
        
        # use this map to color sudoku table image.  maps box to a color.
        self.__display_table_map = self.__cross_cord(self.__rows, self.__cols)

        #mapping to color the cells of sudoku image table 
        self.__colors = ['blue', 'orange', 'green','red','purple','brown','pink','gray', 'cyan']
        self.__color_map = {}
        for square,color in zip(square_units, self.__colors):
            for s in square:
                self.__color_map[s] = color

        #initial state of sudoku board
        state = self.__grid_values(grid)
        if state == False:
            print("Error creating sudoku board")
            return

        ConstraintSolver.__init__(self,state=state, X= self.__boxes, D=self.__unit_values, C=unitlist, peers= peers)

        #let keep a copy of the original sudoku table
        self.__org_state = self.__grid_values(grid,False)

        #add naked twin function to reduction functions
        self.reduce_functions.append(self.naked_twins)

    def __cross(self,A, B):
        """Cross product of elements in A and elements in B."""
        return [s+t for s in A for t in B]

    def __cross_cord(self,A, B):
        """ Returns a dictionry of the every Sudoku cell as its keys
            and the value of its Sudoku cell coordinate. 

            For example cells: 'A1' = (0,0) and 'A2' = (0,1)
        """
        table_dict = {}
        for s_idx, s in enumerate(A):
            for t_idx, t in enumerate(B):
                table_dict[s+t] = (s_idx,t_idx)

        return table_dict

    def __diagonal(self,rows,cols):
        """ get diagonal elements from rows and cols """
        diag1 = [row + col for row,col in zip(rows,cols)]

        #reverse column elements
        diag2 = [row + col for row,col in zip(rows,cols[::-1])]

        return [diag1,diag2]

    def __grid_values(self,grid: str, non_val = True):
        """
            Convert sudoku grid string into a dict of {square: char}.
            
            Parameters
            -----------
            grid: str
                A sudoku grid in string form.
            
            non_val: Boolean [Default True]
                Flag to indicate how we populate empty cells.
                If True then populate empty with '123456789' otherwise populate
                with '.' char. 

            Returns:
            ----------
            Returns sudoku grid in dictionary form
            Where the keys are the boxes, i.e., 'A1' and the values are
            value in each box, i.e., '8'.
        """
        chars = []
        for c in grid:
            if c in self.__unit_values:
                chars.append(c)
            elif c == '.':
                if non_val:
                    chars.append(self.__unit_values)
                else:
                    chars.append('.')
            else:
                print("'{}' is not a valid sudoku board value.".format(c))
                return False

        # lets make sure we have 81 cells.
        if len(chars) != 81:
            print("This is not a valid sudoku board.")
            return False
        else:
            return dict(zip(self.__boxes, chars))
    
    def display_org_cmd(self):
        """ Print the original sudoku board as a 2-D grid in command line format.
        """
        self.__display(self.__org_state)

    def display_state_cmd(self):
        """ Print the current sudoku board as a 2-D grid in command line format.
        """
        self.__display(self.state)
    
    def __display(self,state: dict):
        """
            Display the values of board as a 2-D grid.
        
            Parameters
            ------------
            state: dict
                A sudoku board in dictionary form.
        """
        width = 1+max(len(state[s]) for s in self.__boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.__rows:
            print(''.join( state[r+c].center(width)+ ('|' if c in '36' else '')
                        for c in self.__cols))
            if r in 'CF': print(line)
    
    def __draw(self, state:dict):
        """
            Draw 2-D sudoku board as image.
        
            Parameter
            ------------
            state: dict
                A sudoku board in dictionary form.
        """
        _, ax = plt.subplots()
        ax.set_axis_off()
        tb = Table(ax, bbox=[0,0,1,1])

        width = height = 1.0 /9 


        for key in self.state.keys():
            # Add cells
            i,j = self.__display_table_map[key]
            tb.add_cell(i, j, width, height, text='{}'.format(state[key]), 
                        loc='center',facecolor= self.__color_map[key])

        ax.add_table(tb)
        plt.show()

    def display_state(self):
        """Draw 2-D sudoku board as image."""
        # self.__display(self.state)
        self.__draw(self.state)

    def display_org(self):
        """Draw 2-D sudoku board as image."""
        self.__draw(self.__org_state)

    def naked_twins(self,state:dict):
        """
            Eliminate values using the naked twins strategy.

            Parameter
            ------------
            state: dict
                A sudoku board in dictionary form.
            
            Returns:
            ----------
            Returns modified sudoku grid in dictionary form.
        """
        for unit in self.unitlist:

            #find any twins in unit and save as counter object
            all_pairs = Counter([state[box] for box in unit if len(state[box])==2])
            twins = [key for key,val  in all_pairs.items() if val == 2]

            #loop through twins and replace number in the other boxes
            for twin in twins:
                for num in twin:
                    for box in unit:
                        if twin != state[box]:
                            self.assign_value(state,box,state[box].replace(num,''))
            
        return state

def puzzles():
    """ Import a list of Sudoku puzzles from text file 
        and return it as a list

         Puzzles  credit:
            http://norvig.com/top95.txt
            http://norvig.com/hardest.txt
    """
    with open('sudoku_puzzles.txt') as file:  
        data = file.readlines()

    #remove all end of line characters
    return [i.replace('\n','') for i in data]

def puzzles_diagonal():
    """ Import a list of diagonal Sudoku puzzles from text file 
        and return it as a list

        Puzzles  credit:
            https://sudoku.cool/x-sudoku.php
    """
    with open('sudoku_puzzles_diagonal.txt') as file:  
        data = file.readlines()

    #remove all end of line characters
    return [i.replace('\n','') for i in data]