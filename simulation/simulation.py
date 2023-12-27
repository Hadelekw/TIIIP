"""
 File responsible for the simulation part of the process.
 It runs the simulation for the particular set of files and
 collects all the necessary data. 
 It is done via SUMO TraCI interface (https://pypi.org/project/traci/).
"""

import sys
sys.path.append('../')

import traci

from settings import BASE_SUMO_CONFIG_FILE_PATH, SIMULATION_TIME


DATA_SCHEMA = {
    'arrived_per_step': [],
    'vehicles_per_step': [],
    'collisions_per_step': [],
    'teleported_per_step': [],
    # 'co2_emissions_per_step': [],
    'final_vehicles': [],
}


def run(sumo_config_file_path=BASE_SUMO_CONFIG_FILE_PATH):
    traci.start(['sumo', '-c', sumo_config_file_path, '--junction-taz'])

    data = DATA_SCHEMA
    for key in data:
        data[key] = []

    for step in range(SIMULATION_TIME):
        data['arrived_per_step'].append(traci.simulation.getArrivedNumber())
        if 'vehicles_per_step' in DATA_SCHEMA:
            data['vehicles_per_step'].append(traci.vehicle.getIDCount())
        if 'collisions_per_step' in DATA_SCHEMA:
            data['collisions_per_step'].append(traci.simulation.getCollidingVehiclesNumber())
        if 'teloported_per_step' in DATA_SCHEMA:
            data['teleported_per_step'].append(traci.simulation.getStartingTeleportNumber())
        if 'co2_emissions_per_step' in DATA_SCHEMA:
            data['co2_emissions_per_step'].append(sum([traci.vehicle.getCO2Emission(vehicle_id) for vehicle_id in traci.vehicle.getIDList()]))
        traci.simulationStep()

    data['final_vehicles'] = traci.vehicle.getIDCount()
    traci.close()

    return data
