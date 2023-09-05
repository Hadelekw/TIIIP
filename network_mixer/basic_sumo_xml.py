"""
 File containing classes based on SUMO's enums, therefore constants
 that are necessary for parsing .NET.XML files.
"""

from enum import Enum


class SpreadType(Enum):
    """
     SpreadType taken from official SUMO docs: https://sumo.dlr.de/docs/Networks/PlainXML.html#spreadtype.
    """
    RIGHT = 'right'
    CENTER = 'center'
    ROAD_CENTER = 'roadCenter'

