"""
 File containing functions for available changes in the network.
 Because the extend of possible changes is very large and can
 break stuff easily.
"""

import random

from .components import *


POSSIBLE_SIGNAL_STATES = {
    'G': ['G', 'g', 'r'],
    'g': ['r'],
    'r': ['G', 'r'],
}

# Example function
def name_edge(edges:dict, edge_id:str, new_name:str):
    edges[edge_id].name = new_name


def generate_tl_program(tllogic):
    for phase in tllogic._phases:
        temp_state = phase.state
        for i in range(len(phase.state)):
            if i:
                phase.state[i] = SignalState(random.choice(POSSIBLE_SIGNAL_STATES[phase.state[i - 1].value]))
            else:
                phase.state[i] = SignalState(random.choice(['G', 'r']))
