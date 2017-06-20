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
        
        ## If we just began the game or for an empty game
        if game.move_count == 0:
            
            return (int(game.height/2), int(game.width/2))
            
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


        # Are there any legal moves left for us to play? If not, then return (-1, -1)!
        legal_moves = game.get_legal_moves()

        if not legal_moves:

            return (-1, -1)

        # best move so far to return if timeout
        best_move = (-1,-1)

        # Best Highest score if Maximizing player
        best_max_score = float('-inf')

        # Best Highest score if Minimizing player
        best_min_score = float('inf')



        
        # TODO: finish this function!
        ## Max Node to begin with
        if depth == 0:
            ## Max is just the single Node so it does not matter much!
            return max([(self.score(game.forecast_move(move), self), move) for move in legal_moves])


        if depth == 1:
            
            depth -= 1
            
            if maximizing_player == True:
                
                for move in legal_moves:
                    
                    #temp_score = max(best_max_score,self.min_value(game, game.forecast_move(move)))
                    #temp_score = max(best_max_score, self.score(self.minimax(game, depth, maximizing_player = False), self) )
                    temp_score = max(best_max_score, self.score(game.forecast_move(move), self))
                    
                     # If we are lucky enough to find the winning score right away then end the damn for-loop
                    if temp_score == float('inf'):
                        
                        return move
                    
                    if temp_score > best_max_score:
                        
                        best_max_score == temp_score
                        
                        best_move = move
                        
                        
                return best_move
                
                ## Get move with best score
                #return max([(self.min_value(game, game.forecast_move(move)), move) for move in legal_moves])

            else:
                
                depth -= 1
                
                for move in legal_moves:
                    
                    #temp_score = min(best_min_score,self.max_value(game,game.forecast_move(move)))
                    #temp_score = min(best_min_score,self.score(self.minimax(game, depth, maximizing_player = True), self))
                    temp_score = min(best_min_score, self.score(game.forecast_move(move), self))
                    
                     # If we are lucky enough to find the minimal score right away then end the damn for-loop
                    if temp_score == float('-inf'):
                        
                        return move
                    
                    if temp_score < best_min_score:
                        
                        best_min_score == temp_score
                        
                        best_move = move
                        
                        
                return best_move
                
                ## Get move with best score
                #return min([(self.max_value(game, game.forecast_move(move)), move) for move in legal_moves])
        
           
        
        ## Now we have depth > 1
        # so we recursively call the maximum algorithm
        if maximizing_player == True:
            
            depth -= 1
            
            for move in legal_moves:
                
                #temp_score = self.score(self.minimax(game, depth-1, maximizing_player = False), self)
                temp_score = self.min_value(game, game.forecast_move(move))
                
                # If we are lucky enough to find the winning score right away then end the damn for-loop
                if temp_score == float('inf'):
                    
                    return move
                    
                # find best move from all legal moves using score
                if temp_score > best_max_score:
                    
                    best_max_score = temp_score
                    
                    best_move = move
                        
            return best_move
            
        else: ## Handle Minimmizing player
          
            depth -= 1
            
            for move in legal_moves:
                
                #temp_score = self.score(self.minimax(game, depth-1, maximizing_player = True), self)
                temp_score = self.max_value(game,game.forecast_move(move))
    
                # If we are lucky enough to find the winning score right away then end the damn for-loop
                if temp_score == float('-inf'):
    
                    return move
    
                # find best move from all legal moves using score
                if temp_score < best_min_score:
    
                    best_min_score = temp_score
    
                    best_move = move
    
    
            return best_move
        

            




    def max_value(self, game, move):

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

        # Check if current move is the end move
        if self.terminal_state(game) == True:

            return self.score(game.forecast_move(move), self)


        legal_moves = game.get_legal_moves()

        ## Worst possible score for Max Player
        max_score = float('-inf')

        ##Now loop through all moves and find max score for all forecasted moves
        for move in legal_moves:

            temporal_score =  self.score(game.forecast_move(move), self)
            ##  Get Minplayer Score for all possible legal moves
            #temporal_score =  self.min_value(game, game.forecast_move(move))
            
            # If we are lucky enough to find the winning score right away then end the damn for-loop
            if temporal_score == float('inf'):
                
                return temporal_score

            if temporal_score > max_score:
                
                max_score = temporal_score


        return max_score





    def min_value(self, game, move):

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
        
        
        # Check if current move is end move
        if self.terminal_state(game) == True:

            return self.score(game.forecast_move(move), self) ## ought to return heuristic at terminal node?

        #Worst possible value for Min Player
        min_score = float('inf')
        
        # Get all legal moves from thisw move
        legal_moves = game.get_legal_moves()

        ##Now loop through all moves and find max score for all forcasted moves
        for move in legal_moves:

            # Get temporal score from Max Player
            temporal_score = self.score(game.forecast_move(move), self)
            #temporal_score = self.max_value(game, game.forecast_move(move))
            
            #End loop if we  arriaved at the best possible score for Min
            if temporal_score == float('-inf'):

                return temporal_score

            if temporal_score < min_score:

                min_score = temporal_score

        return min_score



   



    def terminal_state(self, game):

        """
        A game state at a current move is terminal if there are no
        legal moves available

        Returns
        -------
         True/False if we are at a terminal state of game

        """
        #Check if time has expired
        self.time_expired()
            
        
        return len(game.get_legal_moves()) == 0
        #raise NotImplementedError



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

    def get_move(self, game, time_left):
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
        
        if self.time_left() < self.TIMER_THRESHOLD:

            #return best_move_this_far
            raise SearchTimeout()


        legal_moves = game.get_legal_moves()

        if not legal_moves:

            return (-1,-1)
        


        ## If we just started the game then the center is the best move
        if game.move_count == 0:

            return (int(game.height/2), int(game.width/2))
            

        # TODO: finish this function!
        #raise NotImplementedError
        # Initialised best move so far
        best_move_this_far = (-1, -1)
        
        ## TO DO
        # How to handle Iterative search Vs Non-Iterative Search
        
        try:
            
            return self.alphabeta(game, self.search_depth)
            
        except SearchTimeout:
            
            # Handle any actions required after timeout as needed
            pass
            
        
        # Return best move from the last completed search
        return best_move_this_far


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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        #raise NotImplementedError

        #Get legal moves left for us to play

        legal_moves = game.get_legal_moves()
        
        if not legal_moves:
            
            return (-1, -1)
            
        ## If we reach the target search depth,
            
            
        lowest_score_this_far = float('inf')
        
        highest_score_this_far = float('-inf')
        
        best_move_this_far = (-1, -1)
        
        
        ## start with depth == 1        
        if depth == 1:
            
            if max_player == True:
                
                for move in legal_moves:
                    
                    #score this move
                    
                    score = self.score(game.forecast_move(move), self)
                    
                    #is score better than beta? no need to search further if so
                    
                    if score >= beta:
                        
                        return move
                        
                    if score > highest_score_this_far:
                        
                        highest_score_this_far = score
                        
                        best_move_this_far = move
                        
                return best_move_this_far
                
            #Not max player?
            else:
                
                for move in legal_moves:
                    
                    #score this move
                    score = self.score(game.forecast_move(move), self)
                    
                    #is score worse than alpha? no need to search further
                    
                    if score <= alpha:
                        
                        return move
                        
                    if score < lowest_score_this_far:
                        
                        lowest_score_this_far = score
                        
                        best_move_this_far = move
                        
                return best_move_this_far
        
        
        
        ## We still have some legal moves and we are not yet at target search
        #depth > 1
        
        else:
            
            if max_player == True:
                
                for move in legal_moves:
                    
                    ##score this move
                    
                    score = self.score(self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, max_player=False), self)
            
                    ## if score of this branch is better than beta, end search
            
                    if score > beta:
                        
                        return move
                        
                    ## Score is not better than beta so get new alpha
                        
                    if score > highest_score_this_far:
                        
                        highest_score_this_far = score
                        
                        best_move_this_far = move
                        
                        ## Get new alpha
                        alpha = max(alpha, highest_score_this_far)
                        
                return best_move_this_far
                
            # Not max player?
                
            else:
                
                for move in legal_moves:
                    
                    ##score this move
                    
                    score = self.score(self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, max_player=True), self)
            
                    ## if score of this branch is worse than alpha, end search
            
                    if score <= alpha:
                        
                        return move
                        
                    ## Score is not better than beta so get new alpha
                        
                    if score < lowest_score_this_far:
                        
                        lowest_score_this_far = score
                        
                        best_move_this_far = move
                        
                        ## Get new beta
                        beta = min(beta, lowest_score_this_far)
                        
                return best_move_this_far
                
                
                        
                    
        
       