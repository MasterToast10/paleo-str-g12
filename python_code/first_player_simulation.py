import os


from sus import make_wheel, select
from ga import Organism, population_after_mating, population_after_mutation


from rmg_cep import next_generation


def simulate(population_size: int, num_generations: int, folder_name="test"):
    if os.path.exists(f"sim/x_rmg/{folder_name}"):
        raise Exception("Folder exists")
    else:
        os.makedirs(f"sim/x_rmg/{folder_name}")

    population = []
    for _ in range(population_size):
        population.append(Organism())

    for generation_number in range(1, num_generations + 1):
        found_no_loss = False
        to_mate = select(make_wheel(population), population_size // 2)
        after_mating = population_after_mating(to_mate)
        after_mutation = population_after_mutation(after_mating)
        population = next_generation(
            population, after_mating, after_mutation, population_size)
        with open(f"sim/x_rmg/{folder_name}/{generation_number}.csv", "w") as file:
            file.write("Genome, Fitness, Wins (X), Losses (X), Draws (X)\n")
            for organism in population:
                if organism.get_fitness() == 0:
                    found_no_loss = True
                file.write(
                    f"{organism.genome}, {organism.get_fitness()}, {organism.win_x}, {organism.loss_x}, {organism.draw_x}\n")
        print(population[0].get_fitness())
        if found_no_loss:
            return population

    return population


if __name__ == "__main__":
    for i in range(1, 16):
        simulate(100, 500, f"sim_{i}")
