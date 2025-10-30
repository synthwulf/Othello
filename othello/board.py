# This class represents the othello board handles whoese turn it is

import pygame
from .constants import * #TODO: to make things easy for now. May only refer to the variables being used
from .piece import Piece # makes the piece class availible 

class Board:
    def __init__(self):
        self.board = []
        self.black = 2 # initial pieces in the center of the board
        self.white = 2
        self.createBoard() 
        
    def drawSquares(self, screen):
        screen.fill(BACKGROUND_COLOR)
        
    
        screen.fill(BACKGROUND_COLOR) 
        for row in range(ROWS):
            for col in range(COLUMNS):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the coordinates of where the next square will be placed
                pygame.draw.rect(screen, BLACK, rect, 1)  #make a thin border around the square and make a border around it


    def createBoard(self):
        for row in range(ROWS):
            self.board.append([]) #-> this is a 2D array of Pieces and integers that are 0 (which indicate empty space)  
            for column in range(COLUMNS):
                if row == 3 and column == 3:
                    self.board[row].append(Piece(row, column, WHITE))
                elif row == 3 and column == 4:
                    self.board[row].append(Piece(row, column, BLACK))
                elif row == 4 and column == 3:
                    self.board[row].append(Piece(row, column, BLACK))
                elif row == 4 and column == 4:
                    self.board[row].append(Piece(row, column, WHITE))
                else:
                    self.board[row].append(0) # 0 indicates that the spot on the board is empty
                    
    def draw(self, screen):
        self.drawSquares(screen)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(screen)