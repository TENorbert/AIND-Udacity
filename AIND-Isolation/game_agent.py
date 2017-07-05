"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

import math



class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass




## NUMBER OF REMAINING MOVES + SIMPLE DISTANCE + LEGITIMATE MOVES
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


        PERFORMANCE::

                        *************************
                             Playing Matches
                        *************************

         Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                                Won | Lost   Won | Lost   Won | Lost   Won | Lost
            1       Random       8  |   2    10  |   0     9  |   1     8  |   2
            2       MM_Open      6  |   4     8  |   2     8  |   2     6  |   4
            3      MM_Center     8  |   2     6  |   4     7  |   3     8  |   2
            4     MM_Improved    8  |   2     6  |   4     6  |   4     8  |   2
            5       AB_Open      7  |   3     6  |   4     7  |   3     7  |   3
            6      AB_Center     5  |   5     6  |   4     6  |   4     6  |   4
            7     AB_Improved    5  |   5     4  |   6     6  |   4     4  |   6
        --------------------------------------------------------------------------
                   Win Rate:      67.1%        65.7%        70.0%        67.1%

        Your ID search forfeited 160.0 games while there were still legal moves available to play.

    """

    ###If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):

        return float('-inf')

    #If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):

        return float('inf')

    ## player Remaining moves
    player_remaining_moves = len(game.get_legal_moves(player))

    # opponent remaining moves
    opponent_remaining_moves = len(game.get_legal_moves(game.get_opponent(player)))


    if player_remaining_moves != opponent_remaining_moves:

        return float(player_remaining_moves - opponent_remaining_moves)

    # what if both players have the same number of remaining moves; who wins?
    else:
        ## We employ distance to center to find who can actually win
        ## why? b/c the person closest to the center has a special advantage of winning the game
        ## as they have much more space to move to.
        y_center = int(game.height / 2)
        x_center = int(game.width / 2)

        player_y_position, player_x_position = game.get_player_location(player)
        opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

        player_dist_to_center = abs(player_y_position - y_center) + abs(player_x_position - x_center)

        opp_dist_to_center = abs(opp_y_position - y_center) + abs(opp_x_position - x_center)

        dist_difference = float(player_dist_to_center - opp_dist_to_center) / 10.

        ## what if both have the same distance to center?
        if player_dist_to_center != opp_dist_to_center:

            return dist_difference

        else:

            # Now both players have the same distance to the center, so we should
            # employ a heuristic that considers the actual legal number of moves they would make
            # using the player's current_position, and the number of moves left.
            # i.e the number of actual legal moves from the remaining moves will
            # should provide better evaluation and taking into consideration that
            # by symmetry, some moves are actually the same.. i.e symmetric
            # along the vertical, horizontal, and diagonals from their current
            # position.
            # obviously the player with more(less) actual(legitimate) number of legal moves
            # wins(loses) the game.

            player_moves = game.get_legal_moves(player)

            opponent_moves = game.get_legal_moves(game.get_opponent(player))

            #legitimate_player_moves = get_legitimate_legal_moves(game, player_x_position, player_y_position, player_moves)

            #legitimate_opp_moves = get_legitimate_legal_moves(game, opp_x_position, opp_y_position, opponent_moves)

            legitimate_player_moves = get_sum_jumping_runs(game, player_x_position, player_y_position, player_moves)

            legitimate_opp_moves = get_sum_jumping_runs(game, opp_x_position, opp_y_position, opponent_moves)

            if legitimate_player_moves != legitimate_opp_moves:

                return float(legitimate_player_moves - legitimate_opp_moves) / 100.

            else:

                return 0.
            




'''
## NUMBER OF REMAINING MOVES + EUCLIDEAN DISTANCE + LEGITIMATE MOVE RUNS
def custom_score(game, player):
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



                       *************************
                             Playing Matches
                        *************************

         Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                                Won | Lost   Won | Lost   Won | Lost   Won | Lost
            1       Random       8  |   2     8  |   2     7  |   3     8  |   2
            2       MM_Open      8  |   2     6  |   4     7  |   3     8  |   2
            3      MM_Center     8  |   2     9  |   1     9  |   1     6  |   4
            4     MM_Improved    5  |   5     8  |   2     4  |   6     7  |   3
            5       AB_Open      7  |   3     6  |   4     5  |   5     5  |   5
            6      AB_Center     4  |   6     8  |   2     4  |   6     4  |   6
            7     AB_Improved    7  |   3     6  |   4     4  |   6     3  |   7
        --------------------------------------------------------------------------
                   Win Rate:      67.1%        72.9%        57.1%        58.6%

        Your ID search forfeited 164.0 games while there were still legal moves available to play

    """

    ##If the player is loser... then his score has obviously not improved
    if game.is_loser(player):
        return float('-inf')

    # If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):
        return float('inf')

    player_y_position, player_x_position = game.get_player_location(player)
    opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))


    ## Use only player remaining moves as evaluation.
    player_remaining_moves = len(game.get_legal_moves(player))

    opponent_remaining_moves = len(game.get_legal_moves(game.get_opponent(player)))

    ## First use number of moves
    if player_remaining_moves != opponent_remaining_moves:

        return float(player_remaining_moves - opponent_remaining_moves)

    ## Now use distance to center: return 0 if both distances to center are equal
    else:

        player_euclidean_distance_from_center = distance_to_center(game, player_y_position,player_x_position)
        opponent_euclidean_distance_from_center = distance_to_center(game,opp_y_position,opp_x_position)

        if player_euclidean_distance_from_center != opponent_euclidean_distance_from_center:

            return float(player_euclidean_distance_from_center - opponent_euclidean_distance_from_center) / 10.

        else:

            # Now both players have the same distance to the center, so we should
            # employ a heuristic that considers the actual legal number of moves they would make
            # using the player's current_position, and the number of moves left.
            # i.e the number of actual legal moves from the remaining moves will
            # should provide better evaluation and taking into consideration that
            # by symmetry, some moves are actually the same.. i.e symmetric
            # along the vertical, horizontal, and diagonals from their current
            # position.
            # obviously the player with more(less) actual(legitimate) number of legal moves
            # wins(loses) the game.

            player_moves = game.get_legal_moves(player)

            opponent_moves = game.get_legal_moves(game.get_opponent(player))

            legitimate_player_moves = get_legitimate_legal_moves(game, player_x_position, player_y_position,player_moves)

            legitimate_opp_moves = get_legitimate_legal_moves(game, opp_x_position, opp_y_position, opponent_moves)

            #legitimate_player_moves = get_sum_jumping_runs(game, player_x_position, player_y_position, player_moves)

            #legitimate_opp_moves = get_sum_jumping_runs(game, opp_x_position, opp_y_position, opponent_moves)

            if legitimate_player_moves != legitimate_opp_moves:
                
                return float(legitimate_player_moves - legitimate_opp_moves)  / 100.
            
            else:

                return 0.


