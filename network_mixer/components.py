"""
 File containing classes based on SUMO's .NET.XML files' tags.
 All necessary documentation is included in the official docs of SUMO:
 https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#internal_junctions
"""

import sys
sys.path.append('../')

from enum import Enum

import simulation


class Environment:
    """
     Class containing all the information about .NET.XML file's details about simulation environment.
    """
    xml_data = {}
    net_data = {}
    location_data = {}

    def load_xml_data(self, xml_string:str):
        xml_string = xml_string.split('\"')
        self.xml_data = {
            'version': xml_string[1],
            'encoding': xml_string[3]
        }

    def load_net_data(self, net_string:str):
        net_string = net_string.split('\"')
        self.net_data = {
            'version': net_string[1],
            'junctionCornerDetail': net_string[3],
            'limitTurnSpeed': net_string[5],
            'xmlns:xsi': net_string[7],
            'xsi:noNamespaceSchemaLocation': net_string[9],
        }

    def load_location_data(self, location_dict:dict):
        self.location_data = location_dict

    def get_xml_xml_line_attribs(self):
        result = ''
        for key, value in self.xml_data.items():
            result += '{}=\"{}\" '.format(key, value)
        return result

    def get_net_xml_line_attribs(self):
        result = ''
        for key, value in self.net_data.items():
            result += '{}=\"{}\" '.format(key, value)
        return result

    def get_location_xml_line_attribs(self):
        result = ''
        for key, value in self.location_data.items():
            result += '{}=\"{}\" '.format(key, value)
        return result


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
    TRAFFIC_LIGHT = 'traffic_light'


class OutsideConnectionType(Enum):
    IN = 'in'
    OUT = 'out'


class TLLogicType(Enum):
    STATIC = 'static'
    ACTUATED = 'actuated'
    DELAY_BASED = 'delay_based'


class SignalState(Enum):
    RED = 'r'
    YELLOW = 'y'
    GREEN_NO_PRIORITY = 'g'
    GREEN_PRIORITY = 'G'
    GREEN_RIGHT_TURN_ARROW = 's'
    RED_YELLOW = 'u'
    OFF_BLINKING = 'o'
    OFF = 'O'


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

    @property
    def level(self):
        if hasattr(self, 'get_level'):
            return self.get_level()
        return 0

    @property
    def name(self):
        if hasattr(self, 'get_name'):
            return self.get_name()
        return self.__class__.__name__.lower()

    def clean(self):
        for key, value in self.__dict__.items():
            try:
                setattr(self, key, self.schema[key](value))
            except KeyError:
                pass

    # A function for building .NET.XML files from Components
    # Currently tested on just one case
    def get_xml_line(self):
        file_string = '{}<{} '.format('    ' * self.level, self.name)
        end_string = '/>\n'
        for key, value in self.__dict__.items():        
            if key[0] == '_':
                if key == '_lanes' and value:
                    end_string = '>\n'
                    for lane in self._lanes:
                        end_string += lane.get_xml_line()
                    end_string += '{}</edge>\n'.format('    ' * self.level)
                if key == '_requests' and value:
                    end_string = '>\n'
                    for request in self._requests:
                        end_string += request.get_xml_line()
                    end_string += '{}</junction>\n'.format('    ' * self.level)
                if key == '_phases' and value:
                    end_string = '>\n'
                    for phase in self._phases:
                        end_string += phase.get_xml_line()
                    end_string += '{}</tlLogic>\n'.format('    ' * self.level)
                continue
            formatted_value = value

            if isinstance(value, Enum):
                formatted_value = value.value

            elif isinstance(value, Type):
                formatted_value = value.id

            elif isinstance(value, bool):
                formatted_value = {True: '1', False: '0'}[value]

            elif isinstance(value, list):
                value_list = value
                spaced = True
                if not value:
                    continue
                if value_list:
                    if isinstance(value_list[0], str):
                        pass
                    elif isinstance(value_list[0], tuple):
                        if isinstance(value_list[0][0], float):
                            value_list = ['{},{}'.format(pair[0], pair[1]) for pair in value]
                    elif isinstance(value_list[0], SignalState):
                        value_list = [v.value for v in value_list]
                        spaced = False
                    elif type(value_list[0]) is not type:
                        continue
                    elif issubclass(value_list[0], simulation.Vehicle):
                        value_list = [v.__name__.lower() for v in value]
                if spaced:
                    formatted_value = ' '.join(value_list)
                else:
                    formatted_value = ''.join(value_list)

            file_string += '{}=\"{}\" '.format(key, formatted_value)
        return file_string + end_string

    # Functions for specific yet common schema purposes
    def get_fixed_bool(self, bool_string:str):
        return False if bool_string == '0' else True

    def get_id_list(self, initial_string:str):
        return initial_string.split(' ')

    def get_shape_list(self, initial_string:str):
        result = []
        split_pairs = initial_string.split()
        for pair in split_pairs:
            latlon = tuple([float(coord) for coord in pair.split(',')])
            result.append(latlon)
        return result

    def get_vehicle_classes(self, allow_string:str):
        result = []
        allow_list = allow_string.split()
        for vehicle_id in allow_list:
            # if hasattr(simulation, vehicle_id.title()):
            #     result.append(getattr(simulation, vehicle_id.title()))
            if vehicle_id in simulation.VEHICLE_CLASSES:
                result.append(simulation.VEHICLE_CLASSES[vehicle_id])
        return result

    def get_type_class(self, type_id:str):
        return list(filter(lambda type_: type_.id == type_id, self.types))[0]


