from game_variables import Settings as set

import numpy as np
import random 
from copy import deepcopy
import pandas as pd

from stable_baselines3 import PPO



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
            
        self.SearchGrid = SearchBoard(set.GRID_SIZE)
        self.ShipGrid = ShipBoard(set.GRID_SIZE)
        
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
        spare = set.WORLD_SIZE() - sum(self.fleet) 
 
        return 1 - (miss/spare)


class Strategy:
    @staticmethod
    def randomPlayer( moves ):
        return random.choice(moves)

    @staticmethod
    def sequentialPlayer(moves):
        return moves[0]
    
    @staticmethod
    def MCTSPlayer(player_1,player_2, max_depth):
        return MCTS(player_1, player_2, max_depth).MCTSPlayer()
    
    @staticmethod
    def QLearnPlayer(model, board):
        return np.unravel_index(model.predict(board)[0], (set.GRID_SIZE, set.GRID_SIZE))


class Game:
    def __init__(self, grid_size, fleet=None, model=None) -> None:
        set.GRID_SIZE = grid_size
        self.fleet = fleet if fleet else set.ship_sizes[set.GRID_SIZE]
        

        self.player_1 = Player("Human", self.fleet)
        self.player_2 = Player("Computer", self.fleet)

        self.turn = True
        
        # self.model = PPO.load ("models/5/1671268825/1600000.zip")
        if model : self.model = PPO.load (model)
    
        

    def makeMove(self, tr=None, st=None):
        
        strategy_1 = {
            'base': lambda : Strategy.sequentialPlayer(self.player_1.possibleMoves()),
            'tree': lambda: Strategy.MCTSPlayer(self.player_1, self.player_2, 50),
            'rl': lambda: Strategy.QLearnPlayer(self.model, self.player_1.SearchGrid.getBoard())
        }
        
        strategy_2 = {
            'base': lambda : Strategy.sequentialPlayer(self.player_2.possibleMoves()),
            'tree': lambda: Strategy.MCTSPlayer(self.player_2, self.player_1, 50),
            'rl': lambda: Strategy.QLearnPlayer(self.model, self.player_2.SearchGrid.getBoard())
        }
        
        
        if not self.player_1.isDefeated() and not self.player_2.isDefeated():
            
            if self.turn:

                target = strategy_1[st]( ) if not tr else tr

                
                if target in self.player_1.possibleMoves():
                    res = Actions.shootTarget(self.player_1, self.player_2, target)                                
                    self.turn = not self.turn
                
            else:   
                target = strategy_2[st]( ) if not tr else tr
                
                if target in self.player_2.possibleMoves():
                    res = Actions.shootTarget(self.player_2, self.player_1, target)
                    self.turn = not self.turn
    
    
    def run(self):
        
        while not self.player_1.isDefeated() and not self.player_2.isDefeated():
            
            if self.turn:
                # target = Strategy.sequentialPlayer(self.player_1.possibleMoves())
                target = Strategy.MCTSPlayer(self.player_1, self.player_2, 20)
                # target = Strategy.QLearnPlayer(self.model, self.player_2.SearchGrid.getBoard())
                
                res = Actions.shootTarget(self.player_1, self.player_2, target)                
                # print("Player 1 targeted: ", target, "H" if res else "M")
                
                if res != None: self.turn = not self.turn
            else:   
                # # target = Strategy.sequentialPlayer(self.player_2.possibleMoves())
                # target = Strategy.MCTSPlayer(self.player_2, self.player_1, 100)
                target = Strategy.QLearnPlayer(self.model, self.player_2.SearchGrid.getBoard())
                
                res = Actions.shootTarget(self.player_2, self.player_1, target)

                
                if res != None: self.turn = not self.turn


    def runSimulationMode(self, strat):
        
        # Plays one full game in one player mode
        
        strategy = {
            'baseline-sequential': lambda : Strategy.sequentialPlayer(self.player_1.possibleMoves()),
            'tree': lambda: Strategy.MCTSPlayer(self.player_1, self.player_2, 20),
            'qlearning': lambda: Strategy.QLearnPlayer(self.model, self.player_1.SearchGrid.getBoard())
        }
        
        steps = 0
        
        while not self.player_1.winner:
            # target = Strategy.sequentialPlayer(self.player_1.possibleMoves())
            # target = Strategy.MCTSPlayer(self.player_1, self.player_2, 50)
            # target = Strategy.QLearnPlayer(self.model, self.player_1.SearchGrid.getBoard())
            
            target = strategy[strat]( )
            # print(target)
            if target in self.player_1.possibleMoves():
                res = Actions.shootTarget(self.player_1, self.player_2, target)
                # print("Player 1 targeted: ", target, "H" if res else "M")

                steps += 1
        
        return steps, self.isWinner().score(), self.isWinner().SearchGrid.getBoard()
      
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
            return True

        else:
            attacker.SearchGrid.markMiss(row,col)
            return False
        
        return None
        


