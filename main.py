"""
 File implementing the solutions.
"""


import network_mixer, simulation, genetics
from .settings import *


def main():
    environment, components = load_base_file()
    simulation.init_with_components(environment, components)
    data = simulation.run()
    evaulated_data = genetics.evaluate(data)


def run_cycle(road_file_path, flow_file_path, routes_file_path, sumo_config_path, generations=10, n_for_generation=20):
    for i in range(generations):
        for j in range(n_for_generation):


def get_base(road_file_path=BASE_ROAD_FILE_PATH, flow_file_path=BASE_FLOW_FILE_PATH, routes_file_path=BASE_ROUTES_FILE_PATH, sumo_config_path=BASE_SUMO_CONFIG_FILE_PATH):
    return # specimen


if __name__ == '__main__':
    main()
