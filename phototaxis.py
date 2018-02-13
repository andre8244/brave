import sys
import pygame
import math
import random
import util.cli_parser

from pygame.locals import *
from robot.sensor_driven_robot import SensorDrivenRobot
from util.color import Color
from scene.scene import Scene
from scene.light import Light
from sensor.light_sensor import LightSensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController
from util.side_panel import SidePanel


class Phototaxis:

    N_ROBOTS = 5
    N_INITIAL_LIGHTS = 0

    PHOTOTAXIS = True  # toggle between phototaxis and anti-phototaxis
    LIGHT_EMITTING_POWER = 20

    LIGHT_SENSOR_SATURATION_VALUE = 100
    LIGHT_SENSOR_ERROR = 0.1

    MOTOR_CONTROLLER_COEFFICIENT = 0.5
    MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20

    DEFAULT_SCENE_PATH = 'saved_scenes/empty_scene_700.txt'
    DEFAULT_SCENE_SPEED = 30
    SCENE_MAX_SPEED = 200
    SCENE_MIN_SPEED = 1

    ROBOT_SIZE = 30
    SCREEN_MARGIN = ROBOT_SIZE / 2
    STATISTICS_PANEL_WIDTH = 400

    LIGHT_EMITTING_POWER_MIN = 10
    LIGHT_EMITTING_POWER_INTERVAL = 30

    def __init__(self):
        self.scene = None
        self.screen = None
        self.robots = None
        self.lights = None
        self.side_panel = None
        self.scene_speed = None
        self.scene_path = None

        self.parse_cli_arguments()
        pygame.init()
        pygame.display.set_caption("Phototaxis - BRAVE")
        clock = pygame.time.Clock()
        self.initialize()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_r:
                    self.initialize()
                elif event.type == KEYDOWN and event.key == K_j:
                    self.add_robots()
                elif event.type == KEYDOWN and event.key == K_k:
                    self.remove_robot()
                # elif event.type == KEYDOWN and event.key == K_COMMA:
                #     add_lights()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.add_light_at_cursor()
                # elif event.type == KEYDOWN and event.key == K_PERIOD:
                #     remove_light()
                elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                    self.remove_light_at_cursor()
                elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93 or event.key == 270):
                    self.increase_scene_speed()
                elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47 or event.key == 269):
                    self.decrease_scene_speed()
                elif event.type == KEYDOWN and event.key == K_s:
                    self.scene.save('phototaxis_scene')

            # teleport at the margins
            for robot in self.robots:
                robot.sense_and_act()

                if robot.x < -self.SCREEN_MARGIN:
                    robot.x = self.scene.width + self.SCREEN_MARGIN
                if robot.x > self.scene.width + self.SCREEN_MARGIN:
                    robot.x = -self.SCREEN_MARGIN
                if robot.y < -self.SCREEN_MARGIN:
                    robot.y = self.scene.height + self.SCREEN_MARGIN
                if robot.y > self.scene.height + self.SCREEN_MARGIN:
                    robot.y = -self.SCREEN_MARGIN

            self.screen.fill(Color.BLACK)

            for obj in self.scene.objects:
                obj.draw(self.screen)

            self.side_panel.display_info('a light')

            pygame.display.flip()
            int_scene_speed = int(round(self.scene.speed))
            clock.tick(int_scene_speed)

    def build_robot(self, x, y, robot_wheel_radius, light_sensor_direction):
        robot = SensorDrivenRobot(x, y, self.ROBOT_SIZE, robot_wheel_radius)

        left_light_sensor = LightSensor(robot, light_sensor_direction, self.LIGHT_SENSOR_SATURATION_VALUE, self.LIGHT_SENSOR_ERROR, self.scene)
        right_light_sensor = LightSensor(robot, -light_sensor_direction, self.LIGHT_SENSOR_SATURATION_VALUE, self.LIGHT_SENSOR_ERROR, self.scene)
        left_wheel_actuator = Actuator()
        right_wheel_actuator = Actuator()

        if self.PHOTOTAXIS:
            left_motor_controller = MotorController(right_light_sensor, self.MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator,
                                                    self.MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
            right_motor_controller = MotorController(left_light_sensor, self.MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator,
                                                     self.MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
        else:
            # ANTI-PHOTOTAXIS
            left_motor_controller = MotorController(left_light_sensor, self.MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator,
                                                    self.MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
            right_motor_controller = MotorController(right_light_sensor, self.MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator,
                                                     self.MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)

        robot.set_left_motor_controller(left_motor_controller)
        robot.set_right_motor_controller(right_motor_controller)

        self.robots.append(robot)
        return robot

    def build_light(self, x, y, emitting_power, color_fg, color_bg):
        light = Light(x, y, emitting_power, color_fg, color_bg)
        self.lights.append(light)
        return light

    def add_robots(self, number_to_add=1):
        for i in range(number_to_add):
            x = random.randint(0, self.scene.width)
            y = random.randint(0, self.scene.height)
            robot = self.build_robot(x, y, 10, math.pi / 4)
            self.scene.put(robot)
        # print('number of robots:', len(robots))

    def remove_robot(self):
        if len(self.robots) > 0:
            self.scene.remove(self.robots.pop(0))
        # print('number of robots:', len(robots))

    def create_lights(self, number_to_add=1):
        for i in range(number_to_add):
            x = random.randint(0, self.scene.width)
            y = random.randint(0, self.scene.height)
            emitting_power = random.randint(self.LIGHT_EMITTING_POWER_MIN, self.LIGHT_EMITTING_POWER_INTERVAL)
            light = self.build_light(x, y, emitting_power, Color.YELLOW, Color.BLACK)
            self.scene.put(light)
        # print('number of lights:', len(lights))

    def add_light_at_cursor(self):
        x, y = pygame.mouse.get_pos()
        light = self.build_light(x, y, self.LIGHT_EMITTING_POWER, Color.YELLOW, Color.BLACK)
        self.scene.put(light)
        # print('number of lights:', len(lights))

    def remove_light_at_cursor(self):
        x, y = pygame.mouse.get_pos()

        for light in self.lights:
            if x <= light.x + (light.size / 2) and x >= light.x - (light.size / 2) and y <= light.y + (
                    light.size / 2) and y >= light.y - (light.size / 2):
                self.scene.remove(light)
                self.lights.remove(light)
                break

    def initialize(self):
        self.robots = []
        self.lights = []
        self.scene = Scene.load_from_file(self.scene_path, self.scene_speed, self.STATISTICS_PANEL_WIDTH)
        self.screen = self.scene.screen
        self.side_panel = SidePanel(self.scene)
        self.add_robots(self.N_ROBOTS)
        self.create_lights(self.N_INITIAL_LIGHTS)

    def increase_scene_speed(self):
        if self.scene.speed < self.SCENE_MAX_SPEED:
            self.scene.speed *= 1.5
        print('Scene speed:', self.scene.speed)

    def decrease_scene_speed(self):
        if self.scene.speed > self.SCENE_MIN_SPEED:
            self.scene.speed /= 1.5
        print('Scene speed:', self.scene.speed)

    def parse_cli_arguments(self):
        parser = util.cli_parser.CliParser()
        parser.parse_args(self.DEFAULT_SCENE_PATH, self.DEFAULT_SCENE_SPEED, False)

        self.scene_speed = parser.scene_speed
        self.scene_path = parser.scene_path


if __name__ == '__main__':
    Phototaxis()
