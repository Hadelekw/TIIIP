"""
 File containing all the initial procedures for simulation.
 It ensures the proper sequence of events and checks if the
 necessary elements exist. If not, it writes our proper errors.
"""

import sys
sys.path.append('../')

import json

from TIIIP.network_mixer import load_base_file, Environment
from .routes_flows import Flow
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
    flow_data = solve_flow_matrix(flow_data, components)
    vehicle_types = get_vehicle_types()
    generate_rou_xml(environment, components, vehicle_types, flow_data, 'test_2.rou.xml')


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


def solve_flow_matrix(flow_data:dict, components:dict, end=7200):
    result = {}
    in_edges = {}; out_edges = {}
    for edge_id, data in flow_data.items():
        if 'outside_connections' in data:
            in_edges[edge_id] = data
        else:
            out_edges[edge_id] = data
    for in_edge_id, in_data in in_edges.items():
        for out_edge_id, out_data in out_edges.items():
            for vehicle_type in in_data['outside_connections']:
                if out_edge_id in in_data['outside_connections'][vehicle_type]:
                    result['{}_{}'.format(in_edge_id, out_edge_id)] = Flow(
                        id='{}_{}'.format(in_edge_id, out_edge_id),
                        type=vehicle_type,
                        begin=0,
                        color='yellow',
                        fromJunction=components['edge'][in_edge_id]._from,
                        toJunction=components['edge'][out_edge_id]._to,
                        end=end,
                        vehsPerHour=in_data['flow'][vehicle_type] / out_data['flow'][vehicle_type]
                    )
    return result


def get_vehicle_types():
    return {}  # temp


def generate_rou_xml(environment:Environment, components:dict, vehicle_types:dict, solved_flow_data:dict, save_file_path:str):
    """
     Generates a file describing many possible trips of vehicles based
     on data described in .JSON flow file.
    """
    with open(save_file_path, 'w+') as f:
        f.write('<?xml {}?>\n\n'.format(environment.get_xml_xml_line_attribs()))
        f.write('<routes xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://sumo.dlr.de/xsd/routes_file.xsd\">\n')
        for vehicle_type in vehicle_types.values():
            f.write(vehicle_type.get_xml_line())
        for flow in solved_flow_data.values():
            f.write(flow.get_xml_line())
        f.write('</routes>')
