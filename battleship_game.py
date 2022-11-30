# Battleship Gameplay
import pygame
import game_variables as s
from game_physics import Player

pygame.init()
pygame.display.set_caption("BATTLESHIP")
WINDOW = pygame.display.set_mode((s.WIDTH, s.HEIGHT))

WINDOW.fill((s.BLACK))


def draw_grid(t=0,l=0):
    for i in range(s.GRID_SIZE*s.GRID_SIZE):
        x = l + i % s.GRID_SIZE * s.SQUARE
        y = t + i // s.GRID_SIZE * s.SQUARE
        block = pygame.Rect(x,y, s.SQUARE, s.SQUARE)
        pygame.draw.rect(WINDOW,s.BLUE, block, width=1)
        
        
        
def draw_ship(player, t=0, l=0):
    for ship in player.ships:
        x = l + ship.col * s.SQUARE
        y = t + ship.row * s.SQUARE
        
        ship_block = pygame.Rect(x+5,y+5, (s.SQUARE if ship.orientation == "V" else s.SQUARE * ship.size)*0.8, (s.SQUARE if ship.orientation == "H" else s.SQUARE * ship.size)*0.8)
        pygame.draw.rect(WINDOW,s.GREEN, ship_block, border_radius=20)
        

player_1 = Player(s.ship_sizes)
player_2 = Player(s.ship_sizes)

# print(player_1.world)
# print(player_2.world)

animation = True
while animation:
    
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            animation = False
        
        if e.type == pygame.KEYDOWN:
            # print(e)

            if e.key == pygame.K_ESCAPE:
                animation = False
            
    # Top Left        
    draw_grid(s.SQUARE, s.SQUARE)
    # Top Right
    draw_grid(s.SQUARE*s.GRID_SIZE+2*s.SQUARE, s.SQUARE)

    # Bottom 
    draw_grid(s.SQUARE, s.SQUARE*s.GRID_SIZE+2*s.SQUARE )
    draw_grid(s.SQUARE*s.GRID_SIZE+2*s.SQUARE , s.SQUARE*s.GRID_SIZE+2*s.SQUARE )
    
    
    
    draw_ship(player_1,s.SQUARE, s.SQUARE)
    draw_ship(player_2, s.SQUARE*s.GRID_SIZE+ 2 *s.SQUARE, s.SQUARE )
    
    pygame.display.flip()
    
pygame.quit()