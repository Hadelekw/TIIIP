"""
 File containing functions for available changes in the network.
 Because the extend of possible changes is very large and can
 break stuff easily.
"""

import random

from .components import *


POSSIBLE_SIGNAL_STATES = {
    'G': ['G', 'g'],
    'g': ['y', 'g'],
    'r': ['y', 'r'],
    'y': ['y', 'G', 'g', 'r'],
}


def generate_random_new_phase(length):
    new_phase = Phase(
        **{
            'duration': random.randint(1, 100),
            'state': generate_phase_states(length),
        }
    )
    return new_phase


def generate_phase_states(length):
    states = []
    for i in range(length):
        if i:
            states.append(SignalState(random.choice(POSSIBLE_SIGNAL_STATES[states[i - 1].value])))
        else:
            states.append(SignalState(random.choice(['G', 'r'])))
    return states


def mutate_tl_program(tllogic):
    for _ in range(random.randint(1, 3)):  # random mutation count
        chance = random.random()
        if chance < 0.1:
            tllogic._phases.append(generate_random_new_phase(len(tllogic._phases[0].state)))
        elif 0.1 <= chance < 0.9:
            for phase in tllogic._phases:
                phase.state = generate_phase_states(len(phase.state))
        else:
            if len(tllogic._phases) > 1:
                tllogic._phases.remove(random.choice(tllogic._phases))
    return tllogic


def generate_tllogic(id_, length):
    result = TLLogic(
        **{
            'id': id_,
            'type': TLLogicType('static'),
            'programID': '0',
            'offset': 0,
        }
    )
    phases_number = random.randint(1, 8)
    for _ in range(phases_number):
        result._phases.append(generate_random_new_phase(length))
    return result
