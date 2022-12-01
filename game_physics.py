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
    def __init__(self, fleet, name="Commander") -> None:
        self.name = name
        self.ships = []
        
        self.search = np.asarray([0.1] * (s.GRID_SIZE*s.GRID_SIZE))
        self.hit_ships = [] # Coordinates of successful hits
        
        self.arrange_ships(sizes = fleet) 
        
        self.ships_coords = [s.index for s in self.ships]
        self.ships_coords = sum(self.ships_coords, [])

        self.world = np.asarray([0.1] * (s.GRID_SIZE*s.GRID_SIZE))
        self.world[self.ships_coords] = [1] * len(self.ships_coords)
        # self.world = np.reshape(self.world,(s.GRID_SIZE,s.GRID_SIZE))
         
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
    def __init__(self, player_0_name=None, player_1_name=None) -> None:
        '''
        TODO: 
        Takes a player tuple 
        '''
        
        
        self.player_0 = Player(s.ship_sizes, player_0_name)         
        self.player_1 = Player(s.ship_sizes, player_1_name)         
        
        # Player 0 is False and Player 1 is True\
        self.player_turn = True   # Boolean to keep track of the player 0 or 1
        self.game_over_state = False
        
    
    def move (self, coords) -> int:
        # Setting the correct player based on turn to avoid multiple input variables 
        
        attacker = self.player_1 if self.player_turn else self.player_0
        enemy = self.player_0 if self.player_turn else self.player_1

        if attacker.search[coords] == 0.1: # Only if passed index is unknown make a move
            
            # Check if the passed index is in the enemy ship index list
            if coords in enemy.ships_coords:
                
                attacker.search[coords] = 1       
                attacker.hit_ships.append(coords)
                enemy.world[coords] = -1
                
                return_value = 1
                
                # A ship is sunk when the all coordinates of a ship are in the hit array
                for ships in enemy.ships:
                    if all(s in attacker.hit_ships for s in ships.index ):
                        attacker.search[ships.index] = [100] * ships.size
                        
                        enemy.world[ships.index] = -100
                        enemy.ships.remove(ships)
                        # print(enemy.ships)
                        return_value = 100
                        
                        # Endgame
                        if len(enemy.ships_coords) == len(attacker.hit_ships):
                            self.game_over_state = True
                            # print(attacker.name)
                            return -1
                                    
                        break
                        
            else:
                # A miss is set to zero
                attacker.search[coords] = 0
                return_value = 0 
                
            if not self.game_over_state:
                self.player_turn = not self.player_turn # Switch turn
            
            return return_value
            


    def random_strategy(self):
        player = self.player_1 if self.player_turn else self.player_0

        unexplored = [i for i, value in enumerate(player.search) if value == 0.1]
        return random.choice(unexplored)

    def sequential_strategy(self):
        
        player = self.player_1 if self.player_turn else self.player_0
        
        unexplored = [i for i, value in enumerate(player.search) if value == 0.1]
        return unexplored[0]

    def search_and_target_strategy(self):
        return None

