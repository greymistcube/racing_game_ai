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

In my previous post, although I have mentioned that one must be wary of
solving the problem for the AI, I'd say this is a good test case scenario
with relations between input variables and output variables complex enough
where we don't need to worry too much about such problem.

## Raw Values for Input Variables

If one were to be very naive about this, one can just feed in a bunch of
"raw" values to the AI, such as $x$ and $y$ coordinates of the car, its
velocity vector $v$ as a tuple, nearby walls considered as line segments
represented by pairs of points, etc. I have tested this case and this does
work with a single hidden layer network with enough hidden nodes.
I had to force each genome to start with at least 8 hidden nodes,
as it would take unfeasibly long amount of time without any rule modifications
to the current AI, but there seems to be little to no reason why it shouldn't
work when I let the genomes grow organically. More on this later.

## Relative Values for Input Variables

As mentioned above, one of my primary goals was to simulate an autonomous
driving environment. What I meant by this is that I wanted to "limit" the amount
and the kind of information a car can have to what it can "see". I know
the analogy is pretty weak since any real world autonomous driving wouldn't
work like this. Any self driving car would have access to its own *logitude*
and *latitude* via GPS and detailed map data to aid in its thinking.
In any case, I wanted to simulate an agent akin to a human driver
(perhaps with a severe case of amnesia since it doesn't have any map knowledge).
I hope anyone can still see the motivation behind this reasoning.

As this is more of a case study, I had a particular set of variables
to use in mind very early on in the stage. They are as follows:

 * speed of the vehicle
 * direction to go relative to the direction that the car is headed
 * distance measurements to any obstructing object in four directions:
 front, back, left, and right

The first is the most obvious. As for the second, I decided to use an angle
measurement ranging $[-180, 180)$. This isn't too hard since the directional
vector of a car is derived from its angle and speed. The last is the only
one that some explanation might be needed on how the needed values are
acquired.

## Solving the Distance Problem

Let's say we have a car at point $p = (p_{x}, p_{y})$ with its directional
vector $v = (v_{x}, v_{y})$ and some line segements as walls as depicted below.

![Distance Example 01](./img/distance_example_01.png)

We'd like to compute not only the distances to all walls from point $p$ in
the direction of $v$, but also all distances to all walls in all four
directions, which are multiples of $90$ degree rotations of $v$.
Knowing the angle for $v$ and all the relavent coordinates, it is
possible to compute these values directly. Although simple as it may seem,
deriving the formulae and computing the solutions this way is rather tedious
and not so straightforward. However, there is a simpler way.
To do this, we first translate the plane by subtracting $p$ from all points
to get the following.

![Distance Example 02](./img/distance_example_02.png)

The problem looks simpler now, but we can do more. Knowing the angle of $v$
from the $x$-axis, we rotate the entire plane to align $v$ with the $x$-axis.
Then we get the following.

![Distance Example 03](./img/distance_example_03.png)

Now seeing whether the line segments cross one of the four cardinal directions
in relation to the original vector $v$ became a simple matter of comparing
the signs of of $x$ or $y$ coordinates. Evenmore, distances are now just
$x$-intercept and $y$-intercept values.

# Inside the AI's Mind

As flappy bird was rather a simple game, it wasn't very insightful in how
the AI was learning to beat the game. However, in this case, after running
several trails, there were some particulars about the behaviors of the AI
that were quite noticable.

## Learning One Feature at a Time

## Learning a Single Feature Too Well

# Other Discussions


# Future Plans
## Q Learning
