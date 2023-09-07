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


def change_dict_key_name(d, init_name, end_name):
    try:
        d[end_name] = d.pop(init_name)
    except:
        return None


def load_base_file():
    f = open(BASE_ROAD_FILE_PATH)
    root = et.parse(f).getroot()
    f.close()
    types = {}
    edges = {}
    lanes = {}
    for child in root:
        if child.tag == 'type':
            type_dict = child.attrib
            names_to_change = {
                'num_lanes': 'numLanes',
            }
            for key in names_to_change:
                change_dict_key_name(type_dict, names_to_change[key], key)
            types[type_dict['id']] = Type(**type_dict)
        if child.tag == 'edge':
            edge_dict = child.attrib
            # print(edge_dict)
            edges[edge_dict['id']] = Edge(**edge_dict)
        for grandchild in child:
            if grandchild.tag == 'lane':
                lane_dict = grandchild.attrib
                names_to_change = {
                    'change_left': 'changeLeft',
                    'change_right': 'changeRight',
                    'end_offset': 'endOffset',
                }
                for key in names_to_change:
                    change_dict_key_name(lane_dict, names_to_change[key], key)
                lanes[lane_dict['id']] = Lane(**lane_dict)
    for edge in edges:
        for key, value in edges[edge].__dict__.items():
            print('{}\t{}\t{}'.format(key, value, type(value)))
    # print(edges)
    # print(lanes)

def load_file():
    pass
