"""
 File containing functions evaluating the results of simulation.
"""

import sys
sys.path.append('../')

from simulation import DATA_SCHEMA


def evaluate(data):
    result = 0
    new_data = {}
    if 'vehicles_per_step' in DATA_SCHEMA:
        new_data['total_vehicles'] = sum(data['vehicles_per_step'])
    if 'co2_emissions_per_step' in DATA_SCHEMA:
        new_data['total_co2_emissions'] = sum(data['co2_emissions_per_step'])
    result = -sum([new_data[key] for key in new_data])
    return result
