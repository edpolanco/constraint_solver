"""
    Constraint propagation base solver abstract class

    Author: Ed Polanco
    Email:  ed.polanco@outlook.com
"""

from abc import ABC, abstractmethod,ABCMeta
    
class ConstraintSolver(ABC):
    """
        Constraint propagation base solver abstract class.
        Uses elimination and only choice to solve constraint propagation problem but can
        be modified to include other reduction algorithms.

        Parameters:
        ------------
        state: dict
            The initial state of the constraint problem we are trying to solve.  
            A key represents a variable and the value is either its assigned value or 
            the possible values for that variable.  
            
            ** A value must be represented by a 'char' character. 
                For example if the value is the color Blue then the 'B' or 'b'
                should be its value. 

        X: list
            A list of the state variables that can take on a value.

        C: list
            A list of list where state variables are combined by their respective constraint group.
            Each list item represents a constraint list group.  

        D: str
            List of domain variables
            
            ** values must be 1 character length 'char'
        
        peers: dict
            A dict where the keys are variables and the value is
            a list of contraint group that the variable is part of.
            We use this variable in the only choice algorithm. 
    """
    def __init__(self, state: dict, X: list, D:str, C: list, peers: dict ):
        
        #current state of problem
        self.__internal_state = state
        
        #a list of the problem domain variables that can take on a value
        self.__X = X

        #a characters string of the possible values that a our problem
        #domain variables can take
        self.__D = D

        #a list of list where each item represent a constraint group 
        self.__C = C

        #a dictionary where the keys are the problem X variables
        #  and values are a list of a constraint group.
        self.__peers = peers
        
        #flag to indicate if problem was solved.
        self.__solved = False

        #reduction functions list
        self.__reduce_funcs = []
        self.__reduce_funcs.append(self.__eliminate)
        self.__reduce_funcs.append(self.__only_choice)

        #lets count the number of times we call the search and reduction functions
        self.__reduce_count = 0
        self.__search_count = 0
    
    @abstractmethod 
    def display_state(self):
        """ Displays the current state of the constraint problem."""
        pass

    @abstractmethod 
    def display_org(self):
        """ Displays the original constraint problem."""
        pass

    @abstractmethod 
    def display_org_cmd(self):
        """ Displays the original constraint problem to the command line."""
        pass

    @abstractmethod 
    def display_state_cmd(self):
        """ Displays the current state of the constraint problem 
            suitable for the command line."""
        pass

    @property
    def state(self):
        """ Get constraint problem state as dict."""
        return self.__internal_state
    
    @property
    def reduce_count(self):
        """ The count of how many times the reduction function were called."""
        return self.__reduce_count
    
    @property
    def search_count(self):
        """ The count of how many times the search function was called."""
        return self.__search_count

    @property
    def unitlist(self):
        """ Get problem's constraints."""
        return self.__C
    
    @property
    def reduce_functions(self):
        """ Get list of reduction solving functions."""
        return self.__reduce_funcs

    @property
    def solved(self):
        """ Check if constraint problem was solved."""
        return self.__solved
    
    def __solved_units_count(self,state: dict):
        """" Return count of the number of variables solved
            in the given current state.
        """
        return len([item for item in state.keys() if len(state[item]) == 1])

    def __solved_units(self,state: dict):
        """" Returns the the number of solved units as list
             given the current state.
        """
        return [item for item in state.keys() if len(state[item]) == 1]

    def __unsolvable_units(self,state: dict):
        """ Returns true if we have at least ."""
        return len([item for item in state.keys() if len(state[item]) == 0]) > 0

    def assign_value(self,state: dict, item: str, new_val: str):
        """ Assigns value to a unit variable.
            
            Paramters:
            ----------
            state: dict
                The current state of the constraint problem
            
            item: str
                The unit variable we want to assign value to.
            
            new_val: str
                The new value to assign.
            
            Returns:
            ----------
            Returns the new state after assignment.
        """
        if state[item] != new_val:
            state[item] = new_val
        
        return state

    def __eliminate(self, state: dict):
        """
            Go through all the state items, and whenever there an item with a value,
            eliminate this value from the values of all its peers.

            Returns
            --------
            Returns the state after elimination. 
        """
        solved_values = self.__solved_units(state) 
        for item in solved_values:
            val = state[item]
            for peer in self.__peers[item]:
                self.assign_value(state,  peer,state[peer].replace(val,''))
        
        return state
        
    def __only_choice(self,state: dict):
        """
            Go through all constraints, and whenever there is a unit variable with a value that only fits 
            in one unit variable, assign the value to this unit.
            
            Returns
                --------
                Returns the state after only choice iteration. 
        """
        for unit in self.__C:
            for unit_val in self.__D:
                # dplaces = [item for item in unit if unit_val in state[item]]
                dplaces = []
                for item in unit:
                    if unit_val in state[item]:
                        dplaces.append(item)
                if len(dplaces) == 1:
                    self.assign_value(state, dplaces[0],unit_val)    
        
        return state
    
    def __reduce(self, state: dict):
        """
            Iterate the reduction functions list over the given state to decompose  
            the current state closer to a solution.  By default uses the 'eliminate' and
            'only_choice' algorithm but can modified by calling the 'reduce_functions' property.

            Returns:
            -------
            Returns false  if at some point, there is a variable 
            with no available values otherwise returns the current state
            after applying the reduction algorithms.
        """
        self.__reduce_count +=1
        stalled = False
        while not stalled:
            solved_values_before = self.__solved_units_count(state) 
            
            for fun in self.__reduce_funcs:
                state = fun(state)
            
            solved_values_after = self.__solved_units_count(state)
            stalled = solved_values_before == solved_values_after
            
            if self.__unsolvable_units(state):
                return False
        
        return state
        
    def __search(self, state: dict):
        """ Using depth-first search and propagation, try all possible values."""
        
        # First, reduce the state using the reduction functions
        state = self.__reduce(state)
        if state is False:
            return False ## Failed earlier
        if all(len(state[item]) == 1 for item in self.__X): 
            return state ## Solved!
        
        # Choose one of the unfilled unit variables with the fewest possibilities
        _,s = min((len(state[item]), item ) for item in self.__X if len(state[item]) > 1)
        
        # Now use recurrence to try to solve each one of the resulting states.  
        self.__search_count +=1
        for val in state[s]:
            new = state.copy()
            new_state = self.assign_value(new,s,val)
            attempt = self.__search(new_state)
            if attempt:
                return attempt

    def solve(self):
        """
            Attempts to find solution to constraint problem.
        
            Returns:
            ------------
                True if found solution false otherwise.
        """
        self.__reduce_count  = 0
        self.__search_count = 0
        attempt = self.__search(self.__internal_state)
        if attempt:
            self.__internal_state = attempt
            self.__solved = True
        
        return self.__solved