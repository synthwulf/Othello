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
        for row in range(ROWS):
            for col in range(COLUMNS):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the coordinates of where the next square will be placed
                pygame.draw.rect(screen, BLACK, rect, 1)  #make a thin border around the square and make a border around it


    def createBoard(self): # Places the pieces on the board while setting each blank space as 0
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
                    

    def draw(self, screen): #draw a piece or pieces onto the screen
        self.drawSquares(screen)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(screen)
                    
                    
    def placePiece(self, screen, row, column, color): #place a piece on the screen
        piece = Piece(row, column, color)
        if self.board[row][column] == 0: # if the space is not occupied
            self.board[row][column] = piece
            if color == BLACK: 
                self.black += 1 # increase the count of pieces
            elif color == WHITE:
                self.white += 1 # increase the count of pieces
        else: #TODO: make other edgecases
            pass
        
        
    def flipPieces(self, direction, steps, rows, columns):
        dx, dy = direction
        r, c = rows + dy, columns + dx
        for _ in range(steps):
            self.board[r][c].changeColor()
            r += dy
            c += dx
            
    
    def move(self, direction, rows, columns, color):
        dx, dy = direction
        r, c = rows + dy, columns + dx
        steps = 0  # how many steps in that direction to find the flanker
        
        while 0 <= r < ROWS and 0 <= c < COLUMNS: #if were still inside the boundries
            if self.board[r][c] == 0:
                return 0
            elif self.board[r][c].color == color:
                return steps if steps > 0 else 0
            else:
                r += dy
                c += dx
                steps += 1
        return 0

    def findFlanker(self, rows, columns, color): # perform a horizontal, vertical and diagnol search of the flanker piece which should be a different color
            # we need to find the flanker first, then flip the pieces
            
            directions = {
            "up" : (0,1),
            "down" : (0,-1),
            "left" : (-1,0),
            "right" : (1,0),
            "upL" : (-1,1),
            "upR" : (1,1),
            "downL" : (-1,-1),
            "downR" : (1,-1)
            }
            for dir in directions.values():
                steps = self.move(dir, rows, columns, color)
                if steps:
                    self.flipPieces(dir, steps, rows, columns)
