"""
 File containing the functions for visualising the score based on logs.
"""


import matplotlib.pyplot as plt


def get_data_from_log_file(log_file_path=''):
    result = {}
    with open(log_file_path, 'r') as f:
        for line in f:
            split_line = line.split(' ')
            item = {}
            for key, value in zip(split_line[::2], split_line[1::2]):
                item[key] = value
            result[item['GEN'] + '/' + item['N']] = item
    return result


def graph_per_generation(log_file_path='', average=True, max_value=True, min_value=False):
    log_data = get_data_from_log_file(log_file_path)
    print(log_data)
