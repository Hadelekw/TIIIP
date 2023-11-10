"""
 File containing functions evaluating the results of simulation.
"""

import sys
sys.path.append('../')

from simulation import DATA_SCHEMA


def evaluate(data):
    result = {}
    if 'vehicles_per_step' in DATA_SCHEMA:
        result['total_vehicles'] = sum(data['vehicles_per_step'])
    if 'co2_emissions_per_step' in DATA_SCHEMA:
        result['total_co2_emissions'] = sum(data['co2_emissions_per_step'])
    return result
