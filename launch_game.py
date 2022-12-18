import battleship_game
from game_variables import Settings as s

valid = False
while not valid: 
    gs = input("Enter Grid Size [5,7,10,12,15]: ")
    
    
    if int(gs) in [5,7,10,12,15]:
        s.GRID_SIZE = int(gs)
        valid = True

strat_1 = None
strat_2 = None


human_1_bool = True if input("Is Player 1 a human player? [T/F]: ") == 'T' else False

valid = False
while not valid and not human_1_bool: 
    if not human_1_bool:
        strat_1 = input("Enter strategy to use [base,tree,rl]: ")
        if strat_1 in ['base','tree','rl']: valid = True
    
    
human_0_bool = True if input("Is Player 2 a human player? [T/F]: ") == 'T' else False

valid = False
while not valid and not human_0_bool: 
    if not human_0_bool:
        strat_2 = input("Enter strategy to use [base,tree,rl]: ")
        if strat_2 in ['base','tree','rl']: valid = True

# print(human_1_bool,human_0_bool) 
compete = False
if (human_1_bool and not human_0_bool) or (human_0_bool and not human_1_bool):
    compete = True if input("Do you want to play in compete mode? [T/F]: ") == 'T' else False
    
battleship_game.run_game(human_1_bool, human_0_bool, compete, strat_1, strat_2)