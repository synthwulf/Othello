# Name: Ryan Anderson
# Date: 11/9/2025
# Desc: This programs implements the game 'othello' using the python library pygame
#       A player can place down pieces to outflank their opponent to increase their score 
#       A player can win if they have more pieces of their color than the opponents color
#       A player will ALWAYS have the chance to move IF they have availible move.
#       If a player does not have availible moves then their turn is skipped
#       
#       Black []
#       White [[]]
#
#
#       Ex.)        
#           black score: 2
#           white score: 1

#   ---->   [] [[]] [] 
#
#           becomes....
#
#
#           black score: 3
#           white score: 0
#           
#   ---->   [] [] []
#           

#           
#
#
# sources to create this project: 
#   https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window
#   https://www.geeksforgeeks.org/artificial-intelligence/mini-max-algorithm-in-artificial-intelligence
#
#   ## SPACE - to turn MINIMAX ON/TOGGLE
#   ## 0     - to turn ALPHA-BETA PRUNING 
#   ## if MINIMAX is ON then to prorgess to the other players move just left-click and the program will 
#   ### cycle through all possibilities of a given game state and will chose the best move
#
import os
import pygame
from othello.constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE, SQUARE_SIZE #import the constants defined in othello/constants.py
from othello.board import Board
from minimax import minimax_algorithm
from time import *

FPS = 60 # <----  could put this in constants folder but the constants file is specific to the game

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #create the screen

pygame.display.set_caption('Othello') 


#### -------------------- Helper Functions -------------------------

def handleClick(board, row, column, color, valid_moves): ## places the piece on the board if the specified row, coloumn pair is in valid_moves
                                                                # 0 if there are valid moves but none were chosen
    print(valid_moves)
    if (row, column) in valid_moves: ## if the (row, column) is in the list then the piece can be played
        board.placePiece(row, column, color)
        board.findFlanker(row, column, color)
        return True
    elif valid_moves == []:
        return []
    elif valid_moves:
        return  0 # holds the can_move
    #TODO: if there are no valid moves for black then change the turn. Only should be True if valid_moves == []
    
def printScores(board): ## prints the score to the screen by grabbnig the result the winner() in Board
    board.updateScore()
    if board.winner() != False:
        if board.winner() != 0:
            print(f"{"WHITE" if board.winner() == WHITE else "BLACK"} WINS!!!")
            print()
            print("############### FINAL SCORE #############")
            print(f"Black Score: {board.black} White Score: {board.white}")
        else:
            print(" DRAW :( ") # if the 
            print()
            print("############### FINAL SCORE #############")
            print(f"Black Score: {board.black} White Score: {board.white}")
    else:
        print(f"Black Score: {board.black} White Score: {board.white}")
    
def switchTurn(current_color): # changes turns based on the color provided while displaying the current players turn
    
    curTurn =  WHITE if current_color == BLACK else BLACK
    
    print()
    print("======================")
    if curTurn == WHITE:
        print("WHITE's TURN")
    else:
        print("BLACK's TURN")
    print("======================")
    print()
    return curTurn

def getValidMoves(board, color):#-> returns a a list of tuples or returns False
    # Search all possibilities and check to seee if theres availible options
    # if so then highlight only them. If theres not a way to change the color
    # of a piece then switch to the other players turn and check 
    return board.checkAvailible(color)
    


#### --------------------- Main Loop -------------------------

