import os


from engine import Game
from copy import deepcopy
from collections import deque
from random import sample as random_sample


from sus import make_wheel, select
from ga import Organism, population_after_mutation


from control_cep import next_generation


class NewOrganism(Organism):
    def get_fitness(self):
        if self.fitness is not None:
            return self.fitness
        else:
            self.win_o = 0
            self.draw_o = 0
            self.loss_o = 0

            empty_game = deepcopy(Game())
            anal_queue = deque()
            for empty_tile in (i for i in range(9) if not empty_game.tiles[i]):
                empty_game_clone = deepcopy(empty_game)
                empty_game_clone.set_tile(empty_tile)
                empty_game_clone.set_tile(self.move(empty_game_clone))
                anal_queue.append(empty_game_clone)

            while len(anal_queue):
                to_analyze = anal_queue.popleft()

                if to_analyze.winner:
                    if to_analyze.winner == 2:
                        self.win_o += 1
                    elif to_analyze.winner == 1:
                        self.loss_o += 1
                    else:
                        self.draw_o += 1
                else:
                    for empty_tile in (i for i in range(9) if not to_analyze.tiles[i]):
                        to_analyze_clone = deepcopy(to_analyze)
                        to_analyze_clone.set_tile(empty_tile)
                        if not to_analyze_clone.winner:
                            to_analyze_clone.set_tile(
                                self.move(to_analyze_clone))
                        anal_queue.append(to_analyze_clone)

            self.fitness = (self.loss_o) / (self.win_o +
                                            self.draw_o + self.loss_o)

            return self.fitness


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
    return NewOrganism("".join(offspring1_genome)), NewOrganism("".join(offspring2_genome))


def population_after_mating(mating_pool):
    rotated = deque(mating_pool)
    rotated.rotate(-1)
    ret_list = []
    for parent_pair in zip(mating_pool, rotated):
        ret_list.extend(crossover(*parent_pair))
    return ret_list


def simulate(population_size: int, num_generations: int, folder_name="test"):
    if os.path.exists(f"sim/o/{folder_name}"):
        raise Exception("Folder exists")
    else:
        os.makedirs(f"sim/o/{folder_name}")

    population = []
    for _ in range(population_size):
        population.append(NewOrganism())

    for generation_number in range(1, num_generations + 1):
        after_mating = population_after_mating(population)
        after_mutation = population_after_mutation(after_mating)
        population = next_generation(
            population, after_mating, after_mutation, population_size)
        with open(f"sim/o/{folder_name}/{generation_number}.csv", "w") as file:
            file.write("Genome, Fitness, Wins (O), Losses (O), Draws (O)\n")
            for organism in population:
                file.write(
                    f"{organism.genome}, {organism.get_fitness()}, {organism.win_o}, {organism.loss_o}, {organism.draw_o}\n")

    return population


if __name__ == "__main__":
    print(simulate(100, 500, "sim_1"))
