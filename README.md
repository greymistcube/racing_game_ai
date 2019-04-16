# Racing Game with NEAT

![Game Screen](./docs/img/racing_game_ai_peek.gif)

This is a continuation of my previous project
[Flappy Bird Clone with NEAT.](https://github.com/greymistcube/flappy_bird_ai)

## Dependencies

This project only requires `numpy` and `pygame` packages to run.
To install the required packages, run the following commands.
```
pip install numpy
pip install pygame
```
Versions `1.16.2` and `1.9.4` were used respectively during its devlopment.

## Usage

Run with
```
python game.py
```
to start the game normally in a human playable mode with the default settings.
Various other options may be given at startup. For example,
```
python game.py -z 3 -n 200 neat
```
will start the game with 3x zoom, and 200 cars per generation for NEAT AI.
More help can be found with by using the `-h` option.

## Controls
Use <kbd>&uarr;</kbd>, <kbd>&darr;</kbd>, <kbd>&larr;</kbd>, and <kbd>&rarr;</kbd>
keys to control the car. Number keys may be used to change the game speed.
This is mainly used to speed up the training process for the AI.
