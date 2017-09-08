from sensor import Sensor
from box import Box
from math import atan2, sin, cos


class DistanceSensor(Sensor):

    def __init__(self, robot, max_distance, delta_direction, saturation_value, scene):
        super().__init__(robot, delta_direction, saturation_value, scene)
        self.max_distance = max_distance

    def get_value(self):

        for obj in self.scene.objects:
            if issubclass(type(obj), Box):
                box = obj
                # TODO CHECK IF SENSOR DIRECTION INTERSECTS THE OBJECT, COLLECT ALL THESE OBJECTS AND FIND THE NEAREST