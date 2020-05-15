import os


from sus import make_wheel, select
from ga import Organism, population_after_mating, population_after_mutation


from control_cep import next_generation


def simulate(population_size: int, num_generations: int, folder_name="test"):
    if os.path.exists(f"sim/x/{folder_name}"):
        raise Exception("Folder exists")
    else:
        os.makedirs(f"sim/x/{folder_name}")

    population = []
    for _ in range(population_size):
        population.append(Organism())

    for generation_number in range(1, num_generations + 1):
        after_mating = population_after_mating(population)
        after_mutation = population_after_mutation(after_mating)
        population = next_generation(
            population, after_mating, after_mutation, population_size)
        with open(f"sim/x/{folder_name}/{generation_number}.csv", "w") as file:
            file.write("Genome, Fitness, Wins (X), Losses (X), Draws (X)\n")
            for organism in population:
                file.write(
                    f"{organism.genome}, {organism.get_fitness()}, {organism.win_x}, {organism.loss_x}, {organism.draw_x}\n")

    return population


if __name__ == "__main__":
    print(simulate(100, 500, "sim_1"))
