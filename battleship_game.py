# Battleship Gameplay
import pygame
import random
import numpy as np

from game_variables import Settings as s
# from game_physics import Game
import engine 


HUMAN_1 = True
HUMAN_0 = False

WINDOW = None
game = None

def draw_grid(l=0,t=0, search_grid = False, player = None):
    # No check introduced if player not given incase search grid is true
    
    # font = pygame.font.SysFont("Calibri", 16)
    # text = font.render(player.name,True,(255,255,255))
    # WINDOW.blit(text, (l - 80, t-25))

    global WINDOW, game
    
    world = [y for x in player.ShipGrid.getBoard() for y in x ]
    search = [y for x in player.SearchGrid.getBoard() for y in x]

    
    for i in range(s.WORLD_SIZE()):
            
        x = l + i % s.GRID_SIZE * s.SQUARE
        y = t + i // s.GRID_SIZE * s.SQUARE
        
        # Grid 
        block = pygame.Rect(x,y, s.SQUARE, s.SQUARE)
        pygame.draw.rect(WINDOW, s.GREY_1 , block, width = 1)
        
        if not search_grid:
            if world[i] == 1:
                pygame.draw.circle(WINDOW, s.ORANGE , (x+s.SQUARE//2, y+s.SQUARE//2), s.SQUARE//5 )
            
            if world[i] == 100:

                block = pygame.Rect(x+s.SQUARE//8,y+s.SQUARE//8, s.SQUARE-s.SQUARE//8, s.SQUARE-s.SQUARE//8)
                # block = pygame.Rect(x+s.SQUARE,y+s.SQUARE, s.SQUARE-s.SQUARE, s.SQUARE-s.SQUARE)
                pygame.draw.rect(WINDOW, s.GREY_1 , block, border_radius = s.SQUARE//6 )
            

        if search_grid:
            # block = pygame.Rect(x+5,y+5, s.SQUARE*0.8, s.SQUARE*0.8)
            # pygame.draw.rect(WINDOW, s.search_colors[player.search[i]] , block)
            
            # Mark search effort on our grid
            pygame.draw.circle(WINDOW, s.search_colors[search[i]] , (x+s.SQUARE//2, y+s.SQUARE//2), s.SQUARE//4 if search[i] == 0 else s.SQUARE//3 )
    
    
    # Outer Box
    block = pygame.Rect(l,t, s.SQUARE*s.GRID_SIZE, s.SQUARE*s.GRID_SIZE)
    pygame.draw.rect(WINDOW,s.PINK if player.name == "Human" else s.NEON, block, width=1)
    if search_grid: pygame.draw.rect(WINDOW, s.GREY_2, block, width=1)   

        
def draw_ship(player, l=0, t=0):

    global WINDOW, game
    
    coords = []
    
    for sh in player.ships:
        coords.extend(sh.shipCoordinates)
        
    # print(coords)
    for c in coords:

        x = l + c[1] * s.SQUARE
        y = t + c[0] * s.SQUARE

        # ship_block = pygame.Rect(x+s.SQUARE//6,y+s.SQUARE//6, (s.SQUARE if ship.orientation == "V" else s.SQUARE * ship.size)-s.SQUARE//3, (s.SQUARE if ship.orientation == "H" else s.SQUARE * ship.size)-s.SQUARE//3)
        ship_block = pygame.Rect(x+s.SQUARE//6,y+s.SQUARE//6, s.SQUARE*2//3, s.SQUARE*2//3 )
        pygame.draw.rect(WINDOW,s.YELLOW, ship_block, width = 1, border_radius=10)
        
            
def run_game(human_1_bool, human_0_bool, view_opponent, strategy_1=None, strategy_2=None):  
    
    global WINDOW
    

    
    models = {
        5 : 'models/final/5/1500000',
        7 : 'models/final/7/1400000',
        10 : 'models/final/10/1300000',
        12 : 'models/final/12/1200000',
        15 : 'models/final/15/1100000'
    }
    
    if strategy_1 == 'rl' or strategy_2 == 'rl':
        
        game = engine.Game(s.GRID_SIZE, model= models[s.GRID_SIZE])
        
        
    else:
        game = engine.Game(s.GRID_SIZE )
        
    
    
    
    compete_mode = view_opponent

    pygame.init()
    pygame.display.set_caption("BATTLESHIP")

    WINDOW = pygame.display.set_mode(s.GRID_DIM() if not compete_mode else s.COMPETE_GRID_DIM(), flags=pygame.SRCALPHA)


    WINDOW.fill((s.BLACK))

    # game = engine.Game(human_1_bool, human_0_bool)

    animation = True

    while animation:
        
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                animation = False
                break
            
            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_ESCAPE:
                    animation = False
                    break
                    
                if e.key == pygame.K_SPACE:
                    if strategy_1 == 'rl' or strategy_2 == 'rl':                
                        game = engine.Game(s.GRID_SIZE, model= models[s.GRID_SIZE])                        
                    else:
                        game = engine.Game(s.GRID_SIZE )                
                    break
                
                # if e.key == pygame.K_s:
                #     print(game.player_1.search)
                    
            
        if not game.player_1.winner and not game.player_2.winner:
            
    
            if human_1_bool  or human_0_bool:
                    
                    
                if e.type == pygame.MOUSEBUTTONDOWN:
                    

                    x, y = pygame.mouse.get_pos()
                    if (x > s.SQUARE * (s.GRID_SIZE+2) and x < s.SQUARE * (2*s.GRID_SIZE+2)) :
                        
                        if ((game.turn == True and y > s.SQUARE and y < s.SQUARE*(s.GRID_SIZE+1)) \
                            or (game.turn == False and y > s.SQUARE * (s.GRID_SIZE+2) and y < s.SQUARE * (2*s.GRID_SIZE+2))) :
                            
                            row = (y // s.SQUARE) - (1 if game.turn else ( 2 + s.GRID_SIZE) )
                            col = (x // s.SQUARE) - (2 + s.GRID_SIZE)
                            # print(row,col)

                            game.makeMove(tr = (row,col))
                            # if r == 100 : WINDOW.fill(s.BLACK)   
                    
                # else:
                #     print("Comp Turn")
                
            if not human_1_bool and game.turn:
                game.makeMove(st = strategy_1)
            
            if not human_0_bool and not game.turn:
                game.makeMove(st = strategy_2)
                        
                    
            window_pos = [s.SQUARE, s.SQUARE*s.GRID_SIZE+2*s.SQUARE ]

            WINDOW.fill(s.BLACK)
            # Upper Player
            draw_grid(window_pos[0], window_pos[0], False, game.player_1)
            draw_grid(window_pos[1], window_pos[0], True, game.player_1)

            draw_ship(game.player_1,window_pos[0], window_pos[0])


            # Lower Player
            draw_grid(window_pos[0], window_pos[1], False, game.player_2)
            draw_grid(window_pos[1], window_pos[1], True, game.player_2)

            draw_ship(game.player_2, window_pos[0], window_pos[1] )
            
            
            
        else:

            # WINDOW.fill((s.BLACK))

            # font = pygame.font.SysFont("Calibri", 22)
            # text = font.render("GAME OVER",True,s.PINK)
            # WINDOW.blit(text, (s.WIDTH//2-100, s.HEIGHT // 2-20))

            # print("Game finish")
            winner_text =  "Player 1" if game.player_1.winner else "Player 2"  
            winner_text += " destroyed entire enemy fleet! HOOYAH"
            
            font = pygame.font.SysFont("Calibri", 20)
            text = font.render(winner_text ,True,s.ORANGE, s.PURPLE)
            WINDOW.blit(text, ((WINDOW.get_size()[0] - 10*s.SQUARE)//2, WINDOW.get_size()[1] // 2+10))
            
            

        pygame.display.flip()    
        

    pygame.quit()
    
if __name__ == "__main__":
    run_game(True, False, False, strategy_2='tree')