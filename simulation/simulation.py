"""
 File responsible for the simulation part of the process.
 It runs the simulation for the particular set of files and
 collects all the necessary data. 
 It is done via SUMO TraCI interface (https://pypi.org/project/traci/).
"""

import sys
sys.path.append('../')

import traci

from settings import BASE_SUMO_CONFIG_FILE_PATH


DATA_SCHEMA = {
    'arrived_per_step': [],
    'vehicles_per_step': [],
    'co2_emissions_per_step': [],
    # 'average_co2_emissions_per_step_per_liter': [],
}


def run(sumo_config_file_path=BASE_SUMO_CONFIG_FILE_PATH):
    traci.start(['sumo', '-c', sumo_config_file_path, '--junction-taz'])

    data = DATA_SCHEMA

    bot_left, top_right = traci.simulation.getNetBoundary()
    total_area_of_simulation = (top_right[0] - bot_left[0]) * (top_right[1] - bot_left[1])

    for step in range(1000):
        data['arrived_per_step'].append(len(traci.simulation.getArrivedIDList()))
        data['vehicles_per_step'].append(traci.vehicle.getIDCount())
        data['co2_emissions_per_step'].append(sum([traci.vehicle.getCO2Emission(vehicle_id) for vehicle_id in traci.vehicle.getIDList()]))
        # data['average_co2_emissions_per_step_per_liter'].append(list([co2_emission / area_of_simulation for co2_emission in data['co2_emissions_per_step']]))
        traci.simulationStep()
    
    traci.close()

    return data
