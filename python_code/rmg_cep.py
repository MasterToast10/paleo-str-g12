from engine import MoveGenerator, GameController
from ga import Organism
from bisect import insort
from rmg import RandomMoveGenerator


def mg_result(organism: Organism, mg: MoveGenerator):
    loss_counter = 0
    for _ in range(300):
        the_winner = GameController(organism, mg, verbose=False).start()
        if the_winner == 2:
            loss_counter += 1
    print(loss_counter, end=" ")
    return loss_counter



def next_generation(population_before_selection, population_after_mating, population_after_mutation, population_size = 100):
    RMG = RandomMoveGenerator(2)
    combined_list = []
    for organism in population_before_selection:
        insort(combined_list, (mg_result(organism, RMG), organism))
    for organism in population_after_mating:
        insort(combined_list, (mg_result(organism, RMG), organism))
    for organism in population_after_mutation:
        insort(combined_list, (mg_result(organism, RMG), organism))

    ret_list = []
    for i in range(1, population_size + 1):
        j = int(i + (2*population_size) * (((i - 1)*(i - 2))/((population_size - 1)*(population_size - 2))))
        ret_list.append(combined_list[j - 1][1])
    return sorted(ret_list)


if __name__ == "__main__":
    print(next_generation([Organism(), Organism(), Organism()], [Organism(), Organism(), Organism()], [Organism(), Organism(), Organism()], 3))
