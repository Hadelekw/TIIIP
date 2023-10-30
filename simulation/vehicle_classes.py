
from enum import Enum


class VehicleClass(Enum):
    IGNORING = 'ignoring'
    PRIVATE = 'private'
    EMERGENCY = 'emergency'
    AUTHORITY = 'authority'
    ARMY = 'army'
    VIP = 'vip'
    PEDESTRIAN = 'pedestrian'
    PASSENGER = 'passenger'
    HOV = 'hov'
    TAXI = 'taxi'
    BUS = 'bus'
    COACH = 'coach'
    DELIVERY = 'delivery'
    TRUCK = 'truck'
    TRAILER = 'trailer'
    MOTORCYCLE = 'motorcycle'
    MOPED = 'moped'
    BICYCLE = 'bicycle'
    EVEHICLE = 'evehicle'
    TRAM = 'tram'
    RAIL_URBAN = 'rail_urban'
    RAIL = 'rail'
    RAIL_ELECTRIC = 'rail_electric'
    RAIL_FAST = 'rail_fast'
    SHIP = 'ship'


class EmissionClass(Enum):
    PC_G_EU4 = 'PC_G_EU4'
    HBEFAV2_1_BASED = 'HBEFA v2.1-based'
    HBEFAV3_1_BASED = 'HBEFA v3.1-based'
    HBEFAV4_2_BASED = 'HBEFA v4.2-based'
    PHEMLIGHT = 'PHEMlight'
    PHEMLIGHT5 = 'PHEMlight5'
    ELECTRIC_VEHICLE_MODEL = 'Energy'
    ZERO = 'Zero'


class GuiShape(Enum):
    PEDESTRIAN = 'pedestrian'
    BICYCLE = 'bicycle'
    MOPED = 'moped'
    MOTORCYCLE = 'motorcycle'
    PASSENGER = 'passenger'
    PASSENGER_SEDAN = 'passenger/sedan'
    PASSENGER_HATCHBACK = 'passenger/hatchback'
    PASSENGER_WAGON = 'passenger/wagon'
    PASSENGER_VAN = 'passenger/van'
    TAXI = 'taxi'
    DELIVERY = 'delivery'
    TRUCK = 'truck'
    TRUCK_SEMITRAILER = 'truck/semitrailer'
    TRUCK_TRAILER = 'truck/trailer'
    BUS = 'bus'
    BUS_COACH = 'bus/coach'
    BUS_FLEXIBLE = 'bus/flexible'
    BUS_TROLLEY = 'bus/trolley'
    RAIL = 'rail'
    RAIL_RAILCAR = 'rail/railcar'
    RAIL_CARGO = 'rail/cargo'
    EVEHICLE = 'evehicle'
    ANT = 'ant'
    SHIP = 'ship'
    EMERGENCY = 'emergency'
    FIREBRIGADE = 'firebrigade'
    POLICE = 'police'
    RICKSHAW = 'rickshaw'
    SCOOTER = 'scooter'
    AIRCRAFT = 'aircraft'
    UNKNOWN = 'unknown'


class LaneChangeModel(Enum):
    LC2013 = 'LC2013'


class CarFollowModel(Enum):
    KRAUSS = 'Krauss'
    KRAUSS_ORIG_1 = 'KraussOrig1'
    PWAGNER_2009 = 'PWagner2009'
    BKERNER = 'BKerner'
    IDM = 'IDM'
    IDMM = 'IDMM'
    EIDM = 'EIDM'
    KRAUSSPS = 'KraussPS'
    KRAUSSAB = 'KraussAB'
    SMARTSK = 'SmartSK'
    WIEDEMANN = 'Wiedemann'
    W99 = 'W99'
    DANIEL1 = 'Daniel1'
    ACC = 'ACC'
    CACC = 'CACC'
    RAIL = 'Rail'


class LatAlignment(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    COMPACT = 'compact'
    NICE = 'nice'
    ARBITRARY  ='arbitrary'


DEFAULT_FIELDS = {
    'id': None,
    'accel': 2.6,
    'decel': 4.5,
    'apparentDecel': 4.5,
    'emergencyDecel': 9,
    'startupDelay': 0,
    'sigma': 0.5,
    'tau': 1,
    'length': 5,
    'minGap': 2.5,
    'maxSpeed': 55.55,
    'desiredMaxSpeed': 2778,
    'speedFactor': 1,
    'speedDev': 0.1,
    'color': 'yellow',
    'vClass': VehicleClass('passenger'),
    'emissionClass': EmissionClass('PC_G_EU4'),
    'guiShape': GuiShape('unknown'),
    'width': 1.8,
    'height': 1.5,
    'collisionMinGapFactor': 1,
    'imgFile': None,
    'osgFile': None,
    'laneChangeModel': LaneChangeModel('LC2013'),
    'carFollowModel': CarFollowModel('Krauss'),
    'personCapacity': 4,
    'containerCapacity': 0,
    'boardingDuration': 0.5,
    'loadingDuration': 90,
    'latAlignment': LatAlignment('center'),
    'maxSpeedLat': 1,
    'actionStepLength': None,
    'scale': 1,
    'timeToTeleport': None,
    'timeToTeleportBidi': None,
    'speedFactorPremature': None,
}


class Vehicle:
    default_attribs = DEFAULT_FIELDS

    def __init__(self, **kwargs):
        self.set_default_attribs()
        if self.validate(kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def validate(self, kwargs):
        for key in kwargs:
            if key not in DEFAULT_FIELDS:
                return False
        return True

    def set_default_attribs(self):
        for key, value in self.default_attribs.items():
            setattr(self, key, value)

    def get_xml_line(self):
        file_string = '    <vType'
        for key, value in self.__dict__.items():
            if isinstance(value, Enum):
                file_string += ' {}=\"{}\"'.format(key, value.value)
                continue
            file_string += ' {}=\"{}\"'.format(key, value)
        file_string += '/>\n'
        return file_string


class Pedestrian(Vehicle):
    default_attribs = {
        'id': 'pedestrian',
        'vClass': VehicleClass('pedestrian'),
    }


class Bicycle(Vehicle):
    default_attribs = {
        'id': 'bicycle',
        'vClass': VehicleClass('bicycle'),
    }


class Car(Vehicle):
    pass


class Passenger(Car):
    default_attribs = {
        'id': 'passenger',
        'vClass': VehicleClass('passenger'),
    }


class Private(Passenger):
    default_attribs = {
        'id': 'private',
        'vClass': VehicleClass('private'),
    }


class Bus(Car):
    default_attribs = {
        'id': 'bus',
        'vClass': VehicleClass('bus'),
    }


VEHICLE_CLASSES = {
    # 'pedestrian': Pedestrian,
    # 'bicycle': Bicycle,
    'passenger': Passenger,
    # 'private': Private,
    # 'bus': Bus,
}
