"""
 File containing functions evaluating the results of simulation.
"""

import sys
sys.path.append('../')

from simulation import DATA_SCHEMA


def evaluate(sim_data):
    result = 0
    data = {}
    if 'arrived_per_step' in DATA_SCHEMA:
        data['total_arrived'] = sum(sim_data['arrived_per_step'])
    if 'vehicles_per_step' in DATA_SCHEMA:
        data['total_vehicles'] = sum(sim_data['vehicles_per_step'])
        data['average_vehicles'] = data['total_vehicles'] / len(sim_data['vehicles_per_step'])
    if 'co2_emissions_per_step' in DATA_SCHEMA:
        data['total_co2_emissions'] = sum(sim_data['co2_emissions_per_step'])
    result = data['total_arrived'] - data['average_vehicles']
    return result
