import pygame
from .constants import GREY, SQUARE_SIZE

class Piece:
    
    PADDING = 5
    OUTLINE = 2
    
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.x = 0
        self.y = 0
        self.calculatePosition()
        
    def calculatePosition(self):
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2 # 
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
        
    def draw(self, screen):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(screen, GREY,(self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(screen, self.color,(self.x, self.y), radius)

    def changeColor(self, other): # a piece can change color if it is outflanked
        self.color = other
        
    def __repr__(self): # avoids printing the actual object refrence name
        return str(self.color)