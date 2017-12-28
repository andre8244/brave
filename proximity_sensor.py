import random
import pygame
import geometry

from sensor import Sensor
from obstacle import Obstacle
from math import sin, cos
from color import Color
from point import Point
from collision import Collision


class ProximitySensor(Sensor):

    COLLISION_DISTANCE = 6  # px

    def __init__(self, robot, delta_direction, saturation_value, error, max_distance, scene):
        super().__init__(robot, delta_direction, saturation_value, error, scene)
        self.max_distance = max_distance

    def get_value(self):
        dir_sensor = self.robot.direction + self.delta_direction
        x_sensor_eol = self.robot.x + self.max_distance * cos(dir_sensor)
        y_sensor_eol = self.robot.y + self.max_distance * -sin(dir_sensor)

        point_robot = Point(self.robot.x, self.robot.y)
        point_sensor_eol = Point(x_sensor_eol, y_sensor_eol)

        sensor_ray = (point_robot, point_sensor_eol)
        # print("sensor_ray:", geometry.segment_to_string(sensor_ray))
        distance_from_nearest_obstacle = None
        nearest_obstacle = None

        for obj in self.scene.objects:
            if issubclass(type(obj), Obstacle):
                obstacle = obj

                # check collision between obstacle edges and sensor ray
                for obstacle_edge in obstacle.edges:
                    # print("obstacle_edge:", geometry.segment_to_string(obstacle_edge))
                    intersection_point = geometry.segments_intersection(sensor_ray, obstacle_edge)

                    if intersection_point is not None:
                        # print("intersection_point:", geometry.point_to_string(intersection_point))
                        distance_from_obstacle = geometry.distance(point_robot, intersection_point)

                        if distance_from_nearest_obstacle is None or distance_from_obstacle < distance_from_nearest_obstacle:
                            distance_from_nearest_obstacle = distance_from_obstacle
                            nearest_obstacle = obstacle
                            # print("new distance_from_nearest_obstacle:", distance_from_nearest_obstacle)

        if distance_from_nearest_obstacle is None:
            # no obstacle detected
            return 0
        else:
            # check collision
            if distance_from_nearest_obstacle < self.COLLISION_DISTANCE:
                raise Collision(self.robot, nearest_obstacle)

            # percentage standard deviation
            percentage_std_dev = self.error * distance_from_nearest_obstacle
            distance_with_error = random.gauss(distance_from_nearest_obstacle, percentage_std_dev)
            proximity_value = 1 / distance_with_error

            if proximity_value > self.saturation_value:
                return self.saturation_value
            else:
                return proximity_value

    def draw(self):
        dir_sensor = self.robot.direction + self.delta_direction
        x_sensor_eol = self.robot.x + self.max_distance * cos(dir_sensor)
        y_sensor_eol = self.robot.y + self.max_distance * -sin(dir_sensor)

        pygame.draw.line(self.scene.screen, Color.RED, (self.robot.x, self.robot.y), (x_sensor_eol, y_sensor_eol))
