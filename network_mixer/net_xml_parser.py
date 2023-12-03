"""
 This file contains classes and functions for the analysis of SUMO's .NET.XML files.
 It is based on the assumption of the user using Netconvert to create the base file
 and that the data comes from a .OSM file.
"""

import sys
sys.path.append('../')

from os.path import exists
import xml.etree.ElementTree as et
import json

import simulation
from settings import BASE_ROAD_FILE_PATH, BASE_FLOW_FILE_PATH, PROMPT_FLOW_FILE_CREATION
from .components import *
from .components_functions import *


def load_file(road_file_path):
    """
     Analysis of a road file in .NET.XML format. It returns provided environment
     (xml data, net data, location data) and components (everything else which is mutable).
    """
    f = open(road_file_path, 'r')
    root = et.parse(f).getroot()
    f.close()
    f = open(road_file_path, 'r')
    xml_data = f.readline()
    for line in f:
        if line[:4] == '<net':
            net_data = line
    f.close()
    environment = Environment()
    environment.load_xml_data(xml_data)
    environment.load_net_data(net_data)
    components = {tag: {} for tag in COMPONENTS}

    for child in root:
        if child.tag == 'location':
            environment.load_location_data(child.attrib)
            continue

        if 'id' in child.attrib:
            identifier = 'id'
        elif 'index' in child.attrib:
            identifier = 'index'
        else:
            identifier = None

        if identifier:
            components[child.tag][child.attrib[identifier]] = COMPONENTS[child.tag](**child.attrib)
        else:
            components[child.tag][len(components[child.tag])] = COMPONENTS[child.tag](**child.attrib)

        for grandchild in child:
            if grandchild.tag == 'lane':
                components[child.tag][child.attrib['id']]._lanes.append(Lane(**grandchild.attrib))
            if grandchild.tag == 'request':
                components[child.tag][child.attrib['id']]._requests.append(Request(**grandchild.attrib))
            if grandchild.tag == 'phase':
                components[child.tag][child.attrib['id']]._phases.append(Phase(**grandchild.attrib))

    connect_edges_and_junctions(components)
    print('Connecting edges and junctions... [DONE]  ')
    find_and_set_outside_connections(components)
    print('Finding outside connections... [DONE]  ')
    generate_flow_file(components)

    return environment, components


def load_base_file():
    """
     load_file function specifically for base road file definied in settings.
    """
    return load_file(road_file_path=BASE_ROAD_FILE_PATH)


def generate_flow_file(components:dict):
    """
     Generates a semi-empty .JSON file with IDs of outside connection edges
     which can be then used as a template for traffic flow data.
    """
    def get_available_outside_connections(edge:Edge, vehicle_class):
        result = []
        candidate_edges = []
        for edge_ in components['edge'].values():
            if edge_._outside_connection and edge_._outside_connection_type == OutsideConnectionType('out'):
                if hasattr(edge_, 'type'):
                    if edge_.type.allow:
                        if vehicle_class in edge_.type.allow:
                            candidate_edges.append(edge_)
                    else:
                        candidate_edges.append(edge_)
                elif hasattr(edge_, 'allow'):
                    if vehicle_class in edge_.allow:
                        candidate_edges.append(edge_)
                else:
                    if edge_.id[1:] == edge.id or edge.id[1:] == edge_.id:
                        pass
        for candidate_edge in candidate_edges:
            if if_bfs(edge, candidate_edge, components):
                result.append(candidate_edge.id)
        return result

    def get_available_vehicle_types(edge:Edge, function_to_apply):
        result = {}
        if hasattr(edge, 'type'):
            if hasattr(edge.type, 'allow'):
                if edge.type.allow:
                    for vehicle in edge.type.allow:
                        result[vehicle.__name__.lower()] = function_to_apply(edge, vehicle)
                else:
                    for vehicle in simulation.VEHICLE_CLASSES:
                        result[vehicle] = function_to_apply(edge, vehicle)
        else:
            if hasattr(edge, 'allow'):
                for vehicle in edge.allow:
                    result[vehicle.__name__.lower()] = function_to_apply(edge, vehicle)
            else:
                for vehicle in simulation.VEHICLE_CLASSES:
                    result[vehicle] = function_to_apply(edge, vehicle)
        return result

    def process():
        result_json = {}
        n_processed = 0
        for edge_id, edge in components['edge'].items():
            print('Processing components to flow file... [{:.2f}%]'.format(n_processed / len(components['edge']) * 100), end='\r')  # Loading message
            if edge._outside_connection:
                if edge._outside_connection_type == OutsideConnectionType('in'):
                    result_json[edge_id] = {
                        'flow': get_available_vehicle_types(edge, lambda e,v: 500),
                        'outside_connections': get_available_vehicle_types(edge, get_available_outside_connections),
                    }
                else:
                    result_json[edge_id] = {
                        'flow': get_available_vehicle_types(edge, lambda e,v: 500),
                    }
            n_processed += 1
        with open(BASE_FLOW_FILE_PATH, 'w+') as f:
            json.dump(result_json, f, indent=4)
        print('Processing components to flow file... [DONE]  ')

    if not exists(BASE_FLOW_FILE_PATH):
        process()
    else:
        if PROMPT_FLOW_FILE_CREATION:
            overwrite = input('Do you want to want overwrite the existing BASE_FLOW_FILE? [Y/n]')
            if overwrite.lower() == 'y' or not overwrite:
                process()
            else:
                return False


ORDER_OF_BUILD = ['type', 'edge', 'tlLogic', 'junction', 'connection', 'roundabout']

def build_file(environment:Environment, components:dict, save_file_path:str):
    """
     Constructs .NET.XML file based on the provided environment and components.
    """
    with open(save_file_path, 'w+') as f:
        f.write('<?xml {}?>\n\n'.format(environment.get_xml_xml_line_attribs()))
        f.write('<net {}>\n\n'.format(environment.get_net_xml_line_attribs()))
        f.write('    <location {}/>\n\n'.format(environment.get_location_xml_line_attribs()))
        for key in ORDER_OF_BUILD:
            for component in components[key].values():
                f.write(component.get_xml_line())
            f.write('\n')
        # for key, value in components.items():
        #     for _, component in value.items():
        #         f.write(component.get_xml_line())
        f.write('\n</net>')
