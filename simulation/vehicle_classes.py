
from enum import Enum


class VehicleClass(Enum):
    ignoring = 'ignoring'
    private = 'private'
    emergency = 'emergency'
    authority = 'authority'
    army = 'army'
    vip = 'vip'
    pedestrian = 'pedestrian'
    passenger = 'passenger'
    hov = 'hov'
    taxi = 'taxi'
    bus = 'bus'
    coach = 'coach'
    delivery = 'delivery'
    truck = 'truck'
    trailer = 'trailer'
    motorcycle = 'motorcycle'
    moped = 'moped'
    bicycle = 'bicycle'
    evehicle = 'evehicle'
    tram = 'tram'
    rail_urban = 'rail_urban'
    rail = 'rail'
    rail_electric = 'rail_electric'
    rail_fast = 'rail_fast'
    ship = 'ship'


class EmissionClass(Enum):
    pc_g_eu4 = 'PC_G_EU4'
    hbefav2_1_based = 'HBEFA v2.1-based'
    hbefav3_1_based = 'HBEFA v3.1-based'
    hbefav4_2_based = 'HBEFA v4.2-based'
    phemlight = 'PHEMlight'
    phemlight5 = 'PHEMlight5'
    electric_vehicle_model = 'Energy'
    zero = 'Zero'


class GuiShape(Enum):
    pedestrian = 'pedestrian'
    bicycle = 'bicycle'
    moped = 'moped'
    motorcycle = 'motorcycle'
    passenger = 'passenger'
    passenger_sedan = 'passenger/sedan'
    passenger_hatchback = 'passenger/hatchback'
    passenger_wagon = 'passenger/wagon'
    passenger_van = 'passenger/van'
    taxi = 'taxi'
    delivery = 'delivery'
    truck = 'truck'
    truck_semitrailer = 'truck/semitrailer'
    truck_trailer = 'truck/trailer'
    bus = 'bus'
    bus_coach = 'bus/coach'
    bus_flexible = 'bus/flexible'
    bus_trolley = 'bus/trolley'
    rail = 'rail'
    rail_railcar = 'rail/railcar'
    rail_cargo = 'rail/cargo'
    evehicle = 'evehicle'
    ant = 'ant'
    ship = 'ship'
    emergency = 'emergency'
    firebrigade = 'firebrigade'
    police = 'police'
    rickshaw = 'rickshaw'
    scooter = 'scooter'
    aircraft = 'aircraft'
    unknown = 'unknown'


class LaneChangeModel(Enum):
    lc2013 = 'LC2013'


class CarFollowModel(Enum):
    krauss = 'Krauss'
    krauss_orig_1 = 'KraussOrig1'
    pwagner_2009 = 'PWagner2009'
    bkerner = 'BKerner'
    idm = 'IDM'
    idmm = 'IDMM'
    eidm = 'EIDM'
    kraussps = 'KeaussPS'
    kraussab = 'KraussAB'
    smartsk = 'SmartSK'
    wiedemann = 'Wiedemann'
    w99 = 'W99'
    daniel1 = 'Daniel1'
    acc = 'ACC'
    cacc = 'CACC'
    rail = 'Rail'


class LatAlignment(Enum):
    left = 'left'
    right = 'right'
    center = 'center'
    compact = 'compact'
    nice = 'nice'
    aribtrary  ='arbitrary'


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
        if not kwargs:
            self.set_default_attribs()
            return
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
            if value == self.default_attribs[key]:
                continue
            else:
                file_string += ' {}=\"{}\"'.format(key, value)
        file_string += '/>\n'
        return file_string


class Pedestrian(Vehicle):
    def set_default_attribs(self):
        pass


class Bicycle(Vehicle):
    pass


class Car(Vehicle):
    pass


class Passenger(Car):
    pass


class Private(Passenger):
    pass


class Bus(Car):
    pass


vehicle_classes = {
    'pedestrian': Pedestrian,
    'bicycle': Bicycle,
    'passenger': Passenger,
    'private': Private,
    'bus': Bus,
}
