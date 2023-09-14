"""
 File containing functions for available changes in the network.
 Because the extend of possible changes is very large and can
 break stuff easily.
"""


from .components import *

# Example function
def name_edge(edges:dict, edge_id:str, new_name:str):
    edges[edge_id].name = new_name
