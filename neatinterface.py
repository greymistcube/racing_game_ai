import neat
import lib

from lib.settings import Settings
from lib.constants import WIDTH, HEIGHT

settings = Settings()

# game specific neat interface
# this straps on to the original Core class
# by inheriting it and overriding necessary methods
# and adding extensions
class NeatCore(lib.Core):
    # game specific variables
    __num_input = 6
    __num_output = 1

    # overriden methods
    def __init__(self):
        super().__init__()
        self.population = neat.Population(
            self.__num_input,
            self.__num_output,
            pop_size=settings.num_balls
        )
        return

    def new_balls(self):
        return [SmartBall(genome) for genome in self.population.genomes]

    def update(self):
        self.events.update()
        settings.update(self.events)
        # only cycle through balls alive in the environment for optimization
        for ball in self.env.balls:
            ball.think(self.get_x(ball, self.env.walls))
        self.env.update(self.events)

    def game_over(self):
        if self.env.game_over():
            scores = [ball.score for ball in self.balls]
            self.population.score_genomes(scores)
            self.population.evolve_population()
            return True
        else:
            return False

    def get_info_surface(self):
        num_survived = sum([
            ball.color == "blue" and ball.alive
            for ball in self.env.balls
        ])
        num_mutated = sum([
            ball.color == "green" and ball.alive
            for ball in self.env.balls
        ])
        num_bred = sum([
            ball.color == "yellow" and ball.alive
            for ball in self.env.balls
        ])

        texts = [
            " Game: {}".format(self.game_count),
            " Score: {}".format(self.env.score),
            " Alive: {}".format(self.env.num_alive),
            " (Blue) Survived: {}".format(num_survived),
            " (Green) Mutated: {}".format(num_mutated),
            " (Yellow) Bred: {}".format(num_bred)
        ]

        return self.text_renderer.texts_to_surface(texts)

    # extended methods
    def get_x(self, ball, walls):
        if ball.alive:
            return [
                ball.velocity / 100,
                ball.y / HEIGHT,
                walls[0].x / WIDTH,
                walls[0].y / HEIGHT,
                walls[1].x / WIDTH,
                walls[1].y / HEIGHT
            ]
        else:
            return [0] * self.__num_input

class SmartBall(lib.objects.Ball):
    __genome_to_color = {
        "survived": "blue",
        "mutated": "green",
        "bred": "yellow",
        "diverged": "red"
    }

    def __init__(self, genome):
        super().__init__()

        # override randomized color
        self.genome = genome
        self.color = self.get_color(genome)

    def get_color(self, genome):
        return self.__genome_to_color[genome.genome_type]
    
    def think(self, x):
        if self.genome.predict(x)[0]:
            self.jump()
        return
