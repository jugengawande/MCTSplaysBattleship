import random
import game_variables as s

import numpy as np


class Ship:
    
    def __init__(self, size):
        self.index = []
        
        while not self.index:
            
            self.row = random.randrange(0,s.GRID_SIZE)
            self.col = random.randrange(0,s.GRID_SIZE)
            
            self.size = size
            
            self.orientation = random.choice(["H", "V"])
            
            self.index = self.calculate_ship_index()
            
        
    def calculate_ship_index(self):
        # Using an 1-D array to represent the grid world
        
        start_index = self.row * s.GRID_SIZE + self.col
        
        if (start_index + self.size) >= s.WORLD_SIZE:
            # print("Invalid start position")
            return []
        
        if self.orientation == "H" and self.col + self.size >= s.GRID_SIZE:
            return []
            
        if self.orientation == "V" and self.row + self.size >= s.GRID_SIZE:
            return []
        
        if self.orientation == "H":
            return [i for i in range(start_index, start_index+self.size)]
        
        elif self.orientation == "V":
            return [start_index + i * s.GRID_SIZE for i in range(self.size)]
        
              
class Player:
    def __init__(self, fleet) -> None:
        self.ships = []
        self.search = [-0.1] * (s.GRID_SIZE*s.GRID_SIZE)
        self.arrange_ships(sizes = fleet) 
        
        self.ships_coords = [s.index for s in self.ships]
        self.ships_coords = sum(self.ships_coords, [])
        
        self.world = np.asarray(["~"] * (s.GRID_SIZE*s.GRID_SIZE))
        self.world[self.ships_coords] = ["S"] * len(self.ships_coords)
        self.world = np.reshape(self.world,(s.GRID_SIZE,s.GRID_SIZE))
         
    def arrange_ships(self, sizes):
        
        for s in sizes:
            
            valid_position = False
           
            
            while not valid_position:
                ship = Ship(s)
                
                for fleet in self.ships:
                    if set(ship.index).intersection(fleet.index):
                        valid_position = False
                        break
                else:
                    valid_position = True
                
            self.ships.append(ship)                    
         
         
class Game:
    def __init__(self) -> None:
        self.player_0 = Player(s.ship_sizes)         
        self.player_1 = Player(s.ship_sizes)         
        
        # Player 0 is False and Player 1 is True
        player_turn = True   # Boolean to keep track of the player 0 or 1
        self.game_over_state = False
        
        
            
# s = Ship(3)
# print(s.orientation)
# print(s.index )

# p = Player ([2,3,4])


# for ship in p.ships:
#     print(ship.index)

# print(p.world)
# print(p.ships_coords)