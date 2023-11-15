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
    while len(population_scores) > SPARE_PERCENTAGE * NUMBER_PER_GENERATION:
        population_scores.popitem()
    for specimen in population_scores:
        result.append(specimen)
    while len(result) != NUMBER_PER_GENERATION:
        # randomly choose a pair of parents for the new generation for crossover
        # later apply some minor mutations
    return result
