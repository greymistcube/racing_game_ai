---
layout: post
mathjax: true
---

# Racing Game with NEAT

![Game Screen](./img/racing_game_ai_peek.gif)

This is a continuation of my previous project
[Flappy Bird Clone with NEAT.](https://github.com/greymistcube/flappy_bird_ai)
If you want to know about how this particular AI works in general,
please visit the page for my previous project.

This project was started with two main goals in mind:
 
 * Use the NEAT algorithm made for the flappy bird clone game as a backend
 with as little change as possible.
 * Simulate an autonomous driving environment by limiting the kind of
 information that gets fed to the AI.

# Nonlinear and Complex Nature of the Game

Unlike flappy bird, where one can easily come up with a set of rules, expressed
as linear combinations of variables provided, when to jump, a driving game
is very nonlinear in its nature. As blocky as it may seem in the sample
screenshot above, turning mechanics inevitably result in some use of
trigonometric functions, and we know how nonlinear those are.

Although this adds some complexity when trying to come up with a set of
rules by hand, this is not to say the problem isn't solvable via some simple
linear combinations of input variables. For example, given a car at
some point $p$ with its velocity vector $v$ with angle of $\theta$ to
the $x$-axis. The results of turning left or right with some fixed amount are
nonlinear, nontrivial changes in $v$ and $p$ at the next time step.

If $v = (x, y)$, depending on their values, when turning left, $x$ and $y$
don't even change in the same direction in a consistent manner! For example,
if $v = (1, 0)$, turning left means decreasing $x$ and increasing $y$.
On the other hand if $v = (0, 1)$, turning left means decreasing *both* $x$
*and* $y$.

However, one can easily notice that the increasing/decreasing behaviors of
$x$ and $y$ are completely dependant on which quadrant $v$ lies on the plane.
So if we want to figure out whether to turn left or right to change the
values of $x$ and $y$ the way we want, we must first figure out what the
signs of $x$ and $y$ are and then act accordingly.

# Chossing the Variables
## Raw Input

# Installing Sensors
## Solving the Distance Problem

# Inside the AI's Mind
## Learning One Feature at a Time

## Learning a Single Feature Too Well

# Other Discussions


# Future Plans
## Q Learning
