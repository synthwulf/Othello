import pygame
from .constants import *
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.black = 2
        self.white = 2
        self.curColor = BLACK
        self.last_move = None
        self.createBoard()
    
    def drawSquares(self, screen):
        screen.fill(BACKGROUND_COLOR) 
        for row in range(ROWS):
            for col in range(COLUMNS):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])  
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
                    self.board[row].append(0)
                    
    def pieceInSpot(self, row, column):
        return isinstance(self.board[row][column], Piece)
    
    
    def draw(self, screen):
        self.drawSquares(screen)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(screen)
                    
    def placePiece(self, row, column, color):
        piece = Piece(row, column, color)
        if self.board[row][column] == 0:
            self.board[row][column] = piece
            self.last_move = (row, column)
            if color == BLACK: 
                self.black += 1
            elif color == WHITE:
                self.white += 1

    def flipPieces(self, direction, steps, rows, columns):
        dy, dx = direction ## get the value of the directino
        r, c = rows + dy, columns + dx #r and c represent the
        for _ in range(steps):
            piece = self.board[r][c]
            self.board[r][c].changeColor()
            if piece.color == BLACK:
                self.black -= 1
                self.white += 1
            else:
                self.white -= 1
                self.black += 1
            r += dy
            c += dx
    
    def collectValidMoves(self, row, column, color):
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]
        
        valid_moves = []
        if self.board[row][column] != 0: # checks only spaces
            return False
        
        for dy, dx in directions: # search around the piece for other pieces
            r, c = row + dy, column + dx #  check the space around the given spot with the given direcition vector
            if (0 <= r < ROWS and 0 <= c < COLUMNS):
                if self.pieceInSpot(r, c) and self.board[r][c].color != color:
                    steps = self.move((dy, dx), row, column, color)
                    if steps > 0:
                        valid_moves.append((row, column))
                        # break
                        
        return valid_moves if valid_moves else False
    
    def checkAvailible(self, color):
        result = []
        for r in range(ROWS):
            for c in range(COLUMNS):
                moves = self.collectValidMoves(r, c, color)
                if moves and (r, c) not in result:
                    result.append((r, c))
        return result
    
    def move(self, direction, row, column, color):
        dy, dx = direction
        r, c = row + dy, column + dx
        steps = 0
        while (0 <= r < ROWS and 0 <= c < COLUMNS):
            if self.board[r][c] == 0:
                return 0
            elif not self.pieceInSpot(r, c):
                    return 0
            elif self.board[r][c].color == color:
                return steps if steps > 0 else 0
                # if the space is not empty
                # if the piece is not sames as the will be placed piece color
            else:
                r += dy                 # walk to that piece and check
                c += dx 
                steps += 1
        return 0 

    def findFlanker(self, rows, columns, color):
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
            "upL": (-1, -1),
            "upR": (-1, 1),
            "downL": (1, -1),
            "downR": (1, 1)
        }
        for val in directions.values():
            steps = self.move(val, rows, columns, color)
            if steps:   
                self.flipPieces(val, steps, rows, columns)
                
    def evaluate(self): # returns a value that will be used by minimax
                        # corner pieces are perfered
        return self.white - self.black
    
    def winner(self):
        self.updateScore()
        if (self.white + self.black == 64):
            if self.white > self.black:
                return self.white
            elif self.white < self.black:
                return self.black
            else:
                return 0
        else:
            return False

    def updateScore(self):
        self.black = 0
        self.white = 0
        for row in self.board:
            for cell in row:
                if isinstance(cell, Piece):
                    if cell.color == BLACK:
                        self.black += 1
                    else: 
                        self.white += 1