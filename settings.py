

# Road file used as the base for simulation.
# Must be in SUMO's .NET.XML format.
BASE_ROAD_FILE_PATH = 'road_file.net.xml'

# Directory for storage of road files generated during the process.
GENERATIONS_ROAD_FILE_DIRECTORY = 'generations/'
CREATE_NEW_DIRECTORY_FOR_EACH_RUN = True

# File describing the traffic flow for the base road file.
# It uses .JSON format and if non-existent it can be generated
# based on the BASE_ROAD_FILE during parsing.
BASE_FLOW_FILE_PATH = 'flow_file.json'
# The file won't be generated if this is set to false
PROMPT_FLOW_FILE_CREATION = True
VALIDATE_FLOW_DATA = False

# File describing routes and flows of traffic.
# Must be in SUMO's .ROU.XML format.
BASE_ROUTES_FILE_PATH = 'routes_file.rou.xml'

# File collecting the road file and routes file for TraCI.
BASE_SUMO_CONFIG_FILE_PATH = 'sumo_config.sumocfg'

# Generations settings for the genetic algorithm
NUMBER_OF_GENERATIONS = 10
NUMBER_PER_GENERATION = 20

BASE_RESULTS_PATH = 'results'


# Base modes of transport weights (valuability).
# If a mode of transport isn't on this list, it is not supported.
# (Current values are arbitrary and a subject to change)
PEDESTRAIN_WEIGHT = 1
BICYCLE_WEIGHT = 1
CAR_WEIGHT = 1
TRUCK_WEIGHT = 3
BUS_WEIGHT = 5
