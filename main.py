"""
 File implementing the solutions.
"""

import copy

import network_mixer, simulation, genetics
from settings import *


def main(n_generations=NUMBER_OF_GENERATIONS, n_per_generation=NUMBER_PER_GENERATION):
    base_specimen = get_base_specimen()
    population = [genetics.mutate(copy.deepcopy(base_specimen)) for _ in range(n_per_generation)]
    n = 0
    for specimen in population:
        specimen.build_file('generations/{}.net.xml'.format(n))
        n += 1
    for i in range(n_generations):
        for j in range(n_per_generation):
            run_cycle('generations/{}/{}/sumo_config.cumocfg'.format(i, j))


def run_cycle():
    data = simulation.run()


def get_base_specimen(road_file_path=BASE_ROAD_FILE_PATH, flow_file_path=BASE_FLOW_FILE_PATH, routes_file_path=BASE_ROUTES_FILE_PATH, sumo_config_path=BASE_SUMO_CONFIG_FILE_PATH):
    environment, components = simulation.init(road_file_path, flow_file_path, routes_file_path, sumo_config_path)
    specimen = genetics.Specimen(environment, components)
    return specimen


if __name__ == '__main__':
    main()
