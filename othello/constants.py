import pygame

# __init__.py tells us that the folder that it actually a python package therefore we can import specific things from it

# --- screen dimensions ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# --- board dimensions
ROWS = 8
COLUMNS  = 8
SQUARE_SIZE = (SCREEN_WIDTH//COLUMNS)


# --- pieces (in rgb) ----
BLACK = (0,0,0)
WHITE = (255,255,255)

# --- indicator (shows availible moves) ----
BLUE = (0,0,255) #indicates availible moves for the player
CUBE_COLOR = (200, 0, 0)

# --- board color ---
BACKGROUND_COLOR = (223, 208, 192)


