
class Vehicle:
    def __init__(self, **kwargs):
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


vehicle_classes = {
    'pedestrian': Pedestrian,
    'bicycle': Bicycle,
    'passenger': Passenger,
    'private': Private,
    'bus': Bus,
}
