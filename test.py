from game_variables import Settings as s

import numpy as np
import random 
from copy import deepcopy

class Ship:
    
    HORIZONTAL = 0
    VERTICAL = 1
    DL = 2 # Diagonal Left
    DR = 3 # Diagonal Left
    
    ORIENT = ['H', 'V', 'DL', 'DR']

    def __init__(self, size, orientation = None) -> None:
        self.__size = size
        self.__orientation = orientation
        self.hits = 0
        self.__cordinates = None
        self.isSunk = False

    def __repr__(self) -> str:
        return "S(" + str(self.size) + ", " +  str(Ship.ORIENT [self.__orientation])+ ")"
        
    def randomShip(self):
        self.__orientation = random.choice([Ship.HORIZONTAL, Ship.VERTICAL, Ship.DL, Ship.DR])
    
    @property
    def orientation(self):
        return self.__orientation
    
    @property
    def size(self):
        return self.__size
    
    @property
    def shipCoordinates(self):
        return self.__cordinates
    
    @shipCoordinates.setter
    def shipCoordinates(self, v):
        self.__cordinates = v

    def shipHit(self):
        self.hits += 1
        if self.hits == self.size:
            self.isSunk = True
            
    def isSunk(self):
        return self.isSunk


    
class Board:
    
    UNKNOWN = -1
    MISSED = 0
    HIT = 1
    SUNK = 100
    
    
    def __init__(self, GridSize):
        self.length = GridSize
        self.board = [[Board.UNKNOWN] * self.length for _ in range(self.length)]
    

    def getBoard(self):
        return self.board
    
    def isShip(self, row, col):
        if type(self.board[row][col]) == Ship:
            return self.board[row][col]
        else: return False
        
    
    def markHit(self, row, col):
        self.board[row][col] = Board.HIT
            
    def markMiss(self, row, col):
        self.board[row][col] = Board.MISSED
        
    
    def printBoard(self):
        printB = np.array(self.board)
        # printB[printB != -1 ] = 'S'
        # printB[type(printB) is Ship  ] = 'S'
        # printB[printB == -1 ] = '~'
        # print(printB)
        
        for i in  range(self.length):
            # print("\n")
            for j in range(self.length):
                if type(printB[i][j]) == Ship:
                    v = 'S'
                elif printB[i][j] == Board.MISSED:
                    v = '~'
                
                elif printB[i][j] == Board.HIT:
                    v = 'X'
                
                else:
                    v = '.'
                
                print(v, end = " " )
            print()
            
            
    def printDetailBoard(self):
        print(self.board)  



class SearchBoard (Board):    
      
    def markSink(self, ship):
        for c in ship.shipCoordinates():
            row, col = c
            self.board[row][col] == Board.SUNK
        

        
    
class ShipBoard (Board):

    def __init__(self, GridSize):
        super().__init__(GridSize)
        
    
    def placeShip(self, ship, valid_coords): 
        # print(valid_coords,ship)
        ship.shipCoordinates = valid_coords
        for c in valid_coords:
            row, col = c
            self.board[row][col] = ship
                
        
    def validShipCoords(self, ship, row = None, col = None):
        '''
        TODO
        Add custom placing of ships
        '''
        row = random.randrange(0,self.length)
        col = random.randrange(0,self.length)
        valid_coordinates = []
    

        if ship.orientation == Ship.HORIZONTAL:
            if ship.size + col < self.length:
                for i in range(ship.size):
                    if self.board[row][col] == -1:
                        valid_coordinates.append((row, col))
                        col += 1
                    else:
                        return False
                    
        elif ship.orientation == Ship.VERTICAL:
            if ship.size + row < self.length:
                for i in range(ship.size):
                    if self.board[row][col] == -1:
                        valid_coordinates.append((row, col))                   
                        row += 1
                    else:
                        return False

        elif ship.orientation == Ship.DL:
            if row + ship.size - 1  < self.length and col - ship.size + 1 >= 0:
                for i in range(ship.size):
                    if self.board[row][col] == -1:
                        valid_coordinates.append((row, col))                          
                        row += 1
                        col -= 1
                    else:
                        return False
        else: 
            if (row + ship.size - 1  < self.length) and (col + ship.size - 1 < self.length):
                for i in range(ship.size):
                    if self.board[row][col] == -1:
                        valid_coordinates.append((row, col))                         
                        row += 1
                        col += 1
                    else:
                        return False 
                    
        return valid_coordinates

    def markSink(self, ship):
        for c in ship.shipCoordinates:
            row, col = c
            self.board[row][col] = 100


