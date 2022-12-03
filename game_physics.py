import random
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from game_variables import Settings as s

class Ship:
    
    def __init__(self, size):
        self.index = []
        
        while not self.index:
            
            self.row = random.randrange(0,s.GRID_SIZE)
            self.col = random.randrange(0,s.GRID_SIZE)
            
            self.size = size
            
            self.orientation = random.choice(["H", "V", "DL", "DR"])
            
            self.index = self.calculate_ship_index()
            
            if self.index:
                self.ship_coords_2D = np.unravel_index(self.index, (s.GRID_SIZE,s.GRID_SIZE))
                self.ship_coords_2D = list(zip(self.ship_coords_2D[0], self.ship_coords_2D[1]))

    def calculate_ship_index(self):
        # Using an 1-D array to represent the grid world
        
        start_index = self.row * s.GRID_SIZE + self.col
        
        # Out of grid checks
        if (start_index + self.size) >= s.WORLD_SIZE():
            # print("Invalid start position")
            return []
        
        if self.orientation == "H" and self.col + self.size >= s.GRID_SIZE:
            return []
            
        if self.orientation == "V" and self.row + self.size >= s.GRID_SIZE:
            return []
        
        if self.orientation == "DL" and (self.row + self.size - 1  >= s.GRID_SIZE or self.col - self.size + 1 < 0):
            return []
        
        if self.orientation == "DR" and (self.row + self.size - 1  >= s.GRID_SIZE or self.col + self.size -1 >= s.GRID_SIZE):
            return []
        
        
        # Placing valid ships
        if self.orientation == "H":
            return [i for i in range(start_index, start_index+self.size)]
        
        elif self.orientation == "V":
            return [start_index + i * s.GRID_SIZE for i in range(self.size)]
        
        elif self.orientation == "DL":
            return [start_index + i * s.GRID_SIZE - i for i in range(self.size)]
        
        
        elif self.orientation == "DR":
            return [start_index + i * s.GRID_SIZE + i for i in range(self.size)]
        
        
              
class Player:
    def __init__(self, fleet) -> None:
        self.ships = []
        
        self.search = np.asarray([0.1] * (s.WORLD_SIZE()))
        
        self.hit_ships = [] # Coordinates of successful hits
        
        self.arrange_ships(sizes = fleet) 
        
        self.ships_coords = [s.index for s in self.ships]
        self.ships_coords = sum(self.ships_coords, [])
        # print(self.ships_coords)

        
        # self.ships_coords_2D = np.unravel_index(self.ships_coords, (s.GRID_SIZE,s.GRID_SIZE))
        # self.ships_coords_2D = list(zip(self.ships_coords_2D[0], self.ships_coords_2D[1]))
        
        self.ships_coords_2D = [c.ship_coords_2D for c in self.ships]
        self.ships_coords_2D = sum(self.ships_coords_2D, [])
        
        # self.ships_coords_2D = list(zip(self.ships_coords_2D[0], self.ships_coords_2D[1]))
        # print(self.ships_coords_2D)
        
        
        self.world = np.asarray([0.1] * (s.WORLD_SIZE()))
        self.world[self.ships_coords] = [1] * len(self.ships_coords)
        # self.world = np.reshape(self.world,(s.GRID_SIZE,s.GRID_SIZE))
         
    def arrange_ships(self, sizes):
        
        for s in sizes:
            
            valid_position = False
           
            while not valid_position:
                ship = Ship(s)
                
                # Check if the indexes generated intersect with another placed ship
                for fleet in self.ships:
                    if set(ship.index).intersection(fleet.index):
                        valid_position = False
                        break
                    
                    # Check if diagonal ships cross 
                    if fleet.orientation in ["DR", "DL"] and ship.orientation in ["DR", "DL"]: 
                        if max(fleet.index) > max(ship.index) and min(fleet.index) < min(ship.index): 
                            valid_position = False
                            break
                    
                else:
                    valid_position = True
            
   
            self.ships.append(ship)                    
         
         
        
         
