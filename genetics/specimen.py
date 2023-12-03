"""
 File defining the Specimen class which holds data for road files and all functions relating to it.
"""

import sys
sys.path.append('../')

import random

from network_mixer import build_file
import network_mixer.mixer as mixer


class Specimen:

    def __init__(self, environment, components, parents=None):
        self.parents = parents
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
    for tllogic in specimen.tlLogic.values():
        chance = random.random()
        if chance < 0.3:
            mixer.generate_tl_program(tllogic)
        else:
            pass
    specimen.update_components()
    return specimen


def crossover(parents):
    result = parents[0]
    for key, value in parents[1].tlLogic.items():
        if random.random() > 0.5:
            result.tlLogic[key] = value
    result.parents = parents
    result.update_components()
    return result


def validate_tllogic(tllogic):
    pass