class Type(Component):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'allow'):
            self.allow = []
        self.allowed_vehicles_fix()

    def get_level(self):
        return 1

    def get_schema(self):
        schema = {
            'id': str,
            'priority': int,
            'numLanes': int,
            'speed': float,
            'oneway': self.get_fixed_bool,
            'width': float,
            'allow': self.get_vehicle_classes,
            'disallow': self.get_vehicle_classes,
        }
        return schema

    def allowed_vehicles_fix(self):
        if hasattr(self, 'disallow') and self.allow == []:
            for vehicle_class_name, vehicle_class in simulation.VEHICLE_CLASSES:
                if vehicle_class_name not in self.disallow:
                    self.allow.append(vehicle_class)


class Edge(Component):
    """
     Edge taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#edge_descriptions.
     This class is used for quick analysis of edges, finding outside connections,
     applying mutations and generally manipulating possible edges.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lanes = []
        self._outside_connection = False
        self._outside_connection_type = None
        self._from = None
        self._to = None

    def get_level(self):
        return 1

    def get_schema(self):
        schema = {
            'id': str,
            'from': str,  # TODO
            'to': str,  # TODO
            'type': self.get_type_class,
            'function': str,
            'numLanes': int,
            'speed': float,
            'priority': int,
            'length': float,
            'shape': self.get_shape_list,
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

    def get_level(self):
        return 2

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
            'shape': self.get_shape_list,
            'type': self.get_type_class,
            'acceleration': self.get_fixed_bool,
        }
        return schema


class Junction(Component):
    """
     Junctions taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#junctions_and_right-of-way
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._requests = []
        self._from = []
        self._to = []

    def get_level(self):
        return 1

    def get_schema(self):
        schema = {
            'id': str,
            'type': JunctionType,
            'x': float,
            'y': float,
            'z': float,
            'incLanes': self.get_id_list,
            'intLanes': self.get_id_list,
            'shape': self.get_shape_list,
        }
        return schema


class Request(Component):

    def get_level(self):
        return 2

    def get_schema(self):
        schema = {
            'index': int,
            'response': str,
            'foes': str,
            'cont': self.get_fixed_bool,
        }
        return schema


class Connection(Component):
    """
     Connection taken from the official SUMO docs: https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#connections
    """

    def get_level(self):
        return 1

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
    """
     Roundabout taken from the offical SUMO docs: https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html#roundabouts
    """

    def get_level(self):
        return 1

    def get_schema(self):
        schema = {
            'nodes': self.get_id_list,
            'edges': self.get_id_list,
        }
        return schema


class TLLogic(Component):
    """
     Traffic Lights Logic taken from the official SUMO docs: https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#tllogic_attributes
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._phases = []

    def get_level(self):
        return 1

    def get_schema(self):
        schema = {
            'id': str,
            'type': TLLogicType,
            'programID': str,
            'offset': int,
        }
        return schema

    def get_name(self):
        return 'tlLogic'


class Phase(Component):
    """
     Phase for Traffic Lights taken from the offical SUMO docs: https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#phase_attributes
    """

    def get_level(self):
        return 2

    def get_schema(self):
        schema = {
            'duration': int,
            'state': self.get_signal_states,
            'minDur': int,
            'maxDur': int,
            'name': str,
        }
        return schema

    def get_signal_states(self, signal_states):
        result = []
        for signal_state in signal_states:
            result.append(SignalState(signal_state))
        return result


COMPONENTS = {
    'type': Type,
    'edge': Edge,
    'lane': Lane,
    'junction': Junction,
    'request': Request,
    'connection': Connection,
    'roundabout': Roundabout,
    'tlLogic': TLLogic,
    'phase': Phase,
}
