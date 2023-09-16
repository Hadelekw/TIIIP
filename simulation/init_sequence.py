"""
 File containing all the initial procedures for simulation.
 It ensures the proper sequence of events and checks if the
 necessary elements exist. If not, it writes our proper errors.
"""

import sys
sys.path.append('../')

from TIIIP.network_mixer import load_base_file


def init():
    """
     The main procedure.
    """
    environment, components = load_base_file()


def solve_flow_matrix(flow_data:dict):
    """
     Using the data in .JSON flow file this function calculates the
     percentages of vehicles going from one outside connection to another
    """
    pass

def generate_rou_xml(flow_file_path:str):
    """
     Generates a file describing many possible trips of vehicles based
     on data described in .JSON flow file.
    """
    pass
