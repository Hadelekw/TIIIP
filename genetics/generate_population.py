"""
 File containing function for generating a new population.
"""

import sys
sys.path.append('../')

import network_mixer.mixer as mixer
from simulation import DATA_SCHEMA
from specimen import *
from evaluation import evaluate


def generate_population(population, data):
    result = []

    scores = [evaluate(sim_result) for sim_result in data.values()]
    population_scores = {specimen: score for specimen, score in zip(population, scores)}

    # figure out how to sort them and remove the weaklings
    # then create new population by crossing and mutations

    return result
