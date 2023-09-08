"""
 File containing classes based on SUMO's .NET.XML files' tags.
 All necessary documentation is included in the official docs of SUMO:
 https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#internal_junctions
"""

from enum import Enum

import TIIIP.simulation.vehicle_classes


class SpreadType(Enum):
    """
     SpreadType taken from official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#spreadtype.
    """
    RIGHT = 'right'
    CENTER = 'center'
    ROAD_CENTER = 'roadCenter'


class ConnectionDirType(Enum):
    STRAIGHT = 's'
    TURN = 't'
    LEFT = 'l'
    RIGHT = 'r'
    PARTIALLY_LEFT = 'L'
    PARTIALLY_RIGHT = 'R'
    INVALID = 'invalid'


class ConnectionStateType(Enum):
    DEAD_END = '-'
    EQUAL = '='
    MINOR_LINK = 'm'
    MAJOR_LINK = 'M'

    # For traffic lights only:
    CONTROLLER_OFF = 'O'
    YELLOW_FLASHING = 'o'
    YELLOW_MINOR_LINK = 'y'
    YELLOW_MAJOR_LINK = 'Y'
    RED = 'r'
    GREEN_MINOR = 'g'
    GREEN_MAJOR = 'G'


class JunctionType(Enum):
    DEAD_END = 'dead_end'
    PRIORITY = 'priority'
    RIGHT_BEFORE_LEFT = 'right_before_left'
    INTERNAL = 'internal'


class Component:
    """
     Base class for other component classes.
     Simplifies creation of interactive classes from .NET.XML files.
    """

    types = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if instance.__class__.__name__ == 'Type':
            instance.types.append(instance)
        return instance

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.clean()

    @property
    def schema(self):
        if hasattr(self, 'get_schema'):
            return self.get_schema()
        return {}

    def clean(self):
        for key, value in self.__dict__.items():
            try:
                setattr(self, key, self.schema[key](value))
            except KeyError:
                pass

    def get_vehicle_classes(self, allow_string:str):
        result = []
        allow_list = allow_string.split()
        for vehicle_id in allow_list:
            if hasattr(TIIIP.simulation, vehicle_id.title()):
                result.append(getattr(TIIIP.simulation, vehicle_id.title()))
        return result

    def get_type_class(self, type_id:str):
        return list(filter(lambda type_: type_.id == type_id, self.types))[0]


class Type(Component):

    def get_schema(self):
        schema = {
            'id': str,
            'priority': int,
            'numLanes': int,
            'speed': float,
            'oneway': bool,
            'width': float,
            'allow': self.get_vehicle_classes,
            'disallow': self.get_vehicle_classes,
        }
        return schema


class Edge(Component):
    """
     Edge taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#edge_descriptions.
     This class is used for quick analysis of edges, finding outside connections,
     applying mutations and generally manipulating possible edges.
    """

    lanes = []
    outside_connection = False

    def get_schema(self):
        schema = {
            'id': str,
            'from': str,  # TODO
            'to': str,  # TODO
            'type': self.get_type_class,
            'function': str,  # TODO?
            'numLanes': int,
            'speed': float,
            'priority': int,
            'length': float,
            'shape': list[float],  # TODO
            'spreadType': SpreadType,
            'allow': self.get_vehicle_classes,
            'disallow': self.get_vehicle_classes,
            'width': float,
            'name': str,
            'endOffset': float,
            'sidewalkWidth': float,
            'bikeLaneWidth': float,
            'distance': float,
        }
        return schema


class Lane(Component):
    """
     Lane taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#lane-specific_definitions.
     This class is used for quick analysis of lane.
    """

    def get_schema(self):
        schema = {
            'id': str,
            'index': int,
            'allow': self.get_vehicle_classes,
            'disallow': self.get_vehicle_classes,
            'changeLeft': self.get_vehicle_classes,
            'changeRight': self.get_vehicle_classes,
            'speed': float,
            'width': float,
            'length': float,
            'endOffset': float,
            'shape': list,  # TODO
            'type': self.get_type_class,
            'acceleration': bool,
        }
        return schema


class Junction(Component):
    """
     Junctions taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#junctions_and_right-of-way
    """

    requests = []

    def get_schema(self):
        schema = {
            'id': str,
            'type': JunctionType,
            'x': float,
            'y': float,
            'z': float,
            'incLanes': list,  # TODO
            'intLanes': list,  # TODO
            'shape': list,
        }
        return schema


class Request(Component):

    def get_schema(self):
        schema = {
            'index': int,
            'response': str,
            'foes': str,
            'cont': bool,
        }
        return schema


class Connection(Component):
    """
     Connection taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#connections
    """

    def get_schema(self):
        schema = {
            'from': str,
            'to': str,
            'fromLane': int,
            'toLane': int,
            'via': str,
            'tl': str,  # TEMP -- TRAFFIC LIGHTS
            'linkIndex': int,
            'dir': ConnectionDirType,
            'state': ConnectionStateType,
        }
        return schema


class Roundabout(Component):

    def get_schema(self):
        schema = {
            'nodes': list,  # TODO
            'edges': list,  # TODO
        }
        return schema
