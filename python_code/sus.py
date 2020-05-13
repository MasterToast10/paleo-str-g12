# Modified version of code by Ashwin Panchapakesan on March 30, 2014 (https://stackoverflow.com/a/22750088)


import random


from ga import Organism


def make_wheel(population):
    wheel = []
    total = sum(p.get_fitness() for p in population)
    top = 0
    for p in population:
        f = p.get_fitness()/total
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
