"""
 File for classes for creation of .ROU.XML file.
"""

import sys
sys.path.append('../')

import network_mixer


class Flow:
    """
     Class describing flow taken from offical SUMO docs: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html#repeated_vehicles_flows
    """

    def __init__(self, id:str, type:str, begin:int, color:str, fromJunction, toJunction, end:int, vehsPerHour:float):
        self.id = id
        self.type = type
        self.begin = begin
        self.color = color
        self.fromJunction = fromJunction
        self.toJunction = toJunction
        self.end = end
        self.vehsPerHour = vehsPerHour

    def get_xml_line(self):
        file_string = '    <flow'
        for key, value in self.__dict__.items():
            if value is None:
                continue
            if isinstance(value, network_mixer.Junction):
                file_string += ' {}=\"{}\"'.format(key, value.id)
            else:
                file_string += ' {}=\"{}\"'.format(key, value)
        file_string += '/>\n'
        return file_string
