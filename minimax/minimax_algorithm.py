import pygame
from copy import deepcopy ## allows us to copy the board multiple times
from othello.constants import WHITE, BLACK

def minimax(state, depth, max_player):
    if depth == 0 or state.winner != None:
        return state.evaluate(), state # if we are at the last node in the tree then lets get the value of the node in that tree
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for action in actions(state): 
            eval, _ = minimax(result(state, action), depth - 1, False) ## we only worry about the state that gives the higest value
            if eval > max_eval: # if the next move yeilds a loewer eval then we choose that move
                max_eval = eval
                best_move = action
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        for action in actions(state): 
            eval, _ = minimax(result(state, action), depth - 1, True) ## we only worry about the state that gives the loewst value within
            if eval < min_eval: # if the next move yeilds a loewer eval then we choose that move
                min_eval = eval
                best_move = action
        return min_eval, best_move

def result(state, action): # resulting state from taking action a in state s
    new_state = deepcopy(state) # create a new board that represents what happens if you take a move
    new_state.placePiece(action[0], action[1] , state.color)
    new_state.findflanker(action[0], action[1], state.color)
    return new_state

def actions(state, color): #returns all possible valid moves from the current board
    return state.checkAvailible(color)
