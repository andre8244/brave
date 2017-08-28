from sensor import Sensor
from light import Light
from math import atan2, sin, cos
class LightSensor(Sensor):

    def __init__(self, robot, delta_direction, saturation_value, scene):
        super().__init__(robot, delta_direction, saturation_value, scene)

    def get_value(self):
        total_value = 0

        for obj in self.scene.objects:
            if issubclass(type(obj), Light):
                # cambio SDR
                x_robot = self.robot.x
                y_robot = -self.robot.y
                x_light = obj.x
                y_light = -obj.y

                x_light -= x_robot
                y_light -= y_robot

                dir_light = atan2(y_light, x_light)
                dir_sensor = self.robot.direction + self.delta_direction
                difference_dir = dir_sensor - dir_light

                angle_sensor_light = atan2(sin(difference_dir), cos(difference_dir))

                # TODO EMITTING POWER AND DISTANCE

                value = cos(angle_sensor_light)
                print('light:', obj, 'value:', value)

                if value > 0:
                    total_value += value

        if total_value > self.saturation_value:
            return self.saturation_value
        else:
            return total_value
