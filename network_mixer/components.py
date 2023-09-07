"""
 File containing classes based on SUMO's .NET.XML files' tags.
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
     Edge taken from official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#edge_descriptions.
     This class is used for quick analysis of edges, finding outside connections,
     applying mutations and generally manipulating possible edges.
    """

    lanes = []
    outside_connection = False

    def get_schema(self):
        schema = {
            'id': str,
            'from': str,
            'to': str,
            'type': self.get_type_class,
            'function': str,
            'numLanes': int,
            'speed': float,
            'priority': int,
            'length': float,
            'shape': list[float],
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
     Lane taken from official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#lane-specific_definitions.
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
            'shape': list,
            'type': self.get_type_class,
            'acceleration': bool,
        }
        return schema


class Roundabout:
    def __init__(self, nodes:list, edges:list):
        self.nodes = nodes
        self.edges = edges