class Player:
    def __init__(self, name, fleet) -> None:
        self.name = name
        self.fleet = fleet
        self.ships = []
        
        self.SearchGrid = SearchBoard(s.GRID_SIZE)
        self.ShipGrid = ShipBoard(s.GRID_SIZE)
        
        self.createFleetMap()
        
        self.winner = False
        
    def createFleetMap(self):

        
        for f in self.fleet:
            placed = False
            while not placed:
                s = Ship(f)
                s.randomShip()
                c = self.ShipGrid.validShipCoords(s)
            
                if c:
                    self.ShipGrid.placeShip(s,c) # Randomizes the orientation of a ship of size 
                    self.ships.append(s)
                    placed = True
        
    def isDefeated(self):

        self.ships = [sh for sh in self.ships if not sh.isSunk]    
        return True if not self.ships else False
    
    def possibleMoves(self):
        y = np.where(np.array(self.SearchGrid.getBoard()) == -1)
        return list(zip(y[0],y[1]))
    
    def score(self):
        miss = np.count_nonzero(np.array(self.SearchGrid.getBoard()) == 0)
        spare = s.WORLD_SIZE() - sum(self.fleet) 
        
        return 1 - (miss/spare)

class Strategy:
    @staticmethod
    def randomPlayer( moves ):
        return random.choice(moves)

    @staticmethod
    def sequentialPlayer(moves):
        return moves[0]


class Game:
    def __init__(self) -> None:
        self.player_1 = Player("Human", s.Fleet)
        self.player_2 = Player("Computer", s.Fleet)

        self.turn = True
        
    def run(self):
        
        while not self.player_1.isDefeated() and not self.player_2.isDefeated():
            

            if self.turn:
                target = Strategy.randomPlayer(self.player_1.possibleMoves())
                # print("Player 1 targeted: ", target)
                Actions.shootTarget(self.player_1, self.player_2, target)
                self.turn = not self.turn
            else:
                target = Strategy.sequentialPlayer(self.player_2.possibleMoves())
                # print("Player 2 targeted: ", target)
                Actions.shootTarget(self.player_2, self.player_1, target)
                self.turn = not self.turn

            
    
    
    def runSimulationMode(self):
        while not self.player_2.isDefeated():
            target = Strategy.sequentialPlayer(self.player_1.possibleMoves())
            
            # print("Player 1 targeted: ", target)
            Actions.shootTarget(self.player_1, self.player_2, target)

      
    def isWinner(self):
        return self.player_1 if self.player_1.winner else self.player_2
    
    
          
class Actions:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def shootTarget( attacker, enemy, a):
        row, col = a
        sh = enemy.ShipGrid.isShip(row,col)
        if sh:
            attacker.SearchGrid.markHit(row,col)
            enemy.ShipGrid.markHit(row,col)
            sh.shipHit()
            
            if enemy.isDefeated() : attacker.winner = True

        else:
            attacker.SearchGrid.markMiss(row,col)
        


class Node:
    def __init__(self,parent,attacker, enemy) -> None:
        self.parent = parent.deepcopy()
        self.attacker = attacker.deepcopy()
        self.enemy = enemy.deepcopy()
         
        self.children = list()


    def addChildren(self):
        child = Node(self, )


class MCTS:
    def __init__(self, attacker, opponent, maxDepth) -> None:
        self.root = Node(None,attacker, opponent)
        self.maxDepth = maxDepth
        
        
    def MCTSPlayer(self):
        iteration = 0
        while ( iteration < self.maxDepth):
            currNode = self.select()


    def select(self):
        
    def expand(self):
        
    def rollout(self):
        
    def backpropogate(self):
        





# h = Player("Turing", s._ship_size)
# h.ShipGrid.printBoard()

# print()
# c = Player("computer", s._ship_size)
# c.ShipGrid.printBoard()

# print(c.ships)
# c.ships[1].isSunk = True
# c.isDefeated()
    
# print(c.ships)

# print("Moves")
# a = Actions()
# a.shootTarget(h,c, (2,2) )
# a.shootTarget(h,c, (0,0) )
# a.shootTarget(h,c, (1,0) )

# h.SearchGrid.printBoard()

s.Fleet = [2,2,4]

player_1_wins = 0
sample = 1000 
for i in range(sample):
    g = Game()
    g.run()
    
    player_1_wins += 1 if g.isWinner() == g.player_1 else 0
    
player_2_wins = sample - player_1_wins

print("Player 1 Won: ", player_1_wins)
print("Player 2 Won: ", player_2_wins)
    
    
    
# g.runSimulationMode()
# print(g.isWinner().name)
# print(g.player_1.score())

# print()
# g.player_2.SearchGrid.printBoard()
