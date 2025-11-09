import pygame
from copy import deepcopy ## allows us to copy the current boatd state
from othello.constants import WHITE, BLACK

def minimax_with_alpha_beta(state, depth, max_player, alpha, beta): ## returns the best possible move of a current board state after searching a specified depth 
    if depth == 0 or state.winner() is not False:  
        return state.evaluate(), None
    
    current_minimax_color = WHITE if max_player else BLACK ## I consider white to be the maximizing player and black to be the minimizing player by default 
                                                            ## should be able to change and still work
    valid_moves = actions(state, current_minimax_color)
    
    if not valid_moves:
        return state.evaluate(), None

    if max_player:
        max_eval = float('-inf')# collect any move
        best_move = None
        for action in valid_moves:
            new_state = result(state, action) # get the state after perfoming the move
            eval_value, _ = minimax_with_alpha_beta(new_state, depth - 1, False, alpha, beta) # get the eval value from that move
            max_eval = max(alpha, eval_value)
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break
        best_move = (action[0], action[1]) # after going througha all possibllites
        return max_eval, best_move

    else:
        min_eval = float('inf') # opposite logic
        best_move = None
        for action in valid_moves:
            new_state = result(state, action)
            eval_value, _ = minimax_with_alpha_beta(new_state, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval_value)
            beta = min(beta, eval_value)
            if beta <= alpha:
                break
        best_move = (action[0], action[1])
        return min_eval, best_move

def minimax(state, depth, max_player):
    if depth == 0 or state.winner() is not False:
        return state.evaluate(), state # if we are at the last node in the tree then lets get the value of the node in that tree
    
    current_minimax_color = WHITE if max_player else BLACK ## I consider white to be the maximizing player and black to be the minimizing player by default 
                                                            ## should be able to change and still work
    valid_moves = actions(state, current_minimax_color)
    
    if not valid_moves:
        return state.evaluate(), None
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for action in valid_moves:
            new_state = result(state, action)
            eval_value, _ = minimax(new_state, depth - 1, False) ## we only worry about the state that gives the higest value
            if eval_value > max_eval: # if the next move yeilds a loewer eval then we choose that move
                max_eval = eval_value
                best_move = (action[0], action[1])
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        for action in valid_moves: 
            new_state = result(state, action)
            eval_value, _ = minimax(new_state, depth - 1, True) ## we only worry about the state that gives the loewst value within
            if eval_value < min_eval: # if the next move yeilds a loewer eval then we choose that move
                min_eval = eval_value
                best_move = (action[0], action[1])
        return min_eval, best_move


def result(state, action): # resulting state from taking action a in state s
    new_state = deepcopy(state) # create a new board that represents what happens if you take a move
    new_state.placePiece(action[0], action[1] , state.curColor)
    new_state.findFlanker(action[0], action[1], state.curColor)
    newColor = WHITE if state.curColor == BLACK else BLACK   # manually switch the color 
    new_state.curColor = newColor
    new_state.last_move = (action[0], action[1])
    return new_state

def actions(state, color): #returns all possible valid moves from the current board
    return state.checkAvailible(color)





