"""
 File containing functions for available changes in the network.
"""

import random
import copy

from .components import *


# POSSIBLE_SIGNAL_STATES = {
#     'G': {
#         0: ['G', 'g', 's'],  # If there's no collision
#         1: ['r', 'y'],  # If there is collision
#     },
#     'g': {
#         0: ['G', 'g', 's'],
#         1: ['r', 'y'],
#     },
#     'r': {
#         0: ['r', 'y'],
#         1: ['G', 'g', 's'],
#     },
#     'y': {
#         0: ['y', 'G', 'g', 's'],
#         1: ['y', 'r'],
#     },
#     's': {
#         0: ['G', 'g', 'y', 'r'],
#         1: ['r', 'y']
#     },
# }

POSSIBLE_SIGNAL_STATES = ['G', 'r']


def generate_random_new_phase(length, requests):
    new_phase = Phase(
        **{
            'duration': random.randint(1, 100),
            'state': generate_phase_states(length, requests),
        }
    )
    return new_phase


def generate_phase_states(length, requests):
    states = []
    requests = sorted(requests, key=lambda x: x.index)
    for i in range(length):
        if i:
            foes = requests[i].foes[::-1][:i]
            foe_values = []
            for j in range(len(foes)):
                if int(foes[j]):
                    foe_values.append(states[j].value)
            # states.append(SignalState(random.choice(POSSIBLE_SIGNAL_STATES[random.choice(foe_values) if foe_values else random.choice(['G', 'r'])][1 if foe_values else 0])))
            states.append(SignalState(random.choice(POSSIBLE_SIGNAL_STATES)))
        else:
            states.append(SignalState(random.choice(['G', 'r'])))
    return states


def mutate_tl_program(tllogic, requests, min_mutation_count=0, max_mutation_count=3):
    new_tllogic = copy.deepcopy(tllogic)
    for _ in range(random.randint(min_mutation_count, max_mutation_count)):
        chance = random.random()
        if chance < 0.1:
            new_tllogic._phases.append(generate_random_new_phase(len(tllogic._phases[0].state), requests))
        elif 0.1 <= chance < 0.9:
            for phase in new_tllogic._phases:
                phase.state = generate_phase_states(len(phase.state), requests)
        else:
            if len(new_tllogic._phases) > 1:
                new_tllogic._phases.remove(random.choice(new_tllogic._phases))
    return new_tllogic


def generate_tllogic(id_, length, requests):
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
        result._phases.append(generate_random_new_phase(length, requests))
    return result
