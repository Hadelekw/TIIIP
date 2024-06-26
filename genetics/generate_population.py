"""
 File containing function for generating a new population.
"""

import sys
sys.path.append('../')

import random
import copy
import uuid

import network_mixer.mixer as mixer
from settings import NUMBER_PER_GENERATION, SPARED_PERCENTAGE, BAD_SURVIVAL_CHANCE, MAX_MUTATION_COUNT, MIN_MUTATION_COUNT
from simulation import DATA_SCHEMA
from . import *


def pop_random_specimen(population):
    idx = random.randrange(0, len(population))
    return population.pop(idx)


def generate_population(population):
    result = []
    population_scores = [(specimen, specimen.score) for specimen in population]
    population_scores = sorted(population_scores, key=lambda x: x[1], reverse=True)
    org_population_scores = population_scores
    population_scores = population_scores[:int(SPARED_PERCENTAGE * NUMBER_PER_GENERATION)]
    best_scorers = [score[0] for score in population_scores]

    for _ in range(random.randint(MIN_MUTATION_COUNT, MAX_MUTATION_COUNT)):
        if random.random() < BAD_SURVIVAL_CHANCE:
            best_scorers.append(random.choice(org_population_scores)[0])

    result.extend(best_scorers)
    while len(result) < NUMBER_PER_GENERATION:
        chance = random.random()
        if chance > 0.5 and len(best_scorers) > 2:  # crossover
            parents = pop_random_specimen(best_scorers), pop_random_specimen(best_scorers)
            new_specimen = crossover(parents)
            new_specimen.id = uuid.uuid4()
        else:  # mutation
            base_specimen = random.choice(best_scorers)
            new_specimen = mutate(base_specimen)
            new_specimen.id = uuid.uuid4()
        result.append(new_specimen)
    return result


def generate_new_population(base_specimen):
    result = []
    tllogic_ids = [tllogic.id for tllogic in base_specimen.tlLogic.values()]
    length = [len(tllogic._phases[0].state) for tllogic in base_specimen.tlLogic.values()]
    for i in range(NUMBER_PER_GENERATION):
        new_specimen = copy.deepcopy(base_specimen)
        new_specimen.id = 'B{}'.format(i)
        new_specimen.tlLogic = {}
        i = 0
        for id_ in tllogic_ids:
            new_specimen.tlLogic[id_] = mixer.generate_tllogic(id_, length[i], base_specimen.junction[id_]._requests)
            i += 1
        new_specimen.update_components()
        result.append(new_specimen)
    return result
