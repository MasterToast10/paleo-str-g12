from ga import Organism
from bisect import insort


def next_generation(population_before_selection, population_after_mating, population_after_mutation, population_size = 100):
    combined_list = []
    for organism in population_before_selection:
        insort(combined_list, (organism.get_fitness(), organism))
    for organism in population_after_mating:
        insort(combined_list, (organism.get_fitness(), organism))
    for organism in population_after_mutation:
        insort(combined_list, (organism.get_fitness(), organism))

    ret_list = []
    for i in range(1, population_size + 1):
        j = int(i + (2*population_size) * (((i - 1)*(i - 2))/((population_size - 1)*(population_size - 2))))
        ret_list.append(combined_list[j - 1][1])
    return ret_list


if __name__ == "__main__":
    print(next_generation([Organism(), Organism(), Organism()], [Organism(), Organism(), Organism()], [Organism(), Organism(), Organism()], 3))