'''


## Remainin Moves + JUMPING SUM RUNS ONLY
def custom_score_2(game, player):

    """
        This heuristic value is simply the difference between the player's

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
            
            
            PERFORMANCE

    """


    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):
        return float('-inf')

    # If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):
        return float('inf')

    ## player Remaining moves
    player_rem_moves = len(game.get_legal_moves(player))

    # opponent remaining moves
    opponent_rem_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if player_rem_moves != opponent_rem_moves:

        return float(player_rem_moves - opponent_rem_moves)

    # what if both players have the same number of remaining moves; who wins?
    else:

        player_y_position, player_x_position = game.get_player_location(player)
        opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

        player_moves = game.get_legal_moves(player)

        opponent_moves = game.get_legal_moves(game.get_opponent(player))

        #legitimate_player_moves = get_legitimate_legal_moves(game, player_x_position, player_y_position,player_moves)

        #legitimate_opp_moves = get_legitimate_legal_moves(game, opp_x_position, opp_y_position, opponent_moves)

        legitimate_player_moves = get_sum_jumping_runs(game, player_x_position, player_y_position,player_moves)

        legitimate_opp_moves = get_sum_jumping_runs(game, opp_x_position, opp_y_position, opponent_moves)


        if legitimate_player_moves != legitimate_opp_moves :

            return float(legitimate_player_moves - legitimate_opp_moves) / 100.

        else:

            ## SIMPLE DISTANCE
            ## We employ distance to center to find who can actually win
            ## why? b/c the person closest to the center has a special advantage of winning the game
            ## as they have much more space to move to.
            y_center = int(game.height / 2)
            x_center = int(game.width / 2)

            player_y_position, player_x_position = game.get_player_location(player)
            opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

            player_dist_to_center = abs(player_y_position - y_center) + abs(player_x_position - x_center)

            opp_dist_to_center = abs(opp_y_position - y_center) + abs(opp_x_position - x_center)

            dist_difference = float(player_dist_to_center - opp_dist_to_center) / 10.
            ## what if both have the same distance to center, then return 0
            if player_dist_to_center != opp_dist_to_center:

                return dist_difference

            else: ## it might be nice in future to find another better heurestic to call here!

                return 0.




'''
## NUMBER OF REMAINING MOVES
def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This heuristic value is simply the difference between the number of
    player's remaining moves and the opponent's remaining moves.
    The player wins(loss) if they have fewer(more) moves left compared to the opponent.
    Game is a draw if player and opponent have the same number of moves left.

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

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):

        return float('-inf')

    #If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):

        return float('inf')

    ## Use only player remaining moves as evaluation.
    player_remaining_moves = len(game.get_legal_moves(player))

    opponent_remaining_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(player_remaining_moves - opponent_remaining_moves)
