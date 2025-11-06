# Name: Ryan Anderson
# Date: 10/30/2025
# Desc: This programs implements the game othello using pygame 
#
# sources to create this project: 
#   https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window
#
#
import os
import pygame
from othello.constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE, SQUARE_SIZE #import the constants defined in othello/constants.py
from othello.board import Board

FPS = 60 # <----  could put this in constants folder but the constants file is specific to the game

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #create the screen
pygame.display.set_caption('Othello') 


#### -------------------- Helper Functions -------------------------

def handleClick(board, row, column, color, valid_moves):
    if (row, column) in valid_moves: ## if the (row, column) is in the list then the piece can be played
        board.placePiece(row, column, color)
        board.findFlanker(row, column, color)
        return True
    elif valid_moves:
        return  0 # holds the state
    else:
        return False

def printScores(board): ## debugging
    board.updateScore()
    totalPieces = board.black + board.white
    if totalPieces == 64:
        if board.black > board.white:
            print("BLACK WINS!!!!")
            print()
            print("############### FINAL SCORE #############")
            print(f"Black Score: {board.black} White Score: {board.white}")
        else:
            print("WHITE WINS!!!!")
            print()
            print("############### FINAL SCORE #############")
            print(f"Black Score: {board.black} White Score: {board.white}")
    else:
        print(f"Black Score: {board.black} White Score: {board.white}")
    
def switchTurn(current_color): # changes turns
    
    os.system('cls')
    
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
    
    minimax = False
    current_color = BLACK
    running = True
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():#check for any user inputs
            
            if event.type == pygame.QUIT: # quit game
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # place the piece down according to whose turn it is
                
                x, y = pygame.mouse.get_pos()
                
                row = y // SQUARE_SIZE     # normalize the row
                column =  x // SQUARE_SIZE # normalize the column
                
                if current_color == BLACK:
                    valid_moves = getValidMoves(board, BLACK)
                    if board.pieceInSpot(row, column) != True:
                        state = handleClick(board, row, column, BLACK, valid_moves)
                        if state:
                            current_color = switchTurn(BLACK) # change turns
                        elif state == 0:
                            print("Invalid Spot")
                            continue
                        else:
                            current_color = switchTurn(BLACK) # change turns anyway
                            print("No Availible Turns. Switching Turns")
                            
                    printScores(board) # Display the score to the screen
                    
                elif not minimax and current_color == WHITE:
                    valid_moves = getValidMoves(board, WHITE)
                    if board.pieceInSpot(row, column) != True:
                        state = handleClick(board, row, column, WHITE, valid_moves)
                        if state:
                            current_color = switchTurn(WHITE) # change turns
                        elif state == 0:
                            print("Invalid Spot")
                            continue
                        else:
                            current_color = switchTurn(WHITE) # change turns anyway
                            print("No Availible moves. Switching Turns")
                    
                    printScores(board) # Display the score to the screen
                    
                elif minimax and current_color == WHITE:
                    pass
                    
                ### ------------------- Keyboard Input --------------------------
            elif event.type == pygame.KEYDOWN and not minimax:
                if event.key == pygame.K_SPACE:
                    minimax = True
                    print("AI ON")
            
            elif event.type == pygame.KEYDOWN and minimax:
                if event.key == pygame.K_SPACE:
                    minimax = False
                    print("AI OFF")
                    

        Bscore = board.black 
        Wscore = board.white
        
        board.draw(SCREEN)
        font = pygame.font.SysFont(None, 40)
        

        turn_text = font.render(
        f"{'Black' if current_color == BLACK else 'White'}'s Turn ", True, (0, 100, 255)
        )
        white_score = font.render( f"WHITE SCORE: {Bscore}",True,(0,0,200))
        black_score = font.render( f"BLACK SCORE: {Wscore}",True,(0,0,200))
        ai_toggle = font.render( f"MINIMAX: {minimax}",True,(0,200,0))
        SCREEN.blit(turn_text, (20, 20)) #display the turn
        SCREEN.blit(black_score, (20,750))
        SCREEN.blit(white_score, (550, 750))
        SCREEN.blit(ai_toggle, (550, 20))
        
        pygame.display.update() ## update the screen after each loop
        

        
    pygame.quit() # gets rid of the window
        
if __name__ == "__main__": #create the window
    main()
            
            
            
    