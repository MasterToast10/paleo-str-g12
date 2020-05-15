from random import choice as random_choice, sample as random_sample
from linecache import getline as file_getline
from engine import MoveGenerator, Game, GameController
from game_base import GAME_ROTATIONS, find_base_case
from rmg import RandomMoveGenerator
from collections import deque
from copy import deepcopy
from functools import total_ordering


@total_ordering
class Organism(MoveGenerator):
    def __init__(self, genome: str = None):
        self.fitness = None

        if genome is None:
            temp = bytearray()
            with open("python_code/game-base.txt") as file:
                for line in file:
                    game = Game([int(x) for x in line.split()])
                    if not game.winner:
                        temp.append(random_choice(
                            tuple(i for i in range(9) if not game.tiles[i])))
                    else:
                        temp.append(9)
            self.genome = "".join(str(x) for x in temp)
        else:
            if len(genome) != 765:
                raise Exception("Invalid genome")
            self.genome = genome

    def move(self, game: Game):
        base_case = find_base_case(game)
        base_case_repr = f"{repr(base_case)}\n"
        game_repr = f"{repr(game)}\n"

        # print(base_case, base_case_repr, game_repr, sep="\n")

        with open("python_code/game-base.txt") as file:
            for index, line in enumerate(file):
                if line == base_case_repr:
                    base_case_move = int(self.genome[index])
                    # print(base_case_move)

                    if base_case_repr == game_repr:
                        return base_case_move

                    for rotation in GAME_ROTATIONS:
                        temp_list = []
                        for index in rotation:
                            temp_list.append(base_case.tiles[index])

                        if f"{repr(Game(temp_list))}\n" == game_repr:
                            # print(Game(temp_list))
                            for index, base_case_index in enumerate(rotation):
                                if base_case_index == base_case_move:
                                    return index

    def mutate(self, num_to_mutate: int):
        positions = random_sample(range(1, 766), num_to_mutate)
        for position in positions:
            game = Game([int(x) for x in file_getline(
                "python_code/game-base.txt", position).split()])
            if not game.winner:
                self.genome = f"{self.genome[:position-1]}{random_choice(tuple(i for i in range(9) if not game.tiles[i]))}{self.genome[position:]}"
            else:
                self.mutate(1)
        self.fitness = None
        self.get_fitness()

    def get_fitness(self):
        if self.fitness is not None:
            return self.fitness
        else:
            # TODO: Evaluate as first player
            self.win_x = 0
            self.draw_x = 0
            self.loss_x = 0

            empty_game = deepcopy(Game())
            empty_game.set_tile(self.move(empty_game))
            anal_queue = deque([empty_game])

            while len(anal_queue):
                to_analyze = anal_queue.popleft()

                if to_analyze.winner:
                    if to_analyze.winner == 1:
                        self.win_x += 1
                    elif to_analyze.winner == 2:
                        self.loss_x += 1
                    else:
                        self.draw_x += 1
                else:
                    for empty_tile in (i for i in range(9) if not to_analyze.tiles[i]):
                        to_analyze_clone = deepcopy(to_analyze)
                        to_analyze_clone.set_tile(empty_tile)
                        if not to_analyze_clone.winner:
                            to_analyze_clone.set_tile(
                                self.move(to_analyze_clone))
                        anal_queue.append(to_analyze_clone)

            # TODO: Evaluate as second player
            # self.win_o = 0
            # self.draw_o = 0
            # self.loss_o = 0

            # empty_game = deepcopy(Game())
            # anal_queue = deque()
            # for empty_tile in (i for i in range(9) if not empty_game.tiles[i]):
            #     empty_game_clone = deepcopy(empty_game)
            #     empty_game_clone.set_tile(empty_tile)
            #     empty_game_clone.set_tile(self.move(empty_game_clone))
            #     anal_queue.append(empty_game_clone)

            # while len(anal_queue):
            #     to_analyze = anal_queue.popleft()

            #     if to_analyze.winner:
            #         if to_analyze.winner == 1:
            #             self.win_o += 1
            #         elif to_analyze.winner == 2:
            #             self.loss_o += 1
            #         else:
            #             self.draw_o += 1
            #     else:
            #         for empty_tile in (i for i in range(9) if not to_analyze.tiles[i]):
            #             to_analyze_clone = deepcopy(to_analyze)
            #             to_analyze_clone.set_tile(empty_tile)
            #             if not to_analyze_clone.winner:
            #                 to_analyze_clone.set_tile(
            #                     self.move(to_analyze_clone))
            #             anal_queue.append(to_analyze_clone)

            self.fitness = (self.loss_x) / (self.win_x +
                                            self.draw_x + self.loss_x)

            return self.fitness

    def __eq__(self, other):
        return self.get_fitness() == other.get_fitness()

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()

    def __repr__(self):
        return f"Organism <{self.genome}>"


def crossover(parent1: Organism, parent2: Organism):
    cross_sites = sorted(random_sample(range(1, 766), 50))
    pre_cross_sites = deque(cross_sites)
    pre_cross_sites.appendleft(None)
    post_cross_sites = deque(cross_sites)
    post_cross_sites.append(None)
    parent1_genome = parent1.genome
    parent2_genome = parent2.genome
    offspring1_genome = []
    offspring2_genome = []
    alternator = True
    for pre, post in zip(pre_cross_sites, post_cross_sites):
        if alternator:
            offspring1_genome.extend(parent1_genome[pre:post])
            offspring2_genome.extend(parent2_genome[pre:post])
            alternator = False
        else:
            offspring1_genome.extend(parent2_genome[pre:post])
            offspring2_genome.extend(parent1_genome[pre:post])
            alternator = True
    return Organism("".join(offspring1_genome)), Organism("".join(offspring2_genome))


def population_after_mating(mating_pool):
    rotated = deque(mating_pool)
    rotated.rotate(-1)
    ret_list = []
    for parent_pair in zip(mating_pool, rotated):
        ret_list.extend(crossover(*parent_pair))
    return ret_list


def population_after_mutation(population_to_mutate):
    probability_of_mutation = min(o.get_fitness()
                                  for o in population_to_mutate)
    num_to_mutate = int(250*probability_of_mutation + 10)
    print(num_to_mutate)
    for organism in population_to_mutate:
        organism.mutate(num_to_mutate)
    return population_to_mutate


if __name__ == "__main__":
    # for i in range(10000):
    #     organ = Organism()
    #     print(organ)
    #     organ.mutate(5)
    #     print(organ)
    #     boi = GameController(RandomMoveGenerator(1), organ, verbose=True)
    #     boi.start()
    # organ = Organism()
    # for i in range(50):
    #     print(organ.get_fitness())
    parents = [Organism(), Organism()]
    for org in parents:
        print(org.genome)
        print(org.get_fitness())
    # print()
    # for org in population_after_mating(parents):
    #     print(org.genome)
    for mutated in population_after_mutation(parents):
        print(mutated.genome)
        print(mutated.get_fitness())
