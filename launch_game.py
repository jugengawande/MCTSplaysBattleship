import battleship_game
from game_variables import Settings as s

gs = input("Enter Grid Size (Recommended size 5 for current fleet of [2,3,3,4]): ")

s.set_grid_size(size = int(gs))

human_1_bool = True if input("Is Player 1 a human player? [T/F]: ") == 'T' else False
if not human_1_bool:
    strat_1 = input("Enter strategy to use [base,tree,rl]: ")
human_0_bool = True if input("Is Player 2 a human player? [T/F]: ") == 'T' else False
if not human_0_bool:
    strat_2 = input("Enter strategy to use [base,tree,rl]: ")


# print(human_1_bool,human_0_bool) 
compete = False
if (human_1_bool and not human_0_bool) or (human_0_bool and not human_1_bool):
    compete = True if input("Do you want to play in compete mode? [T/F]: ") == 'T' else False
    
battleship_game.run_game(human_1_bool, human_0_bool, compete, strat_1, strat_2)