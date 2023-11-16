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


def generate_population(population, data):
    result = []

    scores = [evaluate(sim_result) for sim_result in data.values()]
    population_scores = {specimen: score for specimen, score in zip(population, scores)}
    population_scores = dict(sorted(population_scores.items(), key=lambda item: item[1], reverse=True))
    best_scorers = []
    while len(population_scores) > SPARED_PERCENTAGE * NUMBER_PER_GENERATION:
        population_scores.popitem()
    for specimen in population_scores:
        result.append(specimen)
        best_scorers.append(specimen)
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