'''

'''
##LEGITIMATE MOVE RUNS ONLY
def custom_score_3(game, player):

    """
                        *************************
                             Playing Matches
                        *************************

         Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                                Won | Lost   Won | Lost   Won | Lost   Won | Lost
            1       Random       9  |   1     8  |   2     8  |   2     8  |   2
            2       MM_Open      8  |   2     9  |   1     5  |   5     6  |   4
            3      MM_Center     9  |   1     8  |   2     6  |   4     9  |   1
            4     MM_Improved    8  |   2     5  |   5     5  |   5     6  |   4
            5       AB_Open      5  |   5     5  |   5     6  |   4     5  |   5
            6      AB_Center     6  |   4     4  |   6     7  |   3     2  |   8
            7     AB_Improved    6  |   4     6  |   4     4  |   6     4  |   6
        --------------------------------------------------------------------------
                   Win Rate:      72.9%        64.3%        58.6%        57.1%

        Your ID search forfeited 163.0 games while there were still legal moves available to play.

    """

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):
        return float('-inf')

    # If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):
        return float('inf')


    player_y_position, player_x_position = game.get_player_location(player)
    opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

    player_moves = game.get_legal_moves(player)

    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    legitimate_player_moves = get_legitimate_legal_moves(game, player_x_position, player_y_position, player_moves)

    legitimate_opp_moves = get_legitimate_legal_moves(game, opp_x_position, opp_y_position, opponent_moves)

    return float(legitimate_player_moves - legitimate_opp_moves) / 100.

