import pygame
from .constants import *
from .piece import Piece


#current weights of the board
#corner pieces are more favored thus the higher weight value
WEIGHTS = [
    [120, -20,  20,  5,  5,  20, -20, 120],
    [-20, -40,  -5, -5, -5,  -5, -40, -20],
    [ 20,  -5,  15,  3,  3,  15,  -5,  20],
    [  5,  -5,   3,  1,  1,   3,  -5,   5],
    [  5,  -5,   3,  1,  1,   3,  -5,   5],
    [ 20,  -5,  15,  3,  3,  15,  -5,  20],
    [-20, -40,  -5, -5, -5,  -5, -40, -20],
    [120, -20,  20,  5,  5,  20, -20, 120]
]

class Board:
    def __init__(self):
        self.board = []
        self.black = 2 # value starts at 2 to follow the inital board state
        self.white = 2 # value starts at 2 to follow the inital board state
        self.curColor = BLACK
        self.last_move = None
        self.NumberOfStates = 0
        self.createBoard()
    
    def drawSquares(self, screen):
        screen.fill(BACKGROUND_COLOR) 
        for row in range(ROWS):
            for col in range(COLUMNS):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def createBoard(self): # create the initial board with the initial pieces on the board
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
                    
    def pieceInSpot(self, row, column): # checks to see if there is a piece in a spot the player or AI is trying to play in.
        return isinstance(self.board[row][column], Piece)
    
    def draw(self, screen): #draws pieces onto the board
        self.drawSquares(screen)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(screen)
                    
    def placePiece(self, row, column, color): #places the piece at the specified location
        piece = Piece(row, column, color)
        if self.board[row][column] == 0:
            self.board[row][column] = piece
            self.last_move = (row, column)
            if color == BLACK: 
                self.black += 1
            elif color == WHITE:
                self.white += 1

    def flipPieces(self, direction, steps, rows, columns):
        dy, dx = direction ## get the value of the direction
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
        ###### these can be seen as direction vectors which modified the current spot as (row, column)
        ###### + row -> down 
        ###### - row -> up
        ###### + column -> right
        ###### + column -> left
    
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
        ## weights below can be seen at the amount of importance of a particular action based on the board state
        ## this will be mostly used for the minimax function
        WEIGHT_PIECE = 1.0
        WEIGHT_POS = 4.0
        WEIGHT_MOBILITY = 3.0 
        
        white_pos, black_pos = self.get_piece_score()
        pos_score = (white_pos - black_pos) * WEIGHT_POS
        mob_score = self.get_mobility_score() * WEIGHT_MOBILITY
        piece_score = (self.white - self.black) * WEIGHT_PIECE
        
        final_score = pos_score + mob_score + piece_score
        
        return final_score
    
    def get_piece_score(self): # score calculated by weight at that spot + piece 
        white_weighted_score = 0
        black_weighted_score = 0
        for r in range(ROWS):
            for c in range(COLUMNS):
                piece = self.board[r][c]
                if piece != 0:
                    weight = WEIGHTS[r][c]
                    if piece.color == WHITE:
                        white_weighted_score += weight
                    elif piece.color == BLACK:
                        black_weighted_score += weight
                    
        return white_weighted_score, black_weighted_score
        
    
    def get_mobility_score(self): # get how many available spots the current player has to play and return a heuristic value for that
        black_moves = self.checkAvailible(BLACK)
        white_moves = self.checkAvailible(WHITE)
        
        return len(white_moves) - len(black_moves)
    
    def winner(self): ## returns the current state of the game in the context of winning 
                        # or losing based on who has more pieces
                        # reutrns False if there is no winner
        self.updateScore()
        if (self.white + self.black == 64):
            if self.white > self.black:
                return WHITE
            elif self.white < self.black:
                return BLACK
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
                    
    def calculateHighlightposition (self, row, column):
        r = SQUARE_SIZE * column + SQUARE_SIZE // 2 
        c = SQUARE_SIZE * row+ SQUARE_SIZE // 2
        return r, c
            
                        
    def highlightSquares(self, screen, valid_moves): ## refers to the cvalid list 
        radius = SQUARE_SIZE // 2 
        
        for spot in valid_moves:
            r, c = self.calculateHighlightposition(spot[0], spot[1])
            pygame.draw.circle(screen, BLUE,(r, c), radius)
            pygame.draw.circle(screen, BLUE,(r, c), radius)
        
        
    def clearStoredStates(self):
        self.NumberOfStates = 0
    
    def storeStates(self, number):
        self.NumberOfStates += number