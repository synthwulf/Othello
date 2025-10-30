# Name: Ryan Anderson
# Date: 10/30/2025
# Desc: This programs implements
#

# sources to create this project: 
#   https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window
#
#
import pygame
from othello.constants import SCREEN_HEIGHT, SCREEN_WIDTH #import the constants defined in othello/constants.py
from othello.board import Board

FPS = 60 # <----  could put this in constants folder but the constants file is specific to the game

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #create the screen
pygame.display.set_caption('Othello') #window name

def main():
    running = True
    clock = pygame.time.Clock() # makes the game run at maximum a machine can handle 
    board = Board()
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # place the piece down
                pass
            
        board.draw_squares(SCREEN)
        pygame.display.update() ## update the screen after each loop
        
    pygame.quit() # gets rid of the window
        

        
main() # Create the window

            
            
            
    