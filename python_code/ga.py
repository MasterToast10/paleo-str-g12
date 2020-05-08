from random import choice as random_choice
from engine import MoveGenerator, Game
from game_base import find_base_case


class Organism(MoveGenerator):
    def __init__(self, player_number: int, genome: str=None):
        self.PLAYER_NUMBER = player_number
        self.fitness = None
        
        if genome is None:
            temp = bytearray()
            with open("python_code/game-base.txt") as file:
                for line in file:
                    game = Game([int(x) for x in line.split()])
                    if not game.winner:
                        temp.append(random_choice(tuple(i for i in range(9) if not game.tiles[i])))
                    else:
                        temp.append(9)
            self.genome = "".join(str(x) for x in temp)
        else:
            if len(genome) != 765:
                raise Exception("Invalid genome")
            self.genome = genome

    def move(self, game: Game):
        base_case_repr = f"{repr(find_base_case(game))}\n"

        with open("python_code/game-base.txt") as file:
            for index, line in enumerate(file):
                if line == base_case_repr:
                    return int(self.genome[index])

    def mutate(self):
        self.fitness = None

    def get_fitness(self):
        if self.fitness is not None:
            return self.fitness
        else:
            # TODO: fitness function
            return self.fitness