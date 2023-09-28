"""
 File containing functions regarding components in components.py.
 These functions are meant to be used on the entire collection of
 components in net_xml_parser functions to, for instance, connect
 components with one another directly.
"""

import time

from .components import *


def connect_edges_and_junctions(components:dict):
    """
     Sets values of special attributes _to and _from in junctions and edges.
     This allows for quick analysis of connections in the net.
    """
    n_processed = 0
    for edge_id, edge in components['edge'].items():
        print('Connecting edges and junctions... [{:.2f}%]'.format(n_processed / len(components['edge']) * 100), end='\r')  # Loading message
        for junction_id, junction in components['junction'].items():
            if hasattr(edge, 'from'):
                if getattr(edge, 'from') == junction_id:
                    junction._from.append(edge)
                    edge._from = junction
            if hasattr(edge, 'to'):
                if getattr(edge, 'to') == junction_id:
                    junction._to.append(edge)
                    edge._to = junction
        n_processed += 1


def find_and_set_outside_connections(components:dict):
    """
     An outside connection is such an edge that has unique to or from value.
     By default every edge has the _outside_connection value set to False.
    """
    n_processed = 0
    for junction in components['junction'].values():
        print('Finding outside connections... [{:.2f}%]'.format(n_processed / len(components['junction']) * 100), end='\r')  # Loading message
        if len(junction._to) == 1 and not junction._from:
            junction._to[0]._outside_connection = True
            junction._to[0]._outside_connection_type = OutsideConnectionType('out')
        elif len(junction._from) == 1 and not junction._to:
            junction._from[0]._outside_connection = True
            junction._from[0]._outside_connection_type = OutsideConnectionType('in')
        elif len(junction._to) == 1 and len(junction._from) == 1:
            if junction._to[0].id == junction._from[0].id[1:] or \
               junction._from[0].id == junction._to[0].id[1:]:
                junction._to[0]._outside_connection = True
                junction._to[0]._outside_connection_type = OutsideConnectionType('out')
                junction._from[0]._outside_connection = True
                junction._from[0]._outside_connection_type = OutsideConnectionType('in')
        n_processed += 1


def get_branching_edges(edge:Edge, _from=False, _to=True, search_depth=1):
    result = []
    i = 0; levels = {n:[] for n in range(search_depth)}
    while i < search_depth:
        if not i:
            if _from:
                levels[i].extend(edge._from._to)
            if _to:
                levels[i].extend(edge._to._from)
        else:
            for edge_ in levels[i - 1]:
                if _from:
                    levels[i].extend(edge_._from._to)
                if _to:
                    levels[i].extend(edge_._to._from)
        for edge_ in levels[i]:
            if edge_ not in result:
                result.append(edge_)
        i += 1
    return result


def find_if_path_between_edges_exists(start_edge:Edge, end_edge:Edge, search_depth=10):
    available_path_edges = []
    available_path_edges.extend(get_branching_edges(start_edge, _from=True, search_depth=search_depth))
    if end_edge in available_path_edges:
        return True
    return False
