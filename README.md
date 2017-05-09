# Pong
### Final Project for Programming Paradigms

## Introduction
For the final project, we decided to implement Atari's Pong. We implemented our version of the game using the Pygame library. In order to allow two players, we also used the Twisted library. The game was implemented using the clock-tick paradigm. 

## Rules
The rules of the game can be found [here](http://en.wikipedia.org/wiki/Pong).
Each player controls a white block vertically across the screen. They must prevent to pong from going past their paddle/white block. If a player successfully gets the pong past their opponent, they receive a point. First player to five points wins the game. 

## How To Play
Each player controls their white block/paddle using the UP and DOWN arrows on their keyboard. 

Player 1: `./gamespace1.py`

Player 2: `./gamespace2.py` 

## Localhost vs Ash Server
Our game runs a lot nicer locally. There are a few lines that must be adjusted based on whether the players are running it locally or on the ash server. These adjust the speed of the ball. 
