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
    'vehicles_per_step': []
}


def run():
    traci.start(['sumo', '-c', BASE_SUMO_CONFIG_FILE_PATH, '--junction-taz'])

    data = DATA_SCHEMA

    for step in range(1000):
        data['vehicles_per_step'].append(len(traci.vehicle.getIDList()))
        traci.simulationStep()
    
    traci.close()

    return data
