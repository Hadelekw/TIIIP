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
    components = {tag: {} for tag in ['type', 'edge', 'junction', 'connection', 'roundabout']}
    for child in root:
        try:
            # This doesn't include connections and roundabouts
            components[child.tag][child.attrib['id']] = getattr(TIIIP.network_mixer, child.tag.title())(**child.attrib)
        except:
            pass
        # for grandchild in child:
        #     if grandchild.tag == 'lane':
        #         lane_dict = grandchild.attrib
        #         names_to_change = {
        #             'change_left': 'changeLeft',
        #             'change_right': 'changeRight',
        #             'end_offset': 'endOffset',
        #         }
        #         for key in names_to_change:
        #             change_dict_key_name(lane_dict, names_to_change[key], key)
        #         lanes[lane_dict['id']] = Lane(**lane_dict)
    print(components)
    rebuild_file(components, 'test.xml')


def rebuild_file(components:dict, file_path:str):
    with open(file_path, 'w+') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        for key, value in components.items():
            for component in value:
                f.write('    <{} {}'.format(key, component.get_file_string()))
