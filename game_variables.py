
# Grid Variables
SQUARE = 50
GRID_SIZE = 7
WORLD_SIZE = GRID_SIZE * GRID_SIZE

# Display Window
WIDTH = SQUARE * GRID_SIZE * 2 + 3 * SQUARE
HEIGHT = SQUARE * GRID_SIZE * 2 + 3 * SQUARE
# HEIGHT = SQUARE * GRID_SIZE + 2 * SQUARE

#Theme Colors
BLACK = (9, 11, 11)
BLUE = (70,172,194)
ORANGE = (205, 83, 52)
YELLOW = (247, 179, 43,255)
GREEN = (189, 191, 9)
NAVY = (4, 36, 57, 150)

GREY_1 = (18, 22, 22)
GREY_2 = (67, 86, 96)
GREY_3 = (37, 45, 45)

PINK = (140, 33, 85)
PURPLE = (57, 43, 88)

NEON = (49, 203, 0)

# Fleet 

ship_sizes = [2,3,3,4]

search_colors = {
    0.1 : BLACK,
    1 : YELLOW,
    0 : NAVY ,
    100: ORANGE,
}