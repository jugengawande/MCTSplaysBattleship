from rl_model import BattleShip
import argparse
import time
import os
from stable_baselines3 import PPO
from test import Game

parser = argparse.ArgumentParser()
parser.add_argument('-g','--grid')

args = parser.parse_args()

test_set ={
    5: [5,[2,3,4]],
    7: [7,[2,3,4]],
    10: [10,[2,3,4]],
    12: [12,[2,3,4]],
    15: [15,[2,3,4]],
}

size = int(args.grid)
env = BattleShip(size)

# env.state = Game(test_set[size][0],test_set[size][1] )

modeldir = f"models/{size}/{int (time.time ( ))}"
logdir = f"logs/{size}/{int (time. time () )}"

if not os.path.exists (modeldir):
    os.makedirs (modeldir)
if not os.path.exists (logdir):
    os.makedirs (logdir)

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 100000

for i in range (1, 1000) : 
    model.learn (total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO") 
    model.save (f'{modeldir}/{TIMESTEPS*i}')
    
env. close ()