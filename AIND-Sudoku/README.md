# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: By applying the only choice strategy of looking at units(especially peers)
   with a box with one value and using this value to eliminate a value from
   the naked twins.

   Also constraint propagation solves the naked twins problem by extending
   the elimination of a single value to double values i.e instead of eliminating
   a single value, we are eliminating the pair unique to a given box from all its
   peers.
   Infact by applying Naked Twins strategy in addition to Elimination and Only Choice
   strategies we are further reducing the number of possibilities thus
   constraining the possible solution space.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal Sudoku problem?
A: The addition of these diagonal entries as peers to a given Soduku box
   increases the constraint on not accepting solutions that do not satisfy
   the diagonal constraint in addition to the other constraints.
   These two diagonal constraints(one for each diagonal) help reduce the number
   of possible solutions i.e help propagate the constraints on the possible
   solutions just as the other constraints.
   These 2 additional diagonals(in diagonal Sudoku) units to the list of units
   increases the constraints and thus allows the constraint propagation to
   become more efficient at solving the Sudoku puzzle.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