def main():
    pygame.init()
    clock = pygame.time.Clock() # makes the game run at maximum a machine can handle 
    board = Board()
    minimax = minimax_algorithm.Minimax()
    
    AB_PRUNING = False
    DEPTH = 2
    MINIMAX = False
    
    current_color = BLACK
    running = True
    
    #type of player
    black_player = True
    white_player = True
    
    while running:
        
        for event in pygame.event.get():#check for any user inputs
            
            if event.type == pygame.QUIT: # quit game
                running = False
            
            # wait for user input
            if event.type == pygame.MOUSEBUTTONDOWN: 
                
                x, y = pygame.mouse.get_pos()
                
                row = y // SQUARE_SIZE     # normalize the row
                column =  x // SQUARE_SIZE # normalize the column
                
                
                # human player playing black
                if not MINIMAX or (current_color == BLACK and black_player == True):
                    valid_moves = getValidMoves(board, BLACK)
                    # board.highlightSquares(SCREEN, valid_moves)
                    if board.pieceInSpot(row, column) != True:
                        can_move = handleClick(board, row, column, BLACK, valid_moves)
                        if can_move: ## if the player has availible moves
                            current_color = switchTurn(BLACK) # change turns
                        elif can_move == 0: ## if the player has availible moves but did not place in a valid spot then print a error
                            print("Invalid Spot")
                            continue
                        elif can_move == []:  ## if there are no valid moves in the first place for black then just skip turn
                            current_color = switchTurn(BLACK) # change turns anyway
                            print("No Availible Turns for player. Switching Turns")
                        printScores(board) # Display the score to the screen
                
                # human player playing white    
                elif not MINIMAX or (current_color == WHITE and white_player == True):
                    valid_moves = getValidMoves(board, WHITE)
                    if board.pieceInSpot(row, column) != True:
                        can_move = handleClick(board, row, column, WHITE, valid_moves)
                        if can_move: 
                            current_color = switchTurn(WHITE) # change turns
                        elif can_move == 0:
                            print("Invalid Spot")
                            continue
                        else:
                            current_color = switchTurn(WHITE) # change turns anyway
                            print("No Availible moves. Switching Turns")
                        printScores(board) # Display the score to the screen
                
                # AI playing black
                elif MINIMAX and current_color == BLACK and black_player == False:
                    
                    board.curColor = BLACK 
                    if AB_PRUNING:
                        value, best_move = minimax.minimax_with_alpha_beta(board, DEPTH, False, float('-inf'), float('inf'))
                        print(best_move)
                        print("Number of States Examined: " + str(minimax.recordedGameStates))
                        minimax.resetRecordings()
                    else:
                        value, best_move = minimax.minimax(board, DEPTH, False)
                        print(best_move)
                        print("Number of States Examined: " + str(minimax.recordedGameStates))
                        minimax.resetRecordings()
                        
                    if best_move:
                        r, c = best_move
                        board.placePiece(r, c, BLACK)
                        board.findFlanker(r, c,BLACK)
                        current_color = switchTurn(BLACK)
                        print(f"placed a {(r, c)} (eval={value})")
                        
                    else:
                        current_color = switchTurn(BLACK)
                        print("AI has no valid moves. Switching turns.")
                    printScores(board)
                
                # AI playing white    
                elif MINIMAX and current_color == WHITE and white_player == False:
                    
                    board.curColor = WHITE
                    if AB_PRUNING:
                        value, best_move = minimax.minimax_with_alpha_beta(board, DEPTH, True, float('-inf'), float('inf'))
                        print(best_move)
                        print("Number of States Examined: " + str(minimax.recordedGameStates))
                        minimax.resetRecordings()
                    else:
                        value, best_move = minimax.minimax(board, DEPTH, True)
                        print(best_move)
                        print("Number of States Examined: " + str(minimax.recordedGameStates))
                        minimax.resetRecordings()
                        
                    if best_move:
                        r, c = best_move
                        board.placePiece(r, c, WHITE)
                        board.findFlanker(r, c,WHITE)
                        current_color = switchTurn(WHITE)
                        print(f"placed a {(r, c)} (eval={value})")
                        
                    else:
                        current_color = switchTurn(WHITE)
                        print("AI has no valid moves. Switching turns.")
                    printScores(board)
                    
                    
            ### ------------------- keyboard input for AI --------------------------
            elif event.type == pygame.KEYDOWN and not MINIMAX:
                if event.key == pygame.K_SPACE:
                    MINIMAX = True
                    print("AI ON")
                
            elif event.type == pygame.KEYDOWN and MINIMAX:
                if event.key == pygame.K_SPACE:
                    MINIMAX = False
                    AB_PRUNING = False
                    print("AI OFF")
                
                if event.key == pygame.K_0 and not AB_PRUNING:
                    AB_PRUNING = True
                    print("ALPHA-BETA PRUNING ON")
                    
                elif event.key == pygame.K_0 and AB_PRUNING:
                    AB_PRUNING = False
                    print("ALPHA-BETA PRUNING OFF")
                    
                
            # independent key events
            if event.type == pygame.KEYDOWN:
                
                #turn human player playing black off
                if event.key == pygame.K_RIGHT:
                    black_player = False if black_player == True else True
                
                #turn human player playing white off
                if event.key == pygame.K_LEFT:
                    white_player = False if white_player == True else True
                    
                    
                    
            

#### ------------------ drawing ---------------------------------------

        Bscore = board.black 
        Wscore = board.white
        
        board.draw(SCREEN)
        font = pygame.font.SysFont(None, 40)
        font_2 = pygame.font.SysFont(None, 30)
        
        turn_text = font.render(
        f"{'Black' if current_color == BLACK else 'White'}'s Turn ", True, (0, 100, 255)
        )
        white_score = font.render( f"WHITE SCORE: {Wscore}",True,(0,0,200))
        black_score = font.render( f"BLACK SCORE: {Bscore}",True,(0,0,200))
        ai_on_display = font.render( f"MINIMAX: {MINIMAX}",True,(0,200,0))
        abp_on_display = font.render(f"AB-PRUNING: {AB_PRUNING}", True, (0,200,0))
        
        playerB = font_2.render(f"BLACK PLAYER: {"Human" if black_player == True else "AI"}", True, (200,0,0) )
        playerW = font_2.render(f"WHITE PLAYER: {"Human" if white_player == True else "AI"}", True, (200,0,0))

        
        SCREEN.blit(turn_text, (20, 20)) #display the turn
        SCREEN.blit(black_score, (20,750))
        SCREEN.blit(white_score, (550, 750))
        SCREEN.blit(ai_on_display, (535, 20))
        SCREEN.blit(abp_on_display, (535, 60))
        
        SCREEN.blit(playerB, (257, 20))
        SCREEN.blit(playerW, (257, 50))

        
        pygame.display.update() ## update the screen after each loop
        
        
    pygame.quit() # gets rid of the window
        
if __name__ == "__main__": #create the window
    main()
            
            
            
    