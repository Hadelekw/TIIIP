

all_vehicle_classes = {
    'pedestrian',
    'bicycle',
    'passenger',
    'private',
    'bus'
}


class Vehicle:
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
