"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    ##raise NotImplementedError

    ## Dummy evaluation

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):

        return float('-inf')

    #If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):

        return float('inf')

    ## can the player improve their score?
    own_moves = len(game.get_legal_moves(player))
    
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(own_moves - opp_moves)




def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    #raise NotImplementedError

    ## Dummy evaluation

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):

        return float('-inf')

    #If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):

        return float('inf')

    ## can the player improve their score?
    return float(len(game.get_legal_moves(player)))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError

    ## Dummy evaluation

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):

        return float('-inf')

    #If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):

        return float('inf')

    ## can the player improve their score?
    return float(len(game.get_legal_moves(player)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """


        self.time_left = time_left
        
  
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        # We want to keep track of the best move so far
        best_move = (-1, -1)
        

        ## Now lets find the best move using Minimax Algorithm
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:

            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move



    def minimax(self, game, depth, maximizing_player=True):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        maximizing_player: bool
            Determines which player is playing so we return the correct score
             

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        self.time_expired()


       
        legal_moves = game.get_legal_moves(game.active_player)

        
        # Terminating State
        # Are there any legal moves left for us to play? 
        # If not, forfeit the game by return (-1, -1)!
        if not legal_moves or depth <= 0:

            return (-1, -1)


        ## For Target Search Depth: depth
        ##

        # best move so far to return if timeout
        best_move = (-1,-1)

        # Best Highest score if Maximizing player
        best_max_score = float('-inf')

        # Best Highest score if Minimizing player
        best_min_score = float('inf')


        ##
        ## Mathod I: Use max_value and min_value functions
        ##

        ## Depth ==1
        if depth == 1:

            if not legal_moves:

                return (-1, -1)

            else:

                best_max_depth_score, best_move = max([(self.score(game.forecast_move(move), self), move) for move in legal_moves])

            return best_move


        elif depth > 1: 

            ## Select the best move from list of legal moves
            best_move = legal_moves[0]

            if not legal_moves:

                return (-1, -1)

            else:

                best_max_depth_score, best_move = max([(self.min_value(game.forecast_move(move), depth-1), move) for move in legal_moves])
  
            return best_move

        '''
        """
        ##
        ## Mathod II : Define and Recurcively call maximum function
        ##
        ## Assumption: Assume First player is always maximizing player
        ##
        ##             No need of maximizing_player stuff
        ## 

        if depth == 1:

            if not legal_moves:

                return (-1, -1)

            else:

                best_move_depth_score, best_move = max([(self.score(game.forecast_move(move), self), move) for move in legal_moves])

            return best_move ## in future could return best_move_depth_score

        elif depth > 1:

            if not legal_moves:

                return (-1, -1)

            else:

                best_move_depth_score, best_move = max([(self.score(game.forecast_move(self.minimax(game.forecast_move(move), depth-1)),self), move) for move in legal_moves])
                
            return best_move  ##  in future could return best_move_depth_score
        """

        
        ##
        ## Mathod II : Define and Recurcively call maximum function
        ##
        ##  NO Assumption: Explicitely define
        ##                 Maximizing Player explicitely
        ##

        if  depth == 1 :
            
            if maximizing_player == True:
                
                if not legal_moves:

                    return (-1, -1)

                else:

                    best_max_score, best_move = max([(self.score(game.forecast_move(move), self), move) for move in legal_moves])

                return best_move ## In future colud return best_max_score
                
            else:
                           
                if not legal_moves:

                    return (-1, -1)

                else:

                    best_min_score, best_move = min([(self.score(game.forecast_move(move), self), move) for move in legal_moves])

                return best_move  ## In future colud return best_min_score
    

        
        ## Now we have depth > 1
        # so we recursively call the minimax algorithm

        elif depth > 1:

            if maximizing_player == True:

                if not legal_moves:

                    return (-1, -1)

                else:

                    best_max_score, best_move = max([(self.score(game.forecast_move(self.minimax(game.forecast_move(move), depth-1, maximizing_player = False)),self), move) for move in legal_moves])
                
                return best_move  ## future could return best_max_score
                          
            else: 
                
                if not legal_moves:

                    return (-1, -1) 

                else:

                    best_min_score, best_move = min([(self.score(game.forecast_move(self.minimax(game.forecast_move(move), depth-1, maximizing_player = True)),self), move) for move in legal_moves])
                
                return best_move ## In future could return best_min_score

        '''      
    ##
    ## Method I : Uses Max and Min Functions seperately
    ##

    ## Maximum Value function
    #
    def max_value(self, game, depth):

        """
        Returns score of Max Player for a given game state

        Checks if we are at terminal state or not before returning score
        
        Get values from Min Player and comapred these values to find the max score
        
        Inputs: game: determines the game state

        Returns
        -------
               float = maximum score of current game state
        """
        
        # Time expired?
        self.time_expired()

        legal_moves = game.get_legal_moves(game.active_player)

        ## Worst possible score for Max Player
        max_score = float('-inf') 


        ## Terminal State Test
        if not legal_moves and depth <= 0:

            return max_score

        
        ## depth == 1 Case:
        if depth == 1:

            if not legal_moves:

                return max_score

            else:

                max_score, best_move = max([(self.score(game.forecast_move(move), self), move) for move in legal_moves])

            return max_score

            """
            for move in legal_moves:

                max_score = max(max_score, self.score(game.forecast_move(move), self) )

            return max_score
            """
        
        elif depth > 1:
            ## depth > 1 Case

            if not legal_moves:

                return max_score

            else:

                max_score, best_move = max([(self.min_value(game.forecast_move(move), depth-1), move) for move in legal_moves])

            return max_score # I could also return best_move in future..

            """
            for move in legal_moves:

                #max_score = max(max_score, self.min_value(game.forecast_move(move), depth-1))
            
            return max_score
            """




    ##
    ## Minimum Value function
    #
    def min_value(self, game, depth):

        """
        Returns score of Min Player for a given game state

        Checks if we are at terminal state or not before returning score
        
        Get values from Max Player and comapred these values to find the min score
        
        Inputs: game: determines the game state
           
        Returns
        -------
               float = minimum score of current game state or game move
        """
        
        # Time expired?
        self.time_expired()


        
         # Get all legal moves from thisw move
        legal_moves = game.get_legal_moves(game.active_player)

        #Worst possible value for Min Player
        min_score = float('inf')

        ## Terminal State Test
        if not legal_moves and depth <= 0:

            return min_score


        ## Non Termnal State

        if depth == 1:

            if not legal_moves:

                return min_score

            else:

                min_score, best_move = min([(self.score(game.forecast_move(move), self), move) for move in legal_moves])

            return min_score # I could also return best_move in future..
    
            """
            for move in legal_moves:
                
                min_score = min(min_score, self.score(game.forecast_move(move), self) )

            return min_score
            """

        elif depth > 1:

            if not legal_moves:

                return min_score

            else:

                min_score, best_move = min([(self.max_value(game.forecast_move(move), depth-1), move) for move in legal_moves])

            return min_score # I could also return best_move in future..

            """
            for move in legal_moves:
                
                #min_score = min(min_score, self.max_value(game.forecast_move(move), depth-1))

            return min_score
            """


    def time_expired(self):
        
        """
         Raises Tiem out error once time has expired
        """
        if self.time_left() < self.TIMER_THRESHOLD:
    
            raise SearchTimeout()




class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left, iterative_deepening_search = True):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """


        self.time_left = time_left
        
        ## check Time Out
        self.time_out()


        ## check if any legal moves i.e forfeit the game at once
        legal_moves = game.get_legal_moves(game.active_player)

        if not legal_moves:

            return (-1,-1)
        


        ## on an empty board. Get the center move as the best move
        if game.move_count == 0:

            return (int(game.height/2), int(game.width/2))
        

        
        # TODO: finish this function!
        #raise NotImplementedError
        # Initialised best move so far
        best_move = (-1, -1)

        best_score = float('inf')


        
        ## TO DO
        # How to handle Iterative search Vs Non-Iterative Search
        
        try:
            if iterative_deepening_search == True:

                iterative_search_depth = 1

                while True:

                    best_move  = self.alphabeta(game, iterative_search_depth)

                    iterative_search_depth += 1
            else:

                best_move = self.alphabeta(game, self.search_depth)

            
        except SearchTimeout:
            
            # Handle any actions required after timeout as needed
            pass
            
        
        # Return best move from the last completed search
        return best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), max_player=True):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        ## Time out check
        self.time_out()

        #Get legal moves left for us to play
        legal_moves = game.get_legal_moves(game.active_player)
        
        ## Terminal State
        if not legal_moves or depth <= 0:

            return (-1, -1)


        ## Now begin Terminal Iterative search
        optimal_move = (-1, -1)

        optimal_score = alpha


        ## start with depth == 1        
        if depth == 1:

            for move in legal_moves:

                temp_score = self.score(game.forecast_move(move), self)

                if temp_score > optimal_score:

                    optimal_score = temp_score

                    optimal_move = move


            return optimal_move


        elif depth > 1:

            for move in legal_moves:

                temp_score = self.min_alpha_beta(game.forecast_move(move), depth-1, optimal_score, beta)

                if temp_score > optimal_score:

                    optimal_score = temp_score

                    optimal_move = move


            return optimal_move


            
        '''
        ## Heading for target search depth,
        lowest_score_this_far = float('inf')
        
        highest_score_this_far = float('-inf')
        
        best_move_this_far = (-1, -1)

        

    
        ## start with depth == 1        
        if depth == 1:
            
            if max_player == True:

                # Get the highest or equal beta score & move
                #highest_beta_score_this_far, best_beta_move_so_far = max([(self.score(game.forecast_move(move), self), move) for move in legal_moves if self.score(game.forecast_move(move), self) >= beta])
                for my_move in legal_moves:

                    highest_score_this_far = self.score(game.forecast_move(my_move), self)

                    ## As soon as we get greater_than_beta move, we're good.
                    if  highest_score_this_far >= beta:

                        return my_move



                # Get for highest score move
                temp_max_score, best_move_this_far = max([(self.score(game.forecast_move(move), self), move) for move in legal_moves])
                    
                return best_move_this_far

                
            #Not max player?
            else:

                # Get smaller or equal alpha score & move
                #lowest_alpha_score_this_far, best_alpha_move_so_far = [(self.score(game.forecast_move(move), self), move) for move in legal_moves if self.score(game.forecast_move(move), self) <= alpha]
                for my_move in legal_moves:

                    lowest_score_this_far  = self.score(game.forecast_move(my_move), self)

                    ## As soon as we get less_than_alpha_ move, we're good.
                    if lowest_score_this_far  <= alpha:

                        return my_move


                # Check for smallest score move
                lowest_score_this_far, best_move_this_far = min([(self.score(game.forecast_move(move), self), move) for move in legal_moves])
      
                return best_move_this_far
                
        
        
        ## We still have some legal moves and we are not yet at target search
        #depth > 1
        
        elif depth > 1:
            
            if max_player == True:

                # Get the higher or equal to beta score & move
                #highest_beta_score_this_far, best_beta_move_so_far = [(self.score(game.forecast_move(self.alphabeta(game.forecast_move(move), depth-1, max_player=False)),self), move) for move in legal_moves if self.score(game.forecast_move(self.alphabeta(game.forecast_move(move), depth-1, max_player=False)),self) >= beta ]
                for my_move in legal_moves:

                    highest_score_this_far = self.score(game.forecast_move(self.alphabeta(game.forecast_move(my_move), depth-1, alpha, beta, max_player=False)), self)

                    ## As soon as we get greater_than_beta move, we're good.
                    if highest_score_this_far >= beta:

                        return my_move

                # Get for highest score move
                highest_score_this_far, best_move_this_far = max([(self.score(game.forecast_move(self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, max_player=False)),self), move) for move in legal_moves])

                ## Get new alpha
                alpha = max(alpha, highest_score_this_far)

                return best_move_this_far

                
            # Not max player?
            else:

                # Get smaller than or equal to alpha move
                #lowest_alpha_score_this_far, best_alpha_move_so_far = [(self.score(game.forecast_move(self.alphabeta(game.forecast_move(move), depth-1, max_player=True)),self), move) for move in legal_moves if self.score(game.forecast_move(self.alphabeta(game.forecast_move(move), depth-1, max_player=True)),self) <= alpha ]
                for my_move in legal_moves:

                    lowest_score_this_far = self.score(game.forecast_move(self.alphabeta(game.forecast_move(my_move), depth-1, alpha, beta, max_player=True)),self)

                    ## As soon as we get less_than_alpha_ move, we're good.
                    if  lowest_score_this_far <= alpha:

                        return  my_move


                # Check for smallest score move
                lowest_score_this_far, best_move_this_far = min([(self.score(game.forecast_move(self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, max_player=True)),self), move) for move in legal_moves])

                ## Get new beta
                beta = min(beta, lowest_score_this_far)

                return best_move_this_far
                
            '''




    def max_alpha_beta(self, game, depth, alpha, beta):
        """
        Implement max_alpha_beta of depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers


       

        Returns
        -------

        alpha: float
            The new updated Alpha limits the lower bound of search on minimizing layers

        """

        # time_out
        self.time_out()

        # get legal moves
        legal_moves = game.get_legal_moves(game.active_player)

        #Worst possible value for Max Player
        max_score = float('-inf')


        ## Terminal State Test
        if not legal_moves and depth <= 0:

            return max_score  


        ## depth == 1

        if depth == 1:

            for my_move in legal_moves:

                max_score = max(max_score, self.score(game.forecast_move(my_move), self) )

                ## As soon as we get greater_than_beta move, we're good.
                if  max_score >= beta:

                    return  max_score

                alpha = max(alpha, max_score)

            return alpha

        
        ## depth > 1
        if depth > 1:

            for my_move in legal_moves:

                max_score = max(max_score, self.min_alpha_beta(game.forecast_move(my_move), depth-1, alpha, beta) )

                ## As soon as we get greater_than_beta, we're good.
                if  max_score >= beta:

                    return  max_score

                alpha = max(alpha, max_score)


            return alpha





    def min_alpha_beta(self, game, depth, alpha, beta):

        """
        Implement min_alpha_beta of depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers


        float
            beta

        Returns
        -------

        beta: float
            Updated Beta limits the upper bound of search on maximizing layers

        """

        # time_out
        self.time_out()

        #Get Legal Moves:
        legal_moves = game.get_legal_moves(game.active_player)

        #Worst possible value for Max Player
        min_score = float('inf')



        ## Terminal State Test
        if not legal_moves and depth <= 0:

            return min_score


        ## depth == 1

        if depth == 1:

            for my_move in legal_moves:

                min_score = min(min_score, self.score(game.forecast_move(my_move), self) )

                 ## As soon as we get less than beta, we're good.
                if  min_score <= alpha:

                    return  min_score

                beta = min(beta, min_score)

            return beta

        
        ## depth > 1
        if depth > 1:

            for my_move in legal_moves:

                min_score = min(min_score, self.max_alpha_beta(game.forecast_move(my_move), depth-1, alpha, beta) )

                ## As soon as we get less than beta, we're good.
                if  min_score <= alpha:

                    return  min_score

                beta = min(beta, min_score)


            return beta


    def time_out(self):
        """
         Raises Tiem out error once time has expired
        """
        if self.time_left() < self.TIMER_THRESHOLD:
    
            raise SearchTimeout()
            
                    
                    
        
       