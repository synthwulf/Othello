# This class represents the othello board handles whoese turn it is

import pygame
from .constants import * 

class Board:
    def __init__(self):
        self.board = []
        self.black = 2 # initial pieces in the center of the board
        self.white = 2
        
    def draw_squares(self, screen):
        screen.fill(BACKGROUND_COLOR)
        
    
        screen.fill(BACKGROUND_COLOR) 
        for row in range(ROWS):
            for col in range(COLUMNS):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the coordinates of where the next square will be placed
                pygame.draw.rect(screen, BLACK, rect, 1)  #make a thin border around the square and make a border around it



