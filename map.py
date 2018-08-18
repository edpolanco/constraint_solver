"""
    Map coloring constraint propagation class for the
    country of Australia.

    Author: Ed Polanco
    Email:  ed.polanco@outlook.com
"""

from solver import ConstraintSolver
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle

class Australia(ConstraintSolver):
    """
        Class for solving the Australian map coloring puzzle using constraint propagation.
        
        The objective is to color each region either red, green, or blue 
        in such a way that no neighboring regions have the same color. 
        
        This class inherits from 'ConstrainSolver' base class that uses 'elimination'
        and 'only_choice' algorithms to solve constraint problems. 

        Parameter
        ------------
        state: dict [default None]
            The initial state of the map.  
    """
    def __init__(self,state:dict = None):
        
        # *** domain variables ***
        # ================================== 
        # WA = Western Australia
        # NT = Northern Territory
        # SA = South Australia
        # QL = Queensland
        # NS = New South Wales
        # VT = Victoria
        self.__X_name = dict()
        self.__X_name['WA'] = 'Western Australia'
        self.__X_name['NT'] = 'Northern Territory'
        self.__X_name['SA'] = 'South Australia'
        self.__X_name['QL'] = 'Queensland'
        self.__X_name['NSW'] = 'New South Wales'
        self.__X_name['VT'] = 'Victoria'

        #domain variables codes        
        self.__X_map = ['WA','NT','SA','QL','NSW','VT']
        #-----------------------------------------
        
        #*** Domain values ***
        #=========================================
        # R = Red
        # B = Blue
        # G = Green
        self.__D_map_name = dict()
        self.__D_map_name['R'] = 'Red'
        self.__D_map_name['B'] = 'Blue'
        self.__D_map_name['G'] = 'Green'
        self.__D_map = 'RBG'
        #-----------------------------------------

        #*** Define Constraints *** 
        # Must be different color within constrain group
        #===============================================
        C = []

        #handle Western Australlia 
        C.append(['WA','NT','SA']) 

        #handle Northen Territory 
        C.append(['NT','SA','QL'])
        
        #handle South Australia 
        C.append(['SA','QL','NSW'])
        C.append(['SA','NSW','VT'])
 
        #create dictionary of all units that a given box is part of.
        C_groups = dict((x_, [c_ for c_ in C if x_ in c_]) for x_ in self.__X_map)

        #lets creat peer groups
        #create a dictionary to look up all the color constraint that a given country is part of.
        peers = dict((s, set(sum(C_groups[s],[]))-set([s])) for s in self.__X_map)    
        #------------------------------------------------------------------------------------------

        # lets create x and y cordinates to color paint circles on the Australia map.
        self.__map_color = dict()
        self.__map_color['WA'] = (135,300)
        self.__map_color['NT'] = (280,75)
        self.__map_color['SA'] = (380,260)
        self.__map_color['QL'] = (460,110)
        self.__map_color['NSW'] = (550,320)
        self.__map_color['VT'] = (435,380)

        #set our state
        self.__org_state = state
        new_state = self.state_setup(state)
        
        ConstraintSolver.__init__(self,state=new_state, X= self.__X_map, D=self.__D_map, C=C, peers= peers)

    def state_setup(self,state:dict=None):
        """
            Reads the initial state of the map and populates the 
            un-polulated regions with all the possible colors.

            Parameter
            ------------
            state: dict [default None]
                The initial state of the map.  
            
            Returns
            -----------
            Returns a state of the map where every region
            is populated by its given initial color or with all the
            possible colors. 
        """ 
        
        D_all = ''.join([d for d in self.__D_map]) 
        
        if state == None:
            state_ ={ x:D_all for x in self.__X_map} 
        else:
            state_ = dict()
            for x in self.__X_map:
                if x in state:
                    state_[x] = state[x]
                else:
                    state_[x] = D_all 
        
        return state_

    def display_state(self):
        """
            Displays an image of the Australia map with the current color(s) 
            for each region. 
        """ 
        self.display_map(self.state)

    def display_map(self, state:dict = None):
        """
            Displays an image of the Australia map with the current color(s) 
            for each region for the given 'state'.   

            Displays a blank map if 'state' is None. 

            Parameter
            ------------
            state: dict [default None]
                The current state of the map.  
        """     
        if state is not None:
            # Create a figure. Equal aspect so circles look circular
            _,ax = plt.subplots(1)
            ax.set_aspect('equal')

            color_code = {'R':'red','B':'blue','G':'green'}
            for key, value in state.items():
                y_shift = 0.0
                for c in value:
                    x = self.__map_color[key][0] 
                    y = self.__map_color[key][1]+ y_shift
                    circ = Circle( (x,y),10,color=color_code[c] )
                    ax.add_patch(circ)
                    y_shift +=20

        plt.axis("off")
        image = mpimg.imread("images/australia.jpg")
        plt.imshow(image)
        plt.show()
    
    def display_org_cmd(self):
        """ Print the original sudoku board as a 2-D grid in command line format.
        """
        for key, value in self.__org_state.items():    
            print("{0:<20}: {1:}".format(self.__X_name[key],  ",".join( [self.__D_map_name[c] for  c in value])  ) )

    def display_state_cmd(self):
        """ Print the current sudoku board as a 2-D grid in command line format.
        """
        for key, value in self.state.items():    
            print("{0:<20}: {1:}".format(self.__X_name[key],  ",".join( [self.__D_map_name[c] for  c in value])  ) )

    def display_org(self):
        """
            Displays an image of the Australia map with color(s) 
            for each region based on its initial state. 
        """
        self.display_map(self.__org_state)