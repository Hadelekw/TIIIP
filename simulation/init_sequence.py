"""
 File containing all the initial procedures for simulation.
 It ensures the proper sequence of events and checks if the
 necessary elements exist. If not, it writes our proper errors.
"""

import sys
sys.path.append('../')

import json

from TIIIP.network_mixer import load_base_file
from settings import BASE_FLOW_FILE_PATH


def init():
    """
     The main procedure.
    """
    environment, components = load_base_file()
    flow_file = open(BASE_FLOW_FILE_PATH)
    flow_data = json.load(flow_file); flow_file.close()
    flow_data = solve_flow_matrix(flow_data)


def solve_flow_matrix(flow_data:dict):
    """
     Using the data in .JSON flow file this function calculates the
     percentages of vehicles going from one outside connection to another
    """
    result = {}
    out_edges = {}
    in_edges = {}
    for edge_id, data in flow_data.items():
        if 'available_outside_connections' in data:
            in_edges[edge_id] = data
        else:
            out_edges[edge_id] = data
            result[edge_id] = {key:[] for key in data['flow']}

    for in_edge_id, in_edge_data in in_edges.items():
        for out_edge_id in in_edge_data['available_outside_connections']:
            for vehicle_type, vehicle_flow in in_edge_data['flow'].items():
                result[out_edge_id][in_edge_data['flow'][vehicle_type]].append(vehicle_flow)
    print(result)


def generate_rou_xml(flow_file_path:str):
    """
     Generates a file describing many possible trips of vehicles based
     on data described in .JSON flow file.
    """
    pass
