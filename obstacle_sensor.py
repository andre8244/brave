import random
import pygame
import geometry

from sensor import Sensor
from obstacle import Obstacle
from math import sin, cos
from color import Color
from point import Point


class ObstacleSensor(Sensor):

    def __init__(self, robot, delta_direction, max_distance, error, scene):
        super().__init__(robot, delta_direction, max_distance, error, scene)
        self.max_distance = max_distance

    def get_value(self):
        # x_robot = self.robot.x
        # y_robot = -self.robot.y
        dir_sensor = self.robot.direction + self.delta_direction
        x_sensor_eol = self.robot.x + self.max_distance * cos(dir_sensor)
        y_sensor_eol = self.robot.y + self.max_distance * -sin(dir_sensor)

        point_robot = Point(self.robot.x, self.robot.y)
        point_sensor_eol = Point(x_sensor_eol, y_sensor_eol)

        sensor_ray = (point_robot, point_sensor_eol)
        print("sensor_ray:", geometry.segment_to_string(sensor_ray))
        distance_from_nearer_obstacle = None

        for obj in self.scene.objects:
            if issubclass(type(obj), Obstacle):
                obstacle = obj

                # cambio SDR
                # x_obstacle = obstacle.x
                # y_obstacle = -obstacle.y
                #
                # x_obstacle -= x_robot
                # y_obstacle -= y_robot

                # check collision between obstacle edges and sensor ray
                for obstacle_edge in obstacle.edges:
                    print("obstacle_edge:", geometry.segment_to_string(obstacle_edge))
                    intersection_point = geometry.segments_intersection(sensor_ray, obstacle_edge)

                    if intersection_point is not None:
                        print("intersection_point:", geometry.point_to_string(intersection_point))
                        distance_from_obstacle = geometry.distance(point_robot, intersection_point)

                        if distance_from_nearer_obstacle is None or distance_from_obstacle < distance_from_nearer_obstacle:
                            distance_from_nearer_obstacle = distance_from_obstacle
                            print("new distance_from_nearer_obstacle:", distance_from_nearer_obstacle)

        if distance_from_nearer_obstacle is None:
            print("@ NO OBSTACLE DETECTED")
            return 1 / self.max_distance
        else:

            print("@ OBSTACLE DETECTED:", distance_from_nearer_obstacle)

            # percentage standard deviation
            percentage_std_dev = self.error * distance_from_nearer_obstacle
            distance_with_error = random.gauss(distance_from_nearer_obstacle, percentage_std_dev)

            print("@ distance with error:", distance_with_error, "returning proximity:", str(1 / distance_with_error))

            return 1 / distance_with_error

    def draw(self):
        dir_sensor = self.robot.direction + self.delta_direction
        x_sensor_eol = self.robot.x + self.max_distance * cos(dir_sensor)
        y_sensor_eol = self.robot.y + self.max_distance * -sin(dir_sensor)

        pygame.draw.line(self.scene.screen, Color.RED, (self.robot.x, self.robot.y), (x_sensor_eol, y_sensor_eol))
