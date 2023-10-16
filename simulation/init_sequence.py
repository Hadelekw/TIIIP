"""
 File containing all the initial procedures for simulation.
 It ensures the proper sequence of events and checks if the
 necessary elements exist. If not, it writes our proper errors.
"""

import sys
sys.path.append('../')

import json

from TIIIP.network_mixer import load_base_file
from settings import BASE_FLOW_FILE_PATH, VALIDATE_FLOW_DATA


def init():
    """
     The main procedure.
    """
    environment, components = load_base_file()
    flow_file = open(BASE_FLOW_FILE_PATH)
    flow_data = json.load(flow_file); flow_file.close()
    if VALIDATE_FLOW_DATA:
        validate_flow_data(flow_data)
    flow_data = solve_flow_matrix(flow_data)


def validate_flow_data(flow_data:dict):
    """
     Validates the values typed into the flow file. The sum of the flow into the simulation
     has to be equal to the amount of flow out the simulation. Technically it is possible
     for them not to be equal but it'd result in percentages greater than 1, therefore
     flow higher than anticipated. This can be turned off in the settings.
    """
    in_flow_sum = 0; out_flow_sum = 0
    for data in flow_data.values():
        if 'outside_connections' in data:
            in_flow_sum += sum([flow for flow in data['flow'].values()])
        else:
            out_flow_sum += sum([flow for flow in data['flow'].values()])
    if in_flow_sum != out_flow_sum:
        raise Exception('Flow into the simulation is not equal to the flow out of the simulation.')
    return True


def solve_flow_matrix(flow_data:dict):
    """
     Using the data in .JSON flow file this function calculates the
     percentages of vehicles going from one outside connection to another
    """
    result = {}
    out_edges = {}
    for edge_id, data in flow_data.items():
        if 'outside_connections' in data:
            result[edge_id] = data['flow'].copy()
        else:
            out_edges[edge_id] = data['flow']
    for edge_id, data in flow_data.items():
        if 'outside_connections' in data:
            for vehicle_type in result[edge_id]:
                result[edge_id][vehicle_type] = {}
                for out_vehicle_type, out_edge_ids in data['outside_connections'].items():
                    if vehicle_type == out_vehicle_type:
                        for out_edge_id in out_edge_ids:
                            result[edge_id][vehicle_type][out_edge_id] = data['flow'][vehicle_type] / out_edges[out_edge_id][vehicle_type]
    return result


def generate_rou_xml(flow_file_path:str):
    """
     Generates a file describing many possible trips of vehicles based
     on data described in .JSON flow file.
    """
    pass
