import pygame
from copy import deepcopy ## allows us to copy the board multiple times
from othello.constants import WHITE, BLACK

def minimax(state, depth, max_player):
    if depth == 0 or state.winner() is not False:           
        return state.evaluate(), None
    
    current_minimax_color = WHITE if max_player else BLACK
    valid_moves = actions(state, current_minimax_color)
    if not valid_moves:
        return state.evaluate(), None

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for action in valid_moves:
            new_state = result(state, action)
            eval_value, _ = minimax(new_state, depth - 1, False)
            if eval_value > max_eval:
                max_eval = eval_value
                best_move = (action[0], action[1])
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for action in valid_moves:
            new_state = result(state, action)
            eval_value, _ = minimax(new_state, depth - 1, True)
            if eval_value < min_eval:
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
