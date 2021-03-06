"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


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
    """
    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")
    
    evaluation_function = 3
    
    if evaluation_function == 1:
        #use an evaluation function of the number of own move vs 2 * opponent moves as described in Lesson 6
        num_my_moves = len(game.get_legal_moves(player))
        num_opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
        
        W = 2.0
        return float(num_my_moves - (W * num_opponent_moves))
    elif evaluation_function == 2:
        #use an evaluation function of the ratio of number of own move to number of free spaces on the board
        num_free_spaces = len(game.get_blank_spaces())
        num_my_moves = len(game.get_legal_moves(player))
        num_opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
        
    
        #return float(num_my_moves/num_free_spaces)  
        if num_opponent_moves == 0:
            return float("inf")
        else:
            #return float(num_free_spaces/num_opponent_moves)  
            return float(num_my_moves/num_opponent_moves)  

    elif evaluation_function == 3:
        #use an evaluation function that weights the available moves based on board position
        #moves in the center of the board are weighted more than the borders

        my_moves = game.get_legal_moves(player)
        opponent_moves = game.get_legal_moves(game.get_opponent(player))

        my_score = 0
        opponent_score = 0

        c_x = game.height / 2
        c_y = game.width / 2

        for m_x, m_y in my_moves:
            if m_x == 0 or m_x == game.height - 1 or m_y == 0 or m_y == game.width - 1:
                my_score += 1.0
            elif m_x > c_x - 2 and m_x < c_x + 2 and m_y > c_y - 2 and m_y < c_y + 2:
                my_score += 3.0
            else:
                my_score += 2.0

        for o_x, o_y in opponent_moves:
            if o_x == 0 or o_x == game.height - 1 or o_y == 0 or o_y == game.width - 1:
                opponent_score += 1.0
            elif o_x > c_x - 2 and o_x < c_x + 2 and o_y > c_y - 2 and o_y < c_y + 2:
                opponent_score += 3.0
            else:
                opponent_score += 2.0

        return (my_score - opponent_score)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

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
        
        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        #a simple opening book move
        if game.move_count == 1:
            return (game.height / 2, game.width / 2)

        #initialize the selected_move  
        my_move = (-1, -1)
        
        #check to see if there any legal move
        if len(legal_moves) == 0:
            return my_move
        
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            #optimize on the search depth and avoid timeouts
            # if self.iterative:
            #     max_depth = len(game.get_blank_spaces())
            # else:
            #     max_depth = self.search_depth
            #
            # if self.iterative:
            #     for depth in range(1, max_depth):
            #         if self.time_left() <= self.TIMER_THRESHOLD:
            #             return my_move
            #
            #         if (self.method == 'minimax'):
            #             my_score, my_move = self.minimax(game, depth)
            #         elif (self.method == 'alphabeta'):
            #             my_score, my_move = self.alphabeta(game, depth)
            #
            # else:
            #     if (self.method == 'minimax'):
            #         my_score, my_move = self.minimax(game, max_depth)
            #     elif (self.method == 'alphabeta'):
            #         my_score, my_move = self.alphabeta(game, max_depth)

            depth = self.search_depth
            if self.iterative:
                depth = 1
                        
            while True:
                if (self.method == 'minimax'):
                    my_score, my_move = self.minimax(game, depth)
                elif (self.method == 'alphabeta'):
                    my_score, my_move = self.alphabeta(game, depth)
            
                if self.iterative:
                    depth += 1
                else:
                    return my_move
                            
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return my_move

        # Return the best move from the last completed search iteration
        return my_move
        
    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        #Mini-Max limited depth psuedocode
        #https://en.wikipedia.org/wiki/Minimax

        recommended_move = (-1, -1)
        
        #check if end of depth bound has been reached or if end of the sub-tree has been reached
        legal_moves = game.get_legal_moves()              
        if depth == 0 or len(legal_moves) == 0:
            return self.score(game, self), recommended_move
            
        #    
        if maximizing_player:
            best_score = float("-inf")
            for attempt_move in legal_moves:
                result_score, result_move = self.minimax(game.forecast_move(attempt_move), depth - 1, False)
                if result_score > best_score:
                    best_score = result_score
                    recommended_move = attempt_move
            
            return best_score, recommended_move
            
        else:
            best_score = float("inf")
            for attempt_move in legal_moves:
                result_score, result_move = self.minimax(game.forecast_move(attempt_move), depth - 1, True)
                if result_score < best_score:
                    best_score = result_score
                    recommended_move = attempt_move
            
            return best_score, recommended_move
                    

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

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

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        #Alpha–beta pruning fail-soft psuedocode
        #https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        recommended_move = (-1, -1)
        
        #check if end of depth bound has been reached or if end of the sub-tree has been reached
        legal_moves = game.get_legal_moves()              
        if depth == 0 or len(legal_moves) == 0:
            return self.score(game, self), recommended_move
            
        #when playing maximizing mode    
        if maximizing_player:
            best_score = float("-inf")
            for attempt_move in legal_moves:
                result_score, result_move = self.alphabeta(game.forecast_move(attempt_move), depth - 1, alpha, beta, False)
                if result_score > best_score:
                    #update the best values
                    best_score = result_score
                    recommended_move = attempt_move
                    alpha = max(alpha, best_score)
                if beta <=  alpha:
                    break

            return best_score, recommended_move
 
        #when playing maximizing mode    
        else:
            best_score = float("inf")
            for attempt_move in legal_moves:
                result_score, result_move = self.alphabeta(game.forecast_move(attempt_move), depth - 1, alpha, beta, True)
                if result_score < best_score:
                    #update the best values
                    best_score = result_score
                    recommended_move = attempt_move
                    beta = min(beta, best_score)
                if beta <=  alpha:
                    break
                
            return best_score, recommended_move
