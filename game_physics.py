import random
from game_variables import Settings as s
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
        
        if (start_index + self.size) >= s.WORLD_SIZE():
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
        
        self.search = np.asarray([0.1] * (s.WORLD_SIZE()))
        self.hit_ships = [] # Coordinates of successful hits
        
        self.arrange_ships(sizes = fleet) 
        
        self.ships_coords = [s.index for s in self.ships]
        self.ships_coords = sum(self.ships_coords, [])

        self.world = np.asarray([0.1] * (s.WORLD_SIZE()))
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
                            self.winner = "Player 1" if self.turn else "Player 0"
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

    def search_and_target_strategy(self):
        
        

        return None


class Engine:
    
    def __init__(self, _game, isHuman1 = True, isHuman0 = True ) -> None:
        self.game = _game
        
        self.player1 = isHuman1
        self.player0 = isHuman0
        
        self.strategy = [self.game.sequential_ai(), self.game.random_ai()]
        

         
        
        pass