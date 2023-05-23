'''arpga/core.py'''

import numpy as np
import math


def init_population(population_size, chromosome_size):
    '''Initialize the population'''

    '''In this case chromosome_size is the number of tracks'''
    population = np.zeros((population_size, chromosome_size))

    for i in range(population_size):
        population[i, :] = np.random.permutation(chromosome_size)

    return population


def fitness(chromosome, radius, width):
    cons = 1
    j = 1
    c = 0

    # Condition that rmin > width/2
    if radius > (width/2):
        cons = (2*radius)/width

    # Calculate total distance for each track segment
    for i in range(len(chromosome)-1):
        turn = abs(chromosome[i] - chromosome[i+1])

        if np.any(turn >= cons):
            # U-turn
            c += (math.pi - 2) * radius + width * turn
        else:
            # Omega-turn
            c += radius * (3 * math.pi - 4 *
                           math.asin((2 * radius + width * turn)/(4 * radius)))

    # Add Penalty if first track(start point) and last track(end point) are not in first and second track respectively
    if np.any(chromosome[0] != 0):
        c += 50
    elif np.any(chromosome[len(chromosome)-1] != 1):
        c += 50

    return c


def mate(father, mother):
    '''Crossover'''
    # # Return the father if the father or mother is empty
    # if np.all(father == 0):
    #     father = mutate(mother)
    # if np.all(mother == 0):
    #     mother = mutate(father)
        
    # #if both are empty
    # if np.all(father == 0) and np.all(mother == 0):
    #     # create a random chromosome
    #     father = np.random.permutation(len(father))
    #     mother = np.random.permutation(len(mother))
        

    # Randomly select a crossover point, make sure that crossover point is not the first or the last track and the crossover point is not the same
    crossover_point = np.sort(np.random.choice(
        len(father)-1, 2, replace=False)+1)

   # Create offspring
    offspring = np.zeros((2, len(father)))

    # Create 2 segments from father and mother
    offspring[0, crossover_point[0]:crossover_point[1]
              ] = father[crossover_point[0]:crossover_point[1]]
    offspring[1, crossover_point[0]:crossover_point[1]
              ] = mother[crossover_point[0]:crossover_point[1]]

    # Fill the rest of the offspring with the remaining tracks from mother and father
    restm = np.setdiff1d(
        mother, offspring[0, crossover_point[0]:crossover_point[1]], assume_unique=True)
    restf = np.setdiff1d(
        father, offspring[1, crossover_point[0]:crossover_point[1]], assume_unique=True)

    offspring[0, :crossover_point[0]] = restm[:crossover_point[0]]
    offspring[0, crossover_point[1]:] = restm[crossover_point[0]:]

    offspring[1, :crossover_point[0]] = restf[:crossover_point[0]]
    offspring[1, crossover_point[1]:] = restf[crossover_point[0]:]

    return offspring


def mutate(chromosome):
    '''Mutation'''

    # Randomly select a mutation point
    mutation_point = np.random.choice(len(chromosome), 2, replace=False)

    prob = np.random.randint(1, 4)

    # Flip the mutation point in k == 1
    if prob == 1:
        chromosome[mutation_point[0]: mutation_point[1]] = np.flip(
            chromosome[mutation_point[0]: mutation_point[1]])

    # Swap the mutation point in k == 2
    elif prob == 2:
        chromosome[mutation_point[0]], chromosome[mutation_point[1]
                                                  ] = chromosome[mutation_point[1]], chromosome[mutation_point[0]]

    # slide the mutation point in k == 3
    elif prob == 3:
        chromosome = np.roll(chromosome, np.random.randint(1, len(chromosome)))

    return chromosome


def new_generation(population, fitness, pSize):
    '''Create new generation'''

    new_gen = np.zeros((pSize, len(population[0])))

    # Sorted Fitness from the shortest distance to the longest distance
    sorted_fitness = np.argsort(fitness)

    # Copy the best 10% of the population to the new generation (the most shortest distance)
    for i in range(int(pSize*0.1)):
        new_gen[i, :] = population[sorted_fitness[i], :]

    # GA Operator
    sum_fitness = np.sum(fitness)
    probability_fitness = fitness/sum_fitness
    cummulative_pf = np.cumsum(probability_fitness)

    # Perform crossover and mutation to the rest of the population
    for i in range(int(pSize*0.1), pSize-1, 2):
        if np.random.rand() < 0.7:

            indexf = np.where(cummulative_pf >= np.random.rand())[0][0]
            indexm = np.where(cummulative_pf >= np.random.rand())[0][0]

            father = population[indexf, :]
            mother = population[indexm, :]
            
            if np.all(father == 0) or np.all(mother == 0):
                # stop the loop if both are empty
                continue

            offspring = mate(father, mother)
            new_gen[i, :] = offspring[0, :]
            new_gen[i+1, :] = offspring[1, :]
        if np.random.rand() <= 0.2:
            index_random = np.where(cummulative_pf >= np.random.rand())[0][0]

            random_chromosome = population[index_random, :]

            new_gen[i, :] = mutate(random_chromosome)

    return new_gen


def run_arpga(track, width, radius, maxGen, pSize, runNumbers):
    """Run ARP Genetic Algorithm"""

    best_fitness_generation = np.zeros((runNumbers, maxGen))
    best_fitness = np.zeros(runNumbers)
    best_solution = np.zeros((runNumbers, track))

    for run in range(runNumbers):
        # Initialize population
        population = init_population(pSize, track)
        fitness_population = np.zeros(pSize)

        for j in range(pSize):
            fitness_population[j] = fitness(population[j, :], radius, width)

        index = np.argmin(fitness_population)
        best_solution_run = population[index, :].copy()
        best_ga = fitness_population[index]

        best_current_gen = population[index, :].copy()

        # Run the algorithm
        for i in range(maxGen):
            # Calculate fitness
            for j in range(pSize):
                fitness_population[j] = fitness(
                    population[j, :], radius, width)

            # Get Index of best fitness
            index = np.argmin(fitness_population)
            best_fitness_generation[run, i] = fitness_population[index]
            best_current_gen = population[index, :].copy()

            if (best_ga > fitness_population[index]):
                best_ga = fitness_population[index]
                best_solution_run = best_current_gen.copy()

            # Create new generation
            population = new_generation(population, fitness_population, pSize)

        best_fitness[run] = best_ga
        best_solution[run, :] = best_solution_run

    # Get the best fitness and solution from all runs
    best_fitness_all = np.min(best_fitness)
    best_solution_all = best_solution[np.argmin(best_fitness), :]

    return best_fitness_all, best_solution_all
