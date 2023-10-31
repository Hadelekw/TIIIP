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


def run():
    traci.start(['sumo', '-c', BASE_SUMO_CONFIG_FILE_PATH, '--junction-taz'])

    vehicles_per_step = []

    for step in range(1000):
        vehicles_per_step.append(len(traci.vehicle.getIDList()))
        traci.simulationStep()

    print(vehicles_per_step)
    
    traci.close()

