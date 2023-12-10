"""
 File defining the Specimen class which holds data for road files and all functions relating to it.
"""

import sys
sys.path.append('../')

import random
import copy

from network_mixer import build_file
import network_mixer.mixer as mixer


class Specimen:

    def __init__(self, environment, components):
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


def mutate(specimen):
    # while not validate_tllogic(specimen.tlLogic):
    new_specimen = copy.deepcopy(specimen)
    for id_, tllogic in specimen.tlLogic.items():
        new_specimen.tlLogic[id_] = mixer.mutate_tl_program(tllogic)
    new_specimen.update_components()
    # print(new_specimen.tlLogic)
    return new_specimen


def crossover(parents):
    result = copy.deepcopy(parents[0])
    while result.tlLogic == parents[0].tlLogic:
        for key, value in parents[1].tlLogic.items():
            if random.random() > 0.5:
                result.tlLogic[key] = value
    result.update_components()
    return result


def validate_tllogic(tllogic):
    pass
