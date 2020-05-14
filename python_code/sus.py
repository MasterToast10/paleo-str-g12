# Modified version of code by Ashwin Panchapakesan on March 30, 2014 (https://stackoverflow.com/a/22750088)


import random


from ga import Organism
from collections import Counter


def get_m(population):
    same_counter = Counter(p.get_fitness() for p in population)
    num_similar_fitness = 0
    for _, count in same_counter.items():
        if count > 1:
            num_similar_fitness += count
    return num_similar_fitness


def fitness(organism: Organism, m: int):
    if m == 0:
        return 1 - organism.get_fitness()
    else:
        return (1/m)*(1 - organism.get_fitness())


def make_wheel(population):
    wheel = []
    num_similar_fitness = get_m(population)
    total = sum(fitness(p, num_similar_fitness) for p in population)
    top = 0
    for p in population:
        f = fitness(p, num_similar_fitness)/total
        wheel.append((top, top+f, p))
        top += f
    return wheel


def bin_search(wheel, num):
    mid = len(wheel)//2
    low, high, answer = wheel[mid]
    if low <= num <= high:
        return answer
    elif high < num:
        return bin_search(wheel[mid+1:], num)
    else:
        return bin_search(wheel[:mid], num)


def select(wheel, N):
    stepSize = 1.0/N
    answer = []
    r = random.random()
    answer.append(bin_search(wheel, r))
    while len(answer) < N:
        r += stepSize
        if r > 1:
            r %= 1
        answer.append(bin_search(wheel, r))
    return answer


if __name__ == "__main__":
    pop = []
    for i in range(10):
        pop.append(Organism())

    print(select(make_wheel(pop), 2))
