from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *

def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def roulette_wheel_selection(items, knapsack_max_capacity, population):
    fitness_values = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    total_fitness = sum(fitness_values)

    if total_fitness == 0:
        return random.choice(population) 
    
    p = [fitness_value / total_fitness for fitness_value in fitness_values]
    selected_index = random.choices(range(len(population)), weights=p, k=1)[0]
    
    return population[selected_index]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def mutate(individual, mutation_rate=0.01):
    mutated_individual = individual[:]
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutated_individual[i] = not mutated_individual[i] 
    return mutated_individual

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 20
n_elite = 1
mutation_rate = 0.01

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
for _ in range(generations):
    population_history.append(population)

    # implement genetic algorithm
    sorted_population = sorted(population, key=lambda ind: fitness(items, knapsack_max_capacity, ind), reverse=True)
    new_population = sorted_population[:n_elite]

    while len(new_population) < population_size:
        parent1 = roulette_wheel_selection(items, knapsack_max_capacity, population)
        parent2 = roulette_wheel_selection(items, knapsack_max_capacity, population)

        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1, mutation_rate))
        if len(new_population) < population_size:
            new_population.append(mutate(child2, mutation_rate))

    population = new_population

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.savefig("output.png")
#plt.show()
