"""
 File defining the Specimen class which holds data for road files and all functions relating to it.
"""

import sys
sys.path.append('../')

import random
import copy

from network_mixer import build_file
import network_mixer.mixer as mixer
from settings import MIN_MUTATION_COUNT, MAX_MUTATION_COUNT


class Specimen:

    def __init__(self, environment, components, id_=''):
        self.id = id_
        self.sim_data = []
        self.score = 0
        self.environment = environment
        self.components = components
        for component_type, component in components.items():
            setattr(self, component_type, component)

    def build_file(self, save_file_path):
        build_file(self.environment, self.components, save_file_path)

    def update_components(self):
        for component in self.components:
            self.components[component] = getattr(self, component)

    def get_log(self, generation, n):
        result = 'GEN {} N {} ID {} '.format(generation, n, self.id)
        result += 'SCORE {}'.format(self.score)
        for tllogic in self.tlLogic.values():
            result += ' TL {}['.format(tllogic.id)
            for phase in tllogic._phases:
                result += '{},'.format(''.join([state.value for state in phase.state]))
            result = result[:-1]
            result += ']'
        result += '\n'
        return result


def mutate(specimen):
    new_specimen = copy.deepcopy(specimen)
    for id_, tllogic in specimen.tlLogic.items():
        new_specimen.tlLogic[id_] = mixer.mutate_tl_program(tllogic, specimen.junction[id_]._requests, MIN_MUTATION_COUNT, MAX_MUTATION_COUNT)
    new_specimen.update_components()
    return new_specimen


def crossover(parents):
    result = copy.deepcopy(parents[0])
    while result.tlLogic == parents[0].tlLogic:
        for key, value in parents[1].tlLogic.items():
            chance = random.random()
            if chance > 0.8:
                result.tlLogic[key] = value
            elif chance > 0.4:
                result.tlLogic[key]._phases[random.randint(0, len(result.tlLogic[key]._phases))] = copy.deepcopy(random.choice(value._phases))
    result.update_components()
    return result
