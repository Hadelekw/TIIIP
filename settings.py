

# Road file used as the base for simulation.
# Must be in SUMO's .NET.XML format.
BASE_ROAD_FILE_PATH = 'road_file.net.xml'

# Directory for storage of road files generated during the process.
GENERATIONS_ROAD_FILE_DIRECTORY = 'generations/'


# Base modes of transport weights (valuability).
# If a mode of transport isn't on this list, it is not supported.
# (Current values are arbitrary and a subject to change)
PEDESTRAIN_WEIGHT = 1
BICYCLE_WEIGHT = 1
CAR_WEIGHT = 1
TRUCK_WEIGHT = 3
BUS_WEIGHT = 5
