import random
import pygame

from sensor import Sensor
from light import Light
from math import atan2, sin, cos
from color import Color


class LightSensor(Sensor):

    LENGTH_SENSOR_LINE = 100


    def __init__(self, robot, delta_direction, saturation_value, error, scene):
        super().__init__(robot, delta_direction, saturation_value, error, scene)

    def get_value(self):
        dir_sensor = self.robot.direction + self.delta_direction
        total_value = 0

        for obj in self.scene.objects:
            if issubclass(type(obj), Light):
                light = obj

                # cambio SDR
                x_robot = self.robot.x
                y_robot = -self.robot.y
                x_light = light.x
                y_light = -light.y

                x_light -= x_robot
                y_light -= y_robot

                dir_light = atan2(y_light, x_light)
                difference_dir = dir_sensor - dir_light

                angle_sensor_light = atan2(sin(difference_dir), cos(difference_dir))

                # TODO CONSIDER ROBOT-LIGHT DISTANCE?

                value = cos(angle_sensor_light) * light.emitting_power
                # print('light:', light, 'value:', value)

                if value > 0:
                    total_value += value

        if total_value > self.saturation_value:
            return self.saturation_value
        else:
            # percentage standard deviation
            percentage_std_dev = self.error * total_value
            total_value_with_error = random.gauss(total_value, percentage_std_dev)

        return total_value_with_error

    def draw(self):
        dir_sensor = self.robot.direction + self.delta_direction
        x_sensor_eol = self.robot.x + self.LENGTH_SENSOR_LINE * cos(dir_sensor)
        y_sensor_eol = self.robot.y + self.LENGTH_SENSOR_LINE * -sin(dir_sensor)

        pygame.draw.line(self.scene.screen, Color.YELLOW, (self.robot.x, self.robot.y), (x_sensor_eol, y_sensor_eol))
