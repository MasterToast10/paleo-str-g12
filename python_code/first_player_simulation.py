from sus import make_wheel, select
from ga import Organism, population_after_mating, population_after_mutation


from control_cep import next_generation

def simulate(population_size: int, num_generations: int):
    population = []
    for _ in range(population_size):
        population.append(Organism())
    
    for _ in range(num_generations):
        after_mating = population_after_mating(population)
        after_mutation = population_after_mutation(after_mating)
        population = next_generation(population, after_mating, after_mutation, population_size)

    return population

if __name__ == "__main__":
    print(simulate(3, 50))
