![plot](/Assets/battleship_1.png)
# Computer plays Battleship

<b>Designed by: Jugen Gawande & Dimpy Ghaswala</b>

Battleship is a turn based strategy game. The goal is to arrange your own fleet and destroy enemy fleet before your own fleet is sunk entirely. 
This project develops a tree based ai algorithm that plays battleship against a human. The hope is to beat humans almost everytime. HAPPY FIGHTING.

In order to run this game you need to install <b>pygame, stable_baseline3.</b>
You will also need numpy and pandas if not already installed.
```
pip install stable-baselines3, pygame
```

To play the game launch the GUI using the following command after cloning this project.
```
python launch_game.py
```
To play the game follow the on screen instructions:

 - Enter the grid size to play with. Currently supported are (5,7,10,12,15).
 - Type <b>T</b> to play as a human for Player 1, similarly set Player 2 as <b>T</b> to set player 2 as human.
 - If either Player 1 or 2 is <b>F</b> then the player is AI. If both players are set to <b>F</b> then teh AI plays AI (World domination 🧨)
 - If you selected <b>F</b> you will have to choose 1 of 3 algorithms to play with for each player.


 - <b>COMPETE MODE: </b>When one player of the player is the computer ai then an option to play in compete mode is presented. If set to <b>T</b> then you can't see the opponents board. Then the game play is like a true game. 

Use the following keys while in game to control the game:
<b>ESC</b> : Exit the game
<b>SPACE</b> : Reset the game (Randomizes a new map)

The gamelplay looks like below

![plot](/Assets/gameplay_1.png)

The analysis of the algorithm can be found in the the gameplay_analysis.ipynb




<center> made with 🧠</center>
