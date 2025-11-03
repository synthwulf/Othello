# Name: Ryan Anderson
# Date: 10/30/2025
# Desc: This programs implements
#
# sources to create this project: 
#   https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window
#
#
import pygame
from othello.constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE, SQUARE_SIZE #import the constants defined in othello/constants.py
from othello.board import Board

FPS = 60 # <----  could put this in constants folder but the constants file is specific to the game

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #create the screen
pygame.display.set_caption('Othello') 

def main():
    running = True
    clock = pygame.time.Clock() # makes the game run at maximum a machine can handle 
    board = Board()
    
    black_player_turn = True
    white_player_turn = False
    
    while running:
        clock.tick(FPS)
        
        #check for any user inputs
        for event in pygame.event.get():
            
            # quit game
            if event.type == pygame.QUIT:
                running = False
            
            # place piece
            if event.type == pygame.MOUSEBUTTONDOWN: # place the piece down according to whose turn it is
                row, column = pygame.mouse.get_pos()
                
                # TODO: make a function that checks for valid moves
                
                # normalize the positions
                row = row // SQUARE_SIZE 
                column =  column // SQUARE_SIZE 
                
                print(f"Mouse clicked at: ({row},{column})")
                
                if black_player_turn:
                    # place the black piece down 
                    board.placePiece(SCREEN, row, column, BLACK)
                    board.findFlanker(row, column, BLACK)
                    
                    
                    # change turns
                    black_player_turn = False
                    white_player_turn = True
                    
                    
                elif white_player_turn:
                    # place the white piece down
                    board.placePiece(SCREEN, row, column, WHITE)
                    board.findFlanker(row, column, WHITE)
                    
                    
                    
                    # change turns
                    white_player_turn = False
                    black_player_turn = True
                    
            
        board.draw(SCREEN)
        pygame.display.update() ## update the screen after each loop
        
    pygame.quit() # gets rid of the window
        

main() # Create the window

            
            
            
    