import random
import numpy as np
from game_variables import Settings as s
from game_physics import  Ship

class MCTS:
    
    def __init__(self) -> None:
        self.sim_board = []
    
    def simulate_board(self, board, ships):
        # Select a random ship size from remaining ships
        # ship_length = random.choice(ships) 
        
        board = board.reshape((5,5))
        # ship_remaining = ships # Fleet still standing
        self.ship_remaining = [len(k) for k in ships] # Fleet still standing
        
        for i in range(100):
            # Place remaining ships on board in probable places
            for s in ship_remaining:
            
                valid_position = False
                
                while not valid_position:
                    ship = Ship(s)
                    
                    ship_coords = np.unravel_index( ship.index, (5,5))
                    
                    for c in ship_coords:
                        if board[c[0],c[1]] in [0, 100]:
                                valid_position = False
                                break
                        else:
                            valid_position = True
                             
                sim = board.copy()
                sim[list(ship_coords)] += 0.9 # Turns unknowns into knows

                
                self.sim_board.append(sim * 5  if np.count_nonzero(sim == 1.9) else sim)
                
         
    def select_move(self, board, ships):
        
        self.simulate_board(board,ships)
        
        print(self.sim_board)
        
        b = np.sum(self.sim_board)
        b = b - board 
        print(b)
        
        return np.argmax(b[])
        
        
        
        
        
# ships = [2,3,4]
# board = np.asarray([0.1, 1.,  0.1, 0.,  0.1, 0.1, 0.1, 0.1, 0.1, 0.,  0.1, 0.,  0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.,  0.,  0.1, 0.1, 0.1, 0.1, 0 ])
# print("Initial Board")
# print(board.reshape((s.GRID_SIZE,s.GRID_SIZE)))
      
# engine =  MCTS()

# print(engine.select_move(board, ships))
