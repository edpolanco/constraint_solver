
# Project Goal
In this project I give a brief overview of the chapter “Constraint Satisfaction Problems”  from Russell and Norvig’s book Artificial Intelligence a Modern Approach (3rd Edition).  
I also implement in `python` two constraint propagation programs.  One   program solves Sudoku puzzles and the other solves the Australian map coloring problem.  

# What is Constraint Satisfaction?
A Constraint Satisfaction Problem (CSP) is a search problem that uses a factored representation for each state where each state has a defined set of variables with possible values. 
 With a CSP we solve the problem by finding a state where the defined variables have a value that satisfies all constraints.  The main idea of a CSP is to be more efficient and eliminate a large proportion of the search space.  A CSP differs from searching a space of states which uses domain-specific heuristics and then tests for goal states.        
The authors defined a CSP as having three components, X, D and C:
> *	X is a set of variables, {X1,...,Xn}.
> * D is a set of domains that is possible for each variable, {D1,...,Dn}.
> *	C is a set of constraints that explicitly state possible combinations of values, {v1,...,vk}. 

In its simplest form, a CSP has variables that have discrete and finite domains.  Map coloring problems and scheduling with limits are such examples.  
It is also common for a CSP to have continuous domains such as scheduling of experiments on the Hubble space telescope.  

CSPs have three main types of constraints:
>  1.	Unary constraints – Restricts the value of a single variable.
>  2.	Binary constraint – Relates to a constraint between two variables.
>  3.	Global constraint – Involves an arbitrary number of constraints, but it does not necessarily   mean all the variables.

# Constraint Propagation
When a CSP uses constraints to reduce the number of legal moves this is called constraint propagation.  Constraint propagation may be combined with a search algorithm or performed as a preprocessing step.  The underlying idea behind constraint propagation is local consistency. If each variable is treated as a node in a graph, then enforcing local consistency in each part of the graph will cause inconsistent values to be eliminated from the graph.  There are three types of local consistency:
> 1.	Node consistency – All the variable’s domain satisfy the variable’s unary constraints.
> 2.	Arc consistency – Every value in a variable’s domain satisfies the variable’s binary constraints.  
> 3.	Path consistency - Uses implicit constraints, on the binary constraints, that are inferred by looking at triples of variables. 


# CSPs and Search
Many CSPs cannot be solved strictly by inference and will require searching for a solution. One of the most effective search algorithms for CSPs is back-tracking.  In back-tracking, we search one variable at a time and then “backtrack” when a variable has no legal values to assign. We can also combine search and inference by using forward-checking.  Forward-checking establishes arc consistency after the search algorithm assigns a value to a variable.

# Implementing Constraint Propagation
Here I discuss implementing constraint propagation in `python` by developing programs for solving Sudoku puzzles and the Australian map coloring problem (described in section 6.1.1 of chapter six).  Our implementation has three modules:
>  1. `solver.py`:  Contains an abstract base class called `ConstraintSolver`, which defines two functions for reducing the problem using arc consistency and a function for searching for a solution when inference is not enough. 
    
>> * The first reduction function is an elimination algorithm that removes any variable in the constraint that has a singleton domain and then removes that value from the domains of the remaining variables.  The second reduction function is an only-choice algorithm that assigns a value to a variable when that value does not fit in any of the other variables.

>> * The search function is a depth-first recursive method that attempts to find a solution by choosing the variable with the least remaining values in its domain. It then iteratively assigns to this variable one of its domain values, and  calls the reduction functions to try and find a solution.  If a solution is found it returns this solved state, otherwise it returns false.

>> * The `ConstraintSolver` abstract class also has other properties and methods to take advantage of code reuse.  

> 2. `sudoku.py`:   The `sudoku.py` module has a class called `Sudoku` to solve Sudoku puzzles. The `Sudoku` class inherits from the `ConstraintSolver` abstract base class.  The `Sudoku` class maintains a list of variables for each box (a Sudoku board has 81 boxes) and domain values 1 through 9.   The class also defines global constraints for the various Sudoku constraints groups (i.e. rows, columns and squares).  We discuss more about the rules of Sudoku along with a demonstration on using the `Sudoko` class in the `sudoku.ipynb` jupyter notebook.    

> 3. `map.py`: The `map.py` module has a class called `Australia` to solve the Australian map coloring problem and also inherits from the `ConstraintSolver` base abstract class.  The `Australia` class has a list of variables for each region and domain values of red, blue and green.  The constraints for the class are that no neighboring regions have the same color.   In the `map.ipynb` jupyter we demonstrate using the `Australia` class.

