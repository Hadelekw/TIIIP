"""
 File containing functions regarding components in components.py.
 These functions are meant to be used on the entire collection of
 components in net_xml_parser functions to, for instance, connect
 components with one another directly.
"""

from .components import *


def connect_edges_and_junctions(components:dict):
    """
     Sets values of special attributes _to and _from in junctions and edges.
     This allows for quick analysis of connections in the net.
    """
    for edge_id, edge in components['edge'].items():
        for junction_id, junction in components['junction'].items():
            if hasattr(edge, 'from'):
                if getattr(edge, 'from') == junction_id:
                    junction._from.append(edge)
                    edge._from = junction
            if hasattr(edge, 'to'):
                if getattr(edge, 'to') == junction_id:
                    junction._to.append(edge)
                    edge._to = junction


def find_and_set_outside_connections(components:dict):
    """
     An outside connection is such an edge that has unique to or from value.
     By default every edge has the _outside_connection value set to False.
    """
    for junction_id, junction in components['junction'].items():
        if len(junction._to) == 1 and not junction._from:
            junction._to[0]._outsice_connection = True
            junction._to[0]._outside_connection_type = OutsideConnectionType('out')
        if len(junction._from) == 1 and not junction._to:
            junction._from[0]._outside_connection = True
            junction._from[0]._outside_connection_type = OutsideConnectionType('in')
        if len(junction._to) == 1 and len(junction._from) == 1:
            if junction._to[0]._to == junction._from[0]._from or \
               junction._from[0]._from == '-' + junction._to[0]._to:
                junction._to[0]._outsice_connection = True
                junction._to[0]._outside_connection_type = OutsideConnectionType('out')
                junction._from[0]._outside_connection = True
                junction._from[0]._outside_connection_type = OutsideConnectionType('in')
