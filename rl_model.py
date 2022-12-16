
import numpy as np
import gym
import os
import time

from gym.spaces import Discrete, Box
from stable_baselines3 import PPO

from game_variables import Settings as s
from test import Game, Actions
import random

class BattleShip(gym.Env):
    def __init__(self) -> None:
        super().__init__()
        
        self.state =  Game(5, [2,3,4])
        self.att = self.state.player_1
        self.en = self.state.player_2
        
        self.action_space = Discrete(s.GRID_SIZE*s.GRID_SIZE)
        self.observation_space = Box(low=0, high= 1, shape=(s.GRID_SIZE, s.GRID_SIZE), dtype=np.int)
        
        self.win = False
        self.prev_reward = 0
  
        
    def step(self, action):
        
        target = np.unravel_index(action, (s.GRID_SIZE,s.GRID_SIZE))
        # print(target)
        
        # target = action 
        reward = 0
        win = 0 
        
        if target in self.att.possibleMoves():
            
            res = Actions.shootTarget(self.att, self.en, target)
            
            if res:
                if self.prev_reward == 1:
                    reward += 5 # If ship is hit
                    
                else:
                    reward += 1
                    
                self.prev_reward = 1
                
                win = self.en.isDefeated() 
                # if win: reward = 100
            
                
            else:
                if self.prev_reward == 0 : # Repeat miss 
                    
                    reward -=1 # If missed
                
                self.prev_reward = 0
         
        else:
            if self.att.SearchGrid.getBoard()[target[0]][target[1]] == 1: 
                reward -= 5
            else:
                reward -= 10  # Penalize choosing an illegal move
            
        prev_action = target
        
        info = {}
            
        return self.att.SearchGrid.getBoard(), reward, win, info 
        
    def reset(self):
        
        self.win = False
        self.prev_reward = 0
        
        self.state =  Game(5, [2,3,4])
        self.att = self.state.player_1
        self.en = self.state.player_2
        
        return 0

        
        
# env = BattleShip()
# res = []
# for ep in range(10):
#     obv = env.reset()
    
#     win = False
#     steps = 0
    
#     while not win:
#         action = env.action_space.sample()
#         # action = random.choice(env.att.possibleMoves())

#         obv, reward, win, _ = env.step(action)
        
#         # if reward > 0: print(f'ac {action} rw {reward}')
        
#         steps += 1
        
#         if win: 
#             print(f"Episode: {ep} Steps took: {steps}", end='\r')
#             # obv.player_1.SearchGrid.printBoard()
#             res.append(steps)
            
            
# env.close()

# res = np.array(res)
# print()
# print(f"Average Steps: {np.mean(res)}" )




# env = BattleShip()

# modeldir = f"models/{int (time.time ( ))}"
# logdir = f"logs/{int (time. time () )}"

# if not os.path.exists (modeldir):
#     os.makedirs (modeldir)
# if not os.path.exists (logdir):
#     os.makedirs (logdir)

# model = PPO("MlpPolicy", env, verbose=1)

# TIMESTEPS = 1000

# for i in range (1, 100) : 
#     model.learn (total_timesteps=TIMESTEPS, reset_num_timesteps=False) #, tb_log_name= "PPO")
#     model.save (f'{modeldir}/{TIMESTEPS*i}')
    
# env. close ()


# del model

model = PPO.load ("models/1671227467/810000")

for i in range(10):
    action, _ = model.predict([[-1,-1,-1,1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,-1,-1,-1]])
    print(np.unravel_index(action, (s.GRID_SIZE,s.GRID_SIZE)))
