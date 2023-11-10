"""
 File defining the Specimen class which holds data for road files.
"""


class Specimen:

    def __init__(self, generation, environment, components):
        self.generation = generation
        self.environment = environment
        for component_type, component in components.items():
            setattr(self, component_type, component)


def generate_traffic_lights_matrix(specimen_list):
    result = []
    for specimen in specimen_list:
        pass
