
from TIIIP import network_mixer
# from TIIIP.network_mixer.components import *


class Flow:
    def __init__(self, id:str, type:str, begin:int, color:str, fromJunction:network_mixer.components.Junction, toJunction:network_mixer.components.Junction, end:int, vehsPerHour:float):
        self.id = id
        self.begin = begin
        self.color = color
        self.fromJunction = fromJunction
        self.toJunction = toJunction
        self.end = end
        self.vehsPerHour = vehsPerHour

    def get_xml_line(self):
        file_string = '    <flow'
        for key, value in self.__dict__.items():
            if not value:
                continue
            if isinstance(value, network_mixer.components.Junction):
                file_string += ' {}=\"{}\"'.format(key, value.id)
            else:
                file_string += ' {}=\"{}\"'.format(key, value)
        file_string += '/>\n'
        return file_string