'''

'''
##DISTANCE ONLY
def custom_score_3(game, player):

    """
      Distance only
    """

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):
        return float('-inf')

    # If the player is the winnder.. then obviously he gets the max score.
    if game.is_winner(player):
        return float('inf')


    ## SIMPLE DISTANCE
    ## We employ distance to center to find who can actually win
    ## why? b/c the person closest to the center has a special advantage of winning the game
    ## as they have much more space to move to.


    y_center = int(game.height / 2)
    x_center = int(game.width / 2)

    player_y_position, player_x_position = game.get_player_location(player)
    opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

    player_dist_to_center = abs(player_y_position - y_center) + abs(player_x_position - x_center)

    opp_dist_to_center = abs(opp_y_position - y_center) + abs(opp_x_position - x_center)

    dist_difference = float(player_dist_to_center - opp_dist_to_center) / 10.

    ## what if both have the same distance to center, then return 0
    if player_dist_to_center != opp_dist_to_center:

        return dist_difference

    else:

        return 0.


    """
    ##EUCLIDEAN DISTANCE

    player_y_position, player_x_position = game.get_player_location(player)
    opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

    player_dist_from_center = distance_to_center(game, player_y_position, player_x_position)
    opponent_dist_from_center = distance_to_center(game, opp_y_position, opp_x_position)

    if player_dist_from_center != opponent_dist_from_center:

        return float(player_dist_from_center - opponent_dist_from_center) /10.
    """

