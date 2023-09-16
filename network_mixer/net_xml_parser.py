"""
 This file contains classes and functions for the analysis of SUMO's .NET.XML files.
 It is based on the assumption of the user using Netconvert to create the base file
 and that the data comes from a .OSM file.
"""

import sys
sys.path.append('../')

import xml.etree.ElementTree as et

from settings import BASE_ROAD_FILE_PATH
from .components import *


def load_base_file():
    """
     Analysis of the base road file in .NET.XML format. It returns provided environment
     (xml data, net data, location data) and components (everything else which is mutable).
    """
    f = open(BASE_ROAD_FILE_PATH, 'r')
    root = et.parse(f).getroot()
    f.close()
    f = open(BASE_ROAD_FILE_PATH, 'r')
    xml_data = f.readline()
    for line in f:
        if line[:4] == '<net':
            net_data = line
    f.close()
    environment = Environment()
    environment.load_xml_data(xml_data)
    environment.load_net_data(net_data)
    components = {tag: {} for tag in ['type', 'edge', 'junction', 'connection', 'roundabout']}

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
            components[child.tag][child.attrib[identifier]] = getattr(TIIIP.network_mixer, child.tag.title())(**child.attrib)
        else:
            components[child.tag][len(components[child.tag])] = getattr(TIIIP.network_mixer, child.tag.title())(**child.attrib)

        for grandchild in child:
            if grandchild.tag == 'lane':
                components[child.tag][child.attrib['id']]._lanes.append(Lane(**grandchild.attrib))
            if grandchild.tag == 'request':
                components[child.tag][child.attrib['id']]._requests.append(Request(**grandchild.attrib))

    find_and_set_outside_connections(components)

    return environment, components


def find_and_set_outside_connections(components:dict):
    """
     An outside connection is such an edge that has unique to or from value.
     By default every edge has the _outside_connection value set to False.
    """
    junctions = {junction.id: [] for junction in components['junction'].values()}
    for edge_id, edge in components['edge'].items():
        if hasattr(edge, 'from'):
            junctions[getattr(edge, 'from')].append(edge_id)
        if hasattr(edge, 'to'):
            junctions[getattr(edge, 'to')].append(edge_id)
    for junction_id, list_of_edges in junctions.items():
        if len(list_of_edges) == 1:
            components['edge'][list_of_edges[0]]._outside_connection = True


def build_file(environment:Environment, components:dict, save_file_path:str):
    """
     Constructs .NET.XML file based on the provided environment and components.
    """
    with open(save_file_path, 'w+') as f:
        f.write('<?xml {}?>\n\n'.format(environment.get_xml_xml_line_attribs()))
        f.write('<net {}>\n\n'.format(environment.get_net_xml_line_attribs()))
        f.write('    <location {}/>\n\n'.format(environment.get_location_xml_line_attribs()))
        for key, value in components.items():
            for _, component in value.items():
                f.write(component.get_xml_line())
            f.write('\n')
        f.write('\n</net>')