class Game:
    def __init__(self, human_player_1, human_player_0) -> None:
        '''
        TODO: 
        Takes a player tuple 
        '''
        
        self.player_0 = Player(s.ship_sizes)         
        self.player_1 = Player(s.ship_sizes)         
        
        # Player 0 is False and Player 1 is True\
        self.turn = True   # Boolean to keep track of the player 0 or 1
        self.ai_turn = True if not human_player_1 else False
        
        self.human_player_1 = human_player_1
        self.human_player_0 = human_player_0
        
        
        self.game_over_state = False
        self.total_hits = 0
        self.total_miss = 0 
        self.winner = None
        
    
    def move (self, coords):
        # Setting the correct player based on turn to avoid multiple input variables 
        
        attacker = self.player_1 if self.turn else self.player_0
        enemy = self.player_0 if self.turn else self.player_1

        if attacker.search[coords] == 0.1: # Only if passed index is unknown make a move
            
            # Check if the passed index is in the enemy ship index list
            if coords in enemy.ships_coords:
                
                attacker.search[coords] = 1       
                attacker.hit_ships.append(coords)
                enemy.world[coords] = -1

                
                # A ship is sunk when the all coordinates of a ship are in the hit array
                for ships in enemy.ships:
                    if all(s in attacker.hit_ships for s in ships.index ):
                        attacker.search[ships.index] = [100] * ships.size
                        
                        enemy.world[ships.index] = -100
                        enemy.ships.remove(ships)
                        # print(enemy.ships)
 
                        
                        # Endgame
                        if len(enemy.ships_coords) == len(attacker.hit_ships):
                            self.game_over_state = True
                            self.total_hits = len(attacker.hit_ships)
                            self.total_miss = np.count_nonzero(attacker.search == 0)
                            self.winner = "Player 1" if self.turn else "Player 2"
                            # print(attacker.name)
                                        
                        break
                        
            else:
                # A miss is set to zero
                attacker.search[coords] = 0
                
            if not self.game_over_state:
                self.turn = not self.turn # Switch turn
                
            if self.turn: self.ai_turn = True if not self.human_player_1 else False
            if not self.turn: self.ai_turn = True if not self.human_player_0 else False


    def random_strategy(self):
        player = self.player_1 if self.turn else self.player_0

        unexplored = [i for i, value in enumerate(player.search) if value == 0.1]
        return random.choice(unexplored)

    def sequential_strategy(self):
        
        player = self.player_1 if self.turn else self.player_0
        
        unexplored = [i for i, value in enumerate(player.search) if value == 0.1]
        return unexplored[0]

    
    def mcts(self):
        
        player = self.player_1 if self.turn else self.player_0
        opponent = self.player_0 if self.turn else self.player_1
        
        engine = MCTS()
        
        return engine.select_move(player.search, opponent.ships )

        

         
class MCTS:
    
    def __init__(self) -> None:
        self.state = None
        self.sim_board = []
    
    def simulate_board(self, BOARD, SHIPS):
        # Select a random ship size from remaining ships
        # ship_length = random.choice(ships) 
        
        self.state = BOARD.copy().reshape((s.GRID_SIZE,s.GRID_SIZE))
        
        self.state[self.state == 100] = 0 # Sunk ships are unaccessible regions
        self.state[self.state == 1] = 10
        self.state[self.state == 0.1] = 1
        
        # ship_remaining = SHIPS # Fleet still standing
        ship_remaining = [k.size for k in SHIPS] # Fleet still standing
        
        
        for i in range(100):
            # Place remaining ships on board in probable places
            # Currently creating 100 sample boards with a ship placed in all possible places
            
            # sim = np.array([0]*s.WORLD_SIZE()).reshape(5,5)
            sim = self.state.copy()
            
            # for s in ship_remaining:
            
            size = random.choice(ship_remaining)
            valid_position = False
            
            while not valid_position:
                ship = Ship(size)   
                             
                for c in ship.ship_coords_2D:
                    
                    # Ship should not be placed in discovered section except hit
                    
                    if sim[c[0],c[1]] in [0, 5]:
                        valid_position = False
                        break
                    
                else:
                    valid_position = True
              
            if valid_position:                
                for c in ship.ship_coords_2D:
                    sim[c[0],c[1]] = 5 # Places a ship in unknown 
            
            # size = random.choice(ship_remaining)
            # unexplored = [i for i, v in enumerate(board.flatten()) if v == 1]
            
            # ship_placed = False
            # while not ship_placed:
                
            #     index = random.choice (unexplored) 
            #     coord = np.unravel_index(index, (5,5) )
            #     orientation = random.choice("H", "V")
                
            #     if orientation == "H":
            #         if (range(index, index+size) in unexplored) and (coord[1]+size < s.GRID_SIZE) 
            #             sim[range(coord[0],coord[0]+size), coord[1]*size] += 5
                
            # print(sim)
        
            self.sim_board.append(sim)
                
         
    def select_move(self, board, ships):
        
        self.simulate_board(board,ships)
        # print(self.sim_board)
        b = sum(self.sim_board)
        # print(b.flatten())
        b = b - self.state * len(self.sim_board) 
        
        # sns.heatmap(b)
        # plt.show()
        # print(b.flatten())
        return np.argmax(b) 


# ships = [2,3,4]
# board = np.asarray([0.1, 1.,  0.1, 0.,  0.1, 0.1, 0.1, 0.1, 0.1, 0.,  0.1, 0.,  0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.,  0.,  0.1, 0.1, 0.1, 0.1, 0 ])
# print("Initial Board")
# print(board.reshape((s.GRID_SIZE,s.GRID_SIZE)))
      
# engine =  MCTS()

# print(engine.select_move(board, ships))




# s =Ship(3)

# print(s.size)
# print(s.orientation)
# print(s.coords)