class Node:
    def __init__(self,parent,attacker, enemy) -> None:
        self.parent = parent
        self.attacker = deepcopy(attacker)
        self.enemy = deepcopy(enemy)
        
        self.children = list()
        
        self.plays = 0
        self.wins = 0
        
    def pickChildToSimulate(self):
        return random.choice(self.children)
            
    def addChild(self, node):
        self.children.append(node)
    
    def makeMove(self, move):
        self.target = move
        Actions.shootTarget(self.attacker, self.enemy, self.target)
        
    def getChildren(self):
        return self.children
    
    def incrementPlay(self):
        self.plays += 1

    def incrementWins(self):
        self.wins += 1
        
    def winPercentage(self):
        if self.plays > 0:
            return float(self.wins / self.plays)
        else:
            return 0

class MCTS:
    
    def __init__(self, attacker, opponent, maxDepth) :
        self.root = Node(None,attacker, opponent)
        self.maxDepth = maxDepth
           

    def UCT(self, parent_plays, curr_wins, curr_plays):
        if curr_plays == 0:
            return float("inf")

        return (curr_wins / curr_plays) + (np.sqrt(2 * np.log(np.exp(parent_plays)) / curr_plays))
    
    
    def select(self, node):
        
        if not node.getChildren(): # No children of root
            return node
        
        bestNode = node
        bestUCT = 0
        
        for n in node.getChildren():
            uct = self.UCT(n.parent.plays, n.wins, n.plays)
        
            if uct == float("inf"): return n
            
            if bestNode == node or uct > bestUCT:
                bestNode = n
                bestUCT = uct
                
        return self.select(bestNode)
        
    def expand(self, parentNode):
        
        moves = parentNode.attacker.possibleMoves()
        
        # print("Expanding node")
        for m in moves:
            # print("Child: move ", m)
            child = Node(parentNode, parentNode.enemy, parentNode.attacker)
            child.makeMove(m)
            parentNode.addChild(child)
                

    def rollout(self, node = None, att = None, en = None):
        
        
        if node != None:
            attacker = deepcopy(node.attacker)
            enemy = deepcopy(node.enemy)
        else:
            attacker = att
            enemy = en
            
            
        possibleMove = attacker.possibleMoves()
        move = random.choice(possibleMove)
        
        Actions.shootTarget(attacker, enemy, move )
        
        if enemy.isDefeated():
            # print("End Simulation")
            return True
        
        return not self.rollout(att = enemy,  en = attacker)
        

    def backpropogate(self, node, wins):
        if wins:
            node.incrementWins()
        node.incrementPlay()
        
        
        if node.parent != None:
            self.backpropogate(node.parent, not wins)
        

     
   
    def run(self):
        iteration = 0

        # print("\nMCTS Start")  
        
        while ( iteration < self.maxDepth):
            # print(iteration) 
            
            currNode = self.select(self.root)
            self.expand(currNode) 
            simulateNode = currNode.pickChildToSimulate()
            # print("Selected child: ", simulateNode.target)
            
            if simulateNode == None or not simulateNode.attacker.possibleMoves():
                break
            
            # print("Started Simulation")    
            win = self.rollout(node = simulateNode)
            self.backpropogate(simulateNode, win)
            iteration += 1
        
            
        return self.root.getChildren() 
            
    def MCTSPlayer(self):
        m = self.run()
        # print(m)
        promisingNode = random.choice(m)
        
        for node in m:
            # print(round(node.winPercentage(),2), end="\t")

            if node.winPercentage() > promisingNode.winPercentage():
                promisingNode = node
                
        # print(promisingNode.target )
        return promisingNode.target



# h = Player("Turing", set._ship_size)
# h.ShipGrid.printBoard()

# print()
# c = Player("computer", set._ship_size)
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

# set.Fleet = [2,3,4]
# set.GRID_SIZE = 5 



# #-------------------------

# player_1_wins = 0
# sample = 10
# for i in range(sample):
    
#     print("Playing game:", i+1, end="\r")
#     g = Game(5, [2,3,4], model="models/5/1671268825/1500000.zip")
#     g.run()
    
#     player_1_wins += 1 if g.isWinner() == g.player_1 else 0
    
#     # print("Won by", g.isWinner().name, " Score:", round(g.isWinner().score(),5))
#     # g.isWinner().SearchGrid.printBoard()
    

# player_2_wins = sample - player_1_wins

# print("Player 1 Wins: ", player_1_wins)
# print("Player 2 Wins: ", player_2_wins)
    

# #-------------------------



# test_set ={
#     5: [5,[2,3,4]],
#     7: [7,[2,3,4]],
#     10: [10,[2,3,4]],
#     15: [15,[2,3,4]],
# }

# exp_result = pd.DataFrame(columns=['input_value','iterations', 'score', 'board'])
# exp_result = exp_result.astype("object")


# sample = 100

# input_config = 5

# for i in range(sample):

#     gm = Game(test_set[input_config][0],test_set[input_config][1], model="models/5/1671268825/1500000.zip")
    
#     # g.player_2.ShipGrid.printBoard()

#     iter, sc, brd = gm.runSimulationMode(strat='tree')
    
#     sim_res = [ input_config ,iter,sc, brd]
    
#     exp_result = pd.concat([exp_result, pd.DataFrame([sim_res], columns = exp_result.columns)], ignore_index=False)
    
#     print(f"Experiment: {i} Score :  {sc} Moves: {iter}")
#     # g.player_1.SearchGrid.printBoard()
    
# print("Best score: ", exp_result['score'].max())
# print("Average Score: ",exp_result['score'].mean())
# print("Average Moves: ",exp_result['iterations'].mean())
