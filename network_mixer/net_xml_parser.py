"""
 This file contains classes and functions for the analysis of SUMO's .NET.XML files.
 It is based on the assumption of the user using Netconvert to create the base file
 and that the data comes from a .OSM file.
"""

import sys
sys.path.append('../')

import xml.etree.ElementTree as et

from settings import BASE_ROAD_FILE_PATH
from .basic_sumo_xml import *


class Type:
    def __init__(self):
        pass


class Edge:
    """
     Edge taken from official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#edge_descriptions.
     This class is used for quick analysis of edges, finding outside connections,
     applying mutations and generally manipulating possible edges.
    """

    lanes = []
    outside_connection = False

    def __init__(
            self, id:str, from_:str='', to:str='', type=None, function:str='',
            num_lanes:int=1, speed:float=0, priority:int=0,
            length:float=0, shape:list=[], spread_type:SpreadType=SpreadType('center'),
            allow:list=[], disallow:list=[],
            width:float=1, name:str='', end_offset:float=0,
            sidewalk_width:float=0, bike_lane_width:float=0, distance:float=0
    ):
        self.id = id
        self.from_ = from_
        self.to = to
        self.type = type
        self.num_lanes = num_lanes
        self.speed = speed
        self.priority = priority
        self.length = length
        self.shape = shape
        self.spread_type = spread_type
        self.allow = allow
        self.disallow = disallow
        self.width = width
        self.name = name
        self.end_offset = end_offset
        self.siedwalk_width = sidewalk_width
        self.bike_lane_width = bike_lane_width
        self.distance = distance


class Lane:
    """
     Lane taken from official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#lane-specific_definitions.
     This class is used for quick analysis of lane.
    """

    def __init__(
            self, id:str, index:int=0,
            allow:list=[], disallow:list=[],
            change_left:list=[], change_right:list=[],
            speed:float=0, width:float=1, length=0, end_offset:float=0,
            shape:list=[], type=None, acceleration:bool=False
    ):
        self.id = id
        self.index = index
        self.allow = allow
        self.disallow = disallow
        self.change_left = change_left
        self.change_right = change_right
        self.speed = speed
        self.width = width
        self.end_offset = end_offset
        self.shape = shape
        self.type = type
        self.acceleration = acceleration


class Roundabout:
    def __init__(self, nodes:list, edges:list):
        self.nodes = nodes
        self.edges = edges


def change_dict_key_name(d, init_name, end_name):
    try:
        d[end_name] = d.pop(init_name)
    except:
        return None


def load_base_file():
    f = open(BASE_ROAD_FILE_PATH)
    root = et.parse(f).getroot()
    f.close()
    edges = {}
    lanes = {}
    for child in root:
        if child.tag == 'edge':
            edge_dict = child.attrib
            names_to_change = {
                'from_': 'from',
                'num_lanes': 'numLanes',
                'spread_type': 'spreadType',
                'end_offset': 'endOffset',
                'sidewalk_width': 'sidewalkWidth',
                'bike_lane_width': 'bikeLaneWidth',
            }
            for key in names_to_change:
                change_dict_key_name(edge_dict, names_to_change[key], key)
            try:
                edge_dict['spread_type'] = SpreadType(edge_dict['spread_type'])
            except:
                pass
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
    print(edges)
    print(lanes)

def load_file():
    pass
