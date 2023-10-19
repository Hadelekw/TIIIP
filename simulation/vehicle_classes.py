

all_vehicle_classes = {
    'pedestrian',
    'bicycle',
    'passenger',
    'private',
    'bus'
}


class Vehicle:  # THINK ABOUT THIS ONE
    def __init__(
            self, id:str, accel=2.6, decel=4.5,
            apparentDecel=4.5, emergencyDecel=9.0,
            startupDelay=0, sigma=0.5, tau=1.0,
            length=5.0, minGap=2.5,
            maxSpeed=55.55, desiredMaxSpeed=2778,
            speedFactor=1.0, speedDev=0.1, color='yellow'
    ):
        pass


class Pedestrian(Vehicle):
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
