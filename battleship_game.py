# Battleship Gameplay
import pygame
import random
import game_variables as s
from game_physics import Game

pygame.init()
pygame.display.set_caption("BATTLESHIP")
WINDOW = pygame.display.set_mode((s.WIDTH, s.HEIGHT))

font = pygame.font.SysFont("Calibri", 16)

WINDOW.fill((s.BLACK))


def draw_grid(l=0,t=0, search_grid = False, player = None):
    # No check introduced if player not given incase search grid is true

        
    for i in range(s.GRID_SIZE*s.GRID_SIZE):
            
        x = l + i % s.GRID_SIZE * s.SQUARE
        y = t + i // s.GRID_SIZE * s.SQUARE
        
        if not search_grid:
            if player.world[i] == -1:
                pygame.draw.circle(WINDOW, s.ORANGE , (x+s.SQUARE//2, y+s.SQUARE//2), s.SQUARE//5 )
            
            if player.world[i] == -100:
                block = pygame.Rect(x+s.SQUARE//8,y+s.SQUARE//8, s.SQUARE-s.SQUARE//4, s.SQUARE-s.SQUARE//4)
                pygame.draw.rect(WINDOW, s.GREY_1 , block, border_radius = s.SQUARE//5 )
            

        if search_grid:
            text = font.render(player.name,True,(255,255,255))
            WINDOW.blit(text, (l - 80, t-25))
            
            # block = pygame.Rect(x+5,y+5, s.SQUARE*0.8, s.SQUARE*0.8)
            # pygame.draw.rect(WINDOW, s.search_colors[player.search[i]] , block)
            
            # Mark search effort on our grid
            pygame.draw.circle(WINDOW, s.search_colors[player.search[i]] , (x+s.SQUARE//2, y+s.SQUARE//2), s.SQUARE//4 if player.search[i] == 0 else s.SQUARE//3 )
            
            # Mark successful effort by enemy

        # Grid 
        block = pygame.Rect(x,y, s.SQUARE, s.SQUARE)
        pygame.draw.rect(WINDOW, s.GREY_1 , block, width = 1)
        
        
    # Outer Box
    block = pygame.Rect(l,t, s.SQUARE*s.GRID_SIZE, s.SQUARE*s.GRID_SIZE)
    pygame.draw.rect(WINDOW,s.PINK if player == game.player_1 else s.NEON, block, width=1)
    if search_grid: pygame.draw.rect(WINDOW, s.GREY_2, block, width=1)
        

# def draw_search_grid(player, t=0,l=0):     

#     for i in range(s.GRID_SIZE*s.GRID_SIZE):
#         x = l + i % s.GRID_SIZE * s.SQUARE
#         y = t + i // s.GRID_SIZE * s.SQUARE
        
#         block = pygame.Rect(x,y, s.SQUARE, s.SQUARE)
#         pygame.draw.rect(WINDOW, s.search_colors[player.search[i]] , block, width=1)
        
def draw_ship(player, l=0, t=0):
    for ship in player.ships:
        x = l + ship.col * s.SQUARE
        y = t + ship.row * s.SQUARE
        
        ship_block = pygame.Rect(x+s.SQUARE//6,y+s.SQUARE//6, (s.SQUARE if ship.orientation == "V" else s.SQUARE * ship.size)-s.SQUARE//3, (s.SQUARE if ship.orientation == "H" else s.SQUARE * ship.size)-s.SQUARE//3)
        pygame.draw.rect(WINDOW,s.YELLOW, ship_block, width = 1, border_radius=20)
        

# player_1 = Player(s.ship_sizes)
# player_2 = Player(s.ship_sizes)

game = Game("Human 0","Human 1")

# game.player_1.search[[2,4,5,6,7]] = [0,0,100,100,1]
# game.player_0.search[[7,12,1]] = [1,1,0]


animation = True
while animation:
    
    
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            animation = False
        
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                animation = False

    
    if not game.game_over_state:
        
        if game.player_turn:
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (x > s.SQUARE * (s.GRID_SIZE+2) and x < s.SQUARE * (2*s.GRID_SIZE+2)) and ((game.player_turn == True and y > s.SQUARE and y < s.SQUARE*(s.GRID_SIZE+1)) or (game.player_turn == False and y > s.SQUARE * (s.GRID_SIZE+2) and y < s.SQUARE * (2*s.GRID_SIZE+2))) :
                    row = (y // s.SQUARE) - (1 if game.player_turn else ( 2 + s.GRID_SIZE) )
                    col = (x // s.SQUARE) - (2 + s.GRID_SIZE)
                    # print(row,col)
                    
                    # Make a move
                    
                    index = row * s.GRID_SIZE + col
                    game.move(index)
            
        else:  
            #Random Player
            index = random.randrange(s.GRID_SIZE*s.GRID_SIZE)
            game.move(index)
            
            
        WINDOW.fill((s.BLACK)) 
        window_pos = [s.SQUARE, s.SQUARE*s.GRID_SIZE+2*s.SQUARE ]

        draw_grid(window_pos[0], window_pos[0], False, game.player_1)
        draw_grid(window_pos[1], window_pos[0], True, game.player_1)


        # draw_grid(window_pos[0], window_pos[1], False, game.player_0)
        # draw_grid(window_pos[1], window_pos[1], True, game.player_0)

        draw_ship(game.player_1,window_pos[0], window_pos[0])
        # draw_ship(game.player_0, window_pos[0], window_pos[1] )
    
    else:
  
        WINDOW.fill((s.BLACK))

        font = pygame.font.SysFont("Calibri", 22)
        text = font.render("GAME OVER",True,s.PINK)
        WINDOW.blit(text, (s.WIDTH//2-100, s.HEIGHT // 2-20))
        
        winner_text = (game.player_1.name if game.player_turn else game.player_0.name) + " destroyed entire enemy fleet! HOOYAH"
        
        font = pygame.font.SysFont("Calibri", 28)
        text = font.render(winner_text ,True,s.ORANGE)
        WINDOW.blit(text, (s.SQUARE, s.HEIGHT // 2+10))
    
    
    
    pygame.display.flip()    
    

pygame.quit()