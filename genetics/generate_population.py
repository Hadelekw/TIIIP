"""
 File containing function for generating a new population.
"""

import sys
sys.path.append('../')

import random
import copy

import network_mixer.mixer as mixer
from settings import NUMBER_PER_GENERATION, SPARED_PERCENTAGE
from simulation import DATA_SCHEMA
from . import *


def generate_population(population):
    result = []
    population_scores = [(specimen, specimen.score) for specimen in population]
    population_scores = sorted(population_scores, key=lambda x: x[1], reverse=True)
    # print(SPARED_PERCENTAGE * NUMBER_PER_GENERATION)
    # print(population_scores)
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


def generate_new_population(base_specimen):
    result = []
    print(base_specimen.tlLogic)
    tllogic_ids = [tllogic.id for tllogic in base_specimen.tlLogic.values()]
    for _ in range(NUMBER_PER_GENERATION):
        new_specimen = copy.deepcopy(base_specimen)
        new_specimen.tlLogic = {}
        for id_ in tllogic_ids:
            new_specimen.tlLogic[id_] = mixer.generate_tllogic(id_)
        new_specimen.update_components()
        result.append(new_specimen)
    return result
