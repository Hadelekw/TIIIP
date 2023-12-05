"""
 File containing function for generating a new population.
"""

import sys
sys.path.append('../')

import random

import network_mixer.mixer as mixer
from settings import NUMBER_PER_GENERATION, SPARED_PERCENTAGE
from simulation import DATA_SCHEMA
from . import *


def generate_population(population):
    result = []
    population_scores = [(specimen, specimen.score) for specimen in population]
    population_scores = sorted(population_scores, key=lambda x: x[1], reverse=True)
    print(SPARED_PERCENTAGE * NUMBER_PER_GENERATION)
    print(population_scores)
    population_scores = population_scores[:int(SPARED_PERCENTAGE * NUMBER_PER_GENERATION)]
    best_scorers = [score[0] for score in population_scores]
    
    result.extend(best_scorers)
    while len(result) != NUMBER_PER_GENERATION:
        chance = random.random()
        if chance > 0.5:  # crossover
            parents = random.sample(best_scorers, 2)
            new_specimen = crossover(parents)
        else:  # mutation
            base_specimen = random.choice(best_scorers)
            new_specimen = mutate(base_specimen)
        result.append(new_specimen)
    return result


def degenerate_population(population, data):
    result = []

    # scores = [evaluate(sim_result) for sim_result in data.values()]
    # population_scores = {specimen: score for specimen, score in zip(population, scores)}
    # population_scores = dict(sorted(population_scores.items(), key=lambda item: item[1], reverse=True))
    population_scores = {key: evaluate(value) for key, value in data.items()}
    best_scorers = []
    print(population_scores)
    while len(population_scores) > SPARED_PERCENTAGE * NUMBER_PER_GENERATION:
        population_scores.pop()
    for specimen in population_scores:
        result.append(specimen)
        best_scorers.append(specimen)
    print(best_scorers)
    while len(result) != NUMBER_PER_GENERATION:
        chance = random.random()
        if chance > 0.5:  # crossover
            parents = random.sample(best_scorers, 2)
            new_specimen = crossover(parents)
        else:  # mutation
            base_specimen = random.choice(best_scorers)
            new_specimen = mutate(base_specimen)
        result.append(new_specimen)
    return result
