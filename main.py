"""
 File implementing the solutions.
"""

import os
import copy

import matplotlib.pyplot as plt

import network_mixer, simulation, genetics
from settings import *


def main(n_generations=NUMBER_OF_GENERATIONS, n_per_generation=NUMBER_PER_GENERATION, results_path=BASE_RESULTS_PATH):
    dirs = create_directories()
    if not dirs:
        os.makedirs('{}/0'.format(results_path))
    else:
        last_dir = max([int(d) for d in dirs])
        os.makedirs('{}/{}'.format(results_path, last_dir + 1))
    base_specimen = get_base_specimen()
    population = genetics.generate_new_population(base_specimen)

    log_file = open('{}/log.log'.format(results_path), 'w+')
    average_scores_per_generation = []
    max_score_per_generation = []

    for i in range(n_generations):
        for j in range(n_per_generation):
            if not os.path.exists('{}/{}'.format(results_path, i)):
                os.makedirs('{}/{}'.format(results_path, i))
            population[j].build_file('{}/{}/{}.net.xml'.format(results_path, i, j))
            simulation.generate_sumo_config('{}/{}/{}.sumocfg'.format(results_path, i, j), '{}.net.xml'.format(j), '../../{}'.format(BASE_ROUTES_FILE_PATH))
        for j in range(n_per_generation):
            print('------------\nGENERATION {}/{} SPECIMEN {}/{}\n------------'.format(i + 1, n_generations, j + 1, n_per_generation))
            population[j].sim_data = simulation.run('{}/{}/{}.sumocfg'.format(results_path, i, j))
            population[j].score = genetics.evaluate(population[j].sim_data)
            log_file.write(population[j].get_log(i, j))
        average_scores_per_generation.append(sum([specimen.score for specimen in population]) / len(population))
        max_score_per_generation.append(max([specimen.score for specimen in population]))
        population = genetics.generate_population(population)
    plt.plot(range(len(average_scores_per_generation)), average_scores_per_generation)
    plt.plot(range(len(max_score_per_generation)), max_score_per_generation)
    plt.show()


def get_base_specimen(road_file_path=BASE_ROAD_FILE_PATH, flow_file_path=BASE_FLOW_FILE_PATH, routes_file_path=BASE_ROUTES_FILE_PATH, sumo_config_path=BASE_SUMO_CONFIG_FILE_PATH):
    environment, components = simulation.init(road_file_path, flow_file_path, routes_file_path, sumo_config_path)
    specimen = genetics.Specimen(environment, components, 'BASE')
    return specimen


def create_directories(results_path=BASE_RESULTS_PATH):
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    dirs = os.listdir(results_path)
    return dirs

if __name__ == '__main__':
    main()