'''


## NUMBER OF REMAINING MOVES + SIMPLE DISTANCE
def custom_score_3(game, player):
    """
    Calculate the heuristic value of a game state from the point of view
    of the given player.

    This heuristic value is simply the difference in the number of
    player's remaining moves and the opponent's remaining moves.
    The player wins(loss) if they have fewer(more) moves left compared to the opponent.

    if player and opponent have the same number of moves left
    use their simple distance to center of board as new evaluation.
    Since player most closest to the center
    would likely win due to his additional space left for him to maneuver or move.

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


        PERFORMANCE:

                        *************************
                             Playing Matches
                        *************************

                 Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
                    1       Random       7  |   3     9  |   1     8  |   2     8  |   2
                    2       MM_Open     10  |   0     6  |   4     9  |   1     9  |   1
                    3      MM_Center     6  |   4     9  |   1     6  |   4     9  |   1
                    4     MM_Improved    7  |   3     6  |   4     7  |   3     6  |   4
                    5       AB_Open      8  |   2     6  |   4     6  |   4     5  |   5
                    6      AB_Center     5  |   5     6  |   4     5  |   5     8  |   2
                    7     AB_Improved    6  |   4     2  |   8     6  |   4     6  |   4
                --------------------------------------------------------------------------
                           Win Rate:      70.0%        62.9%        67.1%        72.9%

                Your ID search forfeited 158.0 games while there were still legal moves available to play.

    """

    ##If the player is loser... then his score has obviously not imporoved
    if game.is_loser(player):
        return float('-inf')

    # If the player is the winner.. then obviously he gets the max score.
    if game.is_winner(player):
        return float('inf')

    ## player Remaining moves
    player_rem_moves = len(game.get_legal_moves(player))

    # opponent remaining moves
    opponent_rem_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if player_rem_moves != opponent_rem_moves:

        return float(player_rem_moves - opponent_rem_moves)

    # what if both players have the same number of remaining moves; who wins?
    else:
        ## SIMPLE DISTANCE
        ## We employ distance to center to find who can actually win
        ## why? b/c the person closest to the center has a special advantage of winning the game
        ## as they have much more space to move to.
        y_center = int(game.height / 2)
        x_center = int(game.width / 2)

        player_y_position, player_x_position = game.get_player_location(player)
        opp_y_position, opp_x_position = game.get_player_location(game.get_opponent(player))

        player_dist_to_center = abs(player_y_position - y_center) + abs(player_x_position - x_center)

        opp_dist_to_center = abs(opp_y_position - y_center) + abs(opp_x_position - x_center)

        dist_difference = float(player_dist_to_center - opp_dist_to_center) / 10.

        ## what if both have the same distance to center, then return 0
        if player_dist_to_center != opp_dist_to_center:

            return dist_difference

        else:

            ##EUCLIDEAN DISTANCE
            player_euclidean_distance_to_center = distance_to_center(game, player_y_position, player_x_position)
            opponent_euclidean_distance_to_center = distance_to_center(game, opp_y_position, opp_x_position)


            if player_euclidean_distance_to_center != opponent_euclidean_distance_to_center:

                return float(player_euclidean_distance_to_center - opponent_euclidean_distance_to_center) / 10.

            else:

                return 0.
            





#
# Utility Functions
#

def distance_to_center(game, y_position, x_position):
    """
    Computes the distance to distance from the current player's postion.
    EUCLIDEAN distance to center of board as new evaluation
    dist((x,y), (cx,cy)) = sqrt((x-cx)**2 + (y-cy)**2)
    since player most closest to the center
    would likely win due if only the opponent does not mirror his subsequent moves.

    :param self:
    :param y_position:
            y position of player
    :param x_position:
            x position of player
    :return:
            float: distance from center
    """

    ## Use Distance to center only as heuristic!
    # it should take care of all the symmetry advantages
    y_center = int(game.height / 2)
    x_center = int(game.width / 2)

    #return float(((y_position - y_center )**2 + (x_position - x_center)**2)**(1/2.0))
    return float(math.sqrt((y_position - y_center )**2 + (x_position - x_center )**2))



def get_legitimate_legal_moves(game, player_y_pos, player_x_pos, moves):
    """This function measures the longest run of jumping moves that can be performed inside the 3x3 squares
    defined by a starting position and EACH of its legal moves left. The longest run one can hope to reach is 7.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player_y_pos, player_x_pos : int, int
        The player's position to evaluate based on its longest jumping run.

    moves : `list` of legal moves for 'player'
        List` of legal moves for 'player'

    Returns
    -------
    int
        The longest run found.
    """

    # ********************** NOTE TO THE REVIEWER ***************************
    # Portions of our heuristics were flagged as needing a rewrite (use for loops, move redundant code in a function)
    # It is our contention that FUNCTION INLINING and LOOP UNROLLING are CRITICAL to the success of this heuristic.
    # It is BECAUSE we don't use functions and for loops that our code can explore more branches before timeout.
    # Using functions (even when passing parameters by reference) and setting up for loops INCREASE OVERHEAD.
    # How do we know this makes a difference here? Because we tried both approaches!
    # Please keep in mind that an increase in code size can be irrelevant when it translates in a significant speed win.
    # Thank you.
    # Respectfully, Phil Ferriere

    longest_player_run = 1
    for move_y, move_x in moves:
        if longest_player_run == 7:
            break
        player_run = 1
        if move_y == player_y_pos + 1 and move_x == player_x_pos + 2:  # Pos 1
            # Start the run going East-South
            # +---+---+---+
            # | 5 | 2 | 7 |
            # +---+---+---+
            # | p | x | 4 |
            # +---+---+---+
            # | 3 | 6 | 1 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 2)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 2)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos - 1 and move_x == player_x_pos + 2:  # Pos 1
            # Start the run going East-North
            # +---+---+---+
            # | 3 | 6 | 1 |
            # +---+---+---+
            # | p | x | 4 |
            # +---+---+---+
            # | 5 | 2 | 7 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 2)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 2)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos - 2 and move_x == player_x_pos + 1:  # Pos 1
            # Start the run going North-East
            # +---+---+---+
            # | 6 | 1 | 4 |
            # +---+---+---+
            # | 3 | x | 7 |
            # +---+---+---+
            # | p | 5 | 2 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos, player_x_pos + 2)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos + 2)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 2)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos - 2 and move_x == player_x_pos - 1:  # Pos 1
            # Start the run going North-West
            # +---+---+---+
            # | 1 | 4 | 7 |
            # +---+---+---+
            # | 6 | x | 2 |
            # +---+---+---+
            # | 3 | p | 5 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 1)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos + 1)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos - 1 and move_x == player_x_pos - 2:  # Pos 1
            # Start the run going West-North
            # +---+---+---+
            # | 1 | 6 | 3 |
            # +---+---+---+
            # | 4 | x | p |
            # +---+---+---+
            # | 7 | 2 | 5 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 2)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 2)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos + 1 and move_x == player_x_pos - 2:  # Pos 1
            # Start the run going West-South
            # +---+---+---+
            # | 7 | 2 | 5 |
            # +---+---+---+
            # | 4 | x | p |
            # +---+---+---+
            # | 1 | 6 | 3 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 2)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 2)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos + 2 and move_x == player_x_pos - 1:  # Pos 1
            # Start the run going South-West
            # +---+---+---+
            # | 3 | p | 5 |
            # +---+---+---+
            # | 6 | x | 2 |
            # +---+---+---+
            # | 1 | 4 | 7 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 1)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos + 1)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

        if move_y == player_y_pos + 2 and move_x == player_x_pos + 1:  # Pos 1
            # Start the run going South-East
            # +---+---+---+
            # | 5 | p | 3 |
            # +---+---+---+
            # | 2 | x | 6 |
            # +---+---+---+
            # | 7 | 4 | 1 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 2
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 3
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos)):  # Pos 4
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 1)):  # Pos 5
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 6
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                player_run += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos - 1)):  # Pos 7
                longest_player_run = max(longest_player_run, player_run)
                continue
            else:
                longest_player_run = 7  # max(longest_player_run, player_run + 1)
                break

    return longest_player_run




def get_sum_jumping_runs(game, player_y_pos, player_x_pos, moves):
    """This function measures the longest run of jumping moves that can be performed inside the 3x3 squares
    defined by a starting position and each of its legal moves left. The longest run one can hope to reach is 7.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player_y_pos, player_x_pos : int, int
        The player's position to evaluate based on its longest jumping run.

    moves : `list` of legal moves for 'player'
        List` of legal moves for 'player'

    Returns
    -------
    int
        The longest run found.
    """

    # ********************** NOTE TO THE REVIEWER ***************************
    # The code below was flagged as needing a revrite (use for loops, move redundant code in a function)
    # It is our contention that FUNCTION INLINING and LOOP UNROLLING are CRITICAL to the success of this heuristic.
    # It is BECAUSE we don't use functions and for loops that our code can explore more branches before timeout.
    # Using functions (even when passing parameters by reference) and setting up for loops INCREASE OVERHEAD.
    # How do we know this makes a different here? Because we tried both ways!
    # Please keep in mind that an increase in code size can be irrelevant when it translates in a significant speed win.
    # Thank you.
    # Respectfully, Phil Ferriere

    sum_jumping_runs = 0
    for move_y, move_x in moves:
        if move_y == player_y_pos + 1 and move_x == player_x_pos + 2:  # Pos 1
            # Start the run going East-South
            # +---+---+---+
            # | 5 | 2 | 7 |
            # +---+---+---+
            # | p | x | 4 |
            # +---+---+---+
            # | 3 | 6 | 1 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 2)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 2)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos - 1 and move_x == player_x_pos + 2:  # Pos 1
            # Start the run going East-North
            # +---+---+---+
            # | 3 | 6 | 1 |
            # +---+---+---+
            # | p | x | 4 |
            # +---+---+---+
            # | 5 | 2 | 7 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 2)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 2)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos - 2 and move_x == player_x_pos + 1:  # Pos 1
            # Start the run going North-East
            # +---+---+---+
            # | 6 | 1 | 4 |
            # +---+---+---+
            # | 3 | x | 7 |
            # +---+---+---+
            # | p | 5 | 2 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos, player_x_pos + 2)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos + 2)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 2)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos - 2 and move_x == player_x_pos - 1:  # Pos 1
            # Start the run going North-West
            # +---+---+---+
            # | 1 | 4 | 7 |
            # +---+---+---+
            # | 6 | x | 2 |
            # +---+---+---+
            # | 3 | p | 5 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos - 1, player_x_pos + 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 1)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 2, player_x_pos + 1)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos - 1 and move_x == player_x_pos - 2:  # Pos 1
            # Start the run going West-North
            # +---+---+---+
            # | 1 | 6 | 3 |
            # +---+---+---+
            # | 4 | x | p |
            # +---+---+---+
            # | 7 | 2 | 5 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 2)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 2)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos + 1 and move_x == player_x_pos - 2:  # Pos 1
            # Start the run going West-South
            # +---+---+---+
            # | 7 | 2 | 5 |
            # +---+---+---+
            # | 4 | x | p |
            # +---+---+---+
            # | 1 | 6 | 3 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 2)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos - 1, player_x_pos - 2)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos + 2 and move_x == player_x_pos - 1:  # Pos 1
            # Start the run going South-West
            # +---+---+---+
            # | 3 | p | 5 |
            # +---+---+---+
            # | 6 | x | 2 |
            # +---+---+---+
            # | 1 | 4 | 7 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 1)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos + 1)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

        if move_y == player_y_pos + 2 and move_x == player_x_pos + 1:  # Pos 1
            # Start the run going South-East
            # +---+---+---+
            # | 5 | p | 3 |
            # +---+---+---+
            # | 2 | x | 6 |
            # +---+---+---+
            # | 7 | 4 | 1 |
            # +---+---+---+
            if not game.move_is_legal((player_y_pos + 1, player_x_pos - 1)):  # Pos 2
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos + 1)):  # Pos 3
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos)):  # Pos 4
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos, player_x_pos - 1)):  # Pos 5
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 1, player_x_pos + 1)):  # Pos 6
                continue
            else:
                sum_jumping_runs += 1
            if not game.move_is_legal((player_y_pos + 2, player_x_pos - 1)):  # Pos 7
                continue
            else:
                sum_jumping_runs += 1
                continue

    return sum_jumping_runs

'''
def get_legitimate_legal_moves(game, player_x_position, player_y_position, player_remaining_moves):
    """

    :param game:
        game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    :param player_x_position:
         x cordinate of the position of player at a given instance in the current game

    :param player_y_position:
         y cordinate of the position of player at a given instance in the current game

         Note: (x,y) = player position

    :param player_remaining_moves:
         Number of remaining moves of player.

    :return: float
           Legitimate number of unique moves player is capable of making if the game
           were to unfold.
    """

    ## since player can always make at least a single move despite symmetry in any direction

    number_of_legitimate_player_moves = 1;

    for move_in_y, move_in_x in player_remaining_moves:

        #End loop once the player has already exhausted the logest moves they can make
        # which is 7 for a 7x7 board.
        if number_of_legitimate_player_moves == 7:

             break

        number_player_moves = 1

        if move_in_y == player_y_position + 1 and move_in_x == player_x_position + 2:

            if not game.move_is_legal((player_y_position - 1, player_x_position + 1 )):

                number_of_legitimate_player_moves = max(number_of_legitimate_player_moves, number_player_moves)

                continue

            else:

                number_player_moves += 1



    return  number_of_legitimate_player_moves

'''




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

            

        ## >1 depth
        elif depth > 1:
            ## depth > 1 Case

            if not legal_moves:

                return max_score

            else:

                max_score, best_move = max([(self.min_value(game.forecast_move(move), depth-1), move) for move in legal_moves])

            return max_score # I could also return best_move in future..

        


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


        ## > 1 Depth

        elif depth > 1:

            if not legal_moves:

                return min_score

            else:

                min_score, best_move = min([(self.max_value(game.forecast_move(move), depth-1), move) for move in legal_moves])

            return min_score # I could also return best_move in future..



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
        


        # Initialised best move & Score so far
        ### Assumning First Player is maximizing player
        best_move = (-1, -1)

        best_score = float('inf')



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
            
            # Actions  Taken required after timeout as needed
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
            
                    
                    
        
       