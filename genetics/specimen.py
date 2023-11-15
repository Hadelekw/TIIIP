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
        for component_type, component in components.items():
            setattr(self, component_type, component)

    @property
    def components(self):
        attrs = self.__dict__
        attrs.pop('parents')
        attrs.pop('environment')
        return attrs

    def build_file(self, save_file_path):
        build_file(self.environment, self.components, save_file_path)


def mutate(specimen):
    # while not validate_tllogic(specimen.tlLogic):
    for tllogic in specimen.tlLogic.values():
        mixer.generate_tl_program(tllogic)
    return specimen


def validate_tllogic(tllogic):
    pass
