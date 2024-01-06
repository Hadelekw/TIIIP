"""
 File containing all the initial procedures for simulation.
 It ensures the proper sequence of events and checks if the
 necessary elements exist. If not, it writes our proper errors.
"""

import sys
sys.path.append('../')

import json

import network_mixer
from .routes_flows import Flow
from .vehicle_classes import VEHICLE_CLASSES
from settings import BASE_FLOW_FILE_PATH, VALIDATE_FLOW_DATA, BASE_ROAD_FILE_PATH, BASE_ROUTES_FILE_PATH, BASE_SUMO_CONFIG_FILE_PATH, VEHICLE_GENERATION_TIME


def init(road_file_path=BASE_ROAD_FILE_PATH, flow_file_path=BASE_FLOW_FILE_PATH, routes_file_path=BASE_ROUTES_FILE_PATH, sumo_config_file_path=BASE_SUMO_CONFIG_FILE_PATH):
    """
     The main initial procedure.
    """
    environment, components = network_mixer.load_file(road_file_path)
    flow_file = open(flow_file_path)
    flow_data = json.load(flow_file); flow_file.close()
    if VALIDATE_FLOW_DATA:
        validate_flow_data(flow_data)
    flow_data = solve_flow_matrix(flow_data, components)
    average_flow = sum([flow.vehsPerHour for flow in flow_data.values()]) / len(flow_data)
    vehicle_types = get_vehicle_types()
    generate_rou_xml(environment, components, vehicle_types, flow_data, routes_file_path)
    generate_sumo_config(sumo_config_file_path, road_file_path, routes_file_path)
    return environment, components, average_flow


def validate_flow_data(flow_data:dict):
    """
     Validates the values typed into the flow file. The sum of the flow into the simulation
     has to be equal to the amount of flow out the simulation. Technically it is possible
     for them not to be equal but it'd result in percentages not summing properly. 
     This can be turned off in the settings.
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


def solve_flow_matrix(flow_data:dict, components:dict, end=VEHICLE_GENERATION_TIME):
    result = {}
    in_edges = {}; out_edges = {}
    for edge_id, data in flow_data.items():
        if 'outside_connections' in data:
            in_edges[edge_id] = data
        else:
            out_edges[edge_id] = data
    for in_edge_id, in_data in in_edges.items():
        out_flow = {vehicle_type:0 for vehicle_type in in_data['flow']}
        for vehicle_type, outside_connections in in_data['outside_connections'].items():
            for outside_connection_id in outside_connections:
                out_flow[vehicle_type] += out_edges[outside_connection_id]['flow'][vehicle_type]
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
                        vehsPerHour=round(out_data['flow'][vehicle_type] / out_flow[vehicle_type] * in_data['flow'][vehicle_type], 2)
                    )
    return result


def get_vehicle_types():
    """
     Creates Vehicle objects from classes defined in vehicle_classes.py
    """
    result = {}
    for key, value in VEHICLE_CLASSES.items():
        result[key] = value()
    return result


def generate_rou_xml(environment, components:dict, vehicle_types:dict, solved_flow_data:dict, save_file_path:str):
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


def generate_sumo_config(save_file_path:str, road_file_path:str, routes_file_path:str):
    """
     Writes a file collecting the road file and routes file.
    """
    with open(save_file_path, 'w+') as f:
        f.write('<configuration>\n')
        f.write('    <n v=\"{}\"/>\n'.format(road_file_path))
        f.write('    <r v=\"{}\"/>\n'.format(routes_file_path))
        f.write('</configuration>')
