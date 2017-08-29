import sys
import pygame
import math
import random

from pygame.locals import *
from sensor_driven_robot import SensorDrivenRobot
from color import Color
from scene import Scene
from light import Light
from light_sensor import LightSensor
from actuator import Actuator
from motor_controller import MotorController


# TODO AGGIUNGERE E RIMUOVERE LUCI CASUALMENTE
# TODO CONTROLLO VELOCITA' SIMULAZIONE

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 30
ROBOT_WHEEL_SPEED_DELTA = 3

LIGHT_SENSOR_SATURATION_VALUE = 100

MOTOR_CONTROLLER_COEFFICIENT = 1.5
MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20

SCREEN_MARGIN = ROBOT_SIZE / 2

scene = None
robots = None


def build_robot(x, y, robot_wheel_radius, light_sensor_direction):
    global scene
    global robots

    robot = SensorDrivenRobot(x, y, ROBOT_SIZE, robot_wheel_radius)

    left_light_sensor = LightSensor(robot, light_sensor_direction, LIGHT_SENSOR_SATURATION_VALUE, scene)
    right_light_sensor = LightSensor(robot, -light_sensor_direction, LIGHT_SENSOR_SATURATION_VALUE, scene)
    left_wheel_actuator = Actuator()
    right_wheel_actuator = Actuator()
    left_motor_controller = MotorController(right_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator,
                                            MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
    right_motor_controller = MotorController(left_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator,
                                             MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)

    robot.set_left_motor_controller(left_motor_controller)
    robot.set_right_motor_controller(right_motor_controller)

    robots.append(robot)
    return robot


def add_robot():
    global scene
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    robot = build_robot(x, y, 10, math.pi / 4)
    scene.put(robot)


def remove_robot():
    global scene
    scene.remove(robots.pop(0))


def init_scene():
    global scene
    global robots

    robots = []
    scene = Scene()
    light = Light(600, 200, 16, Color.YELLOW, Color.BLACK, 20)
    light2 = Light(700, 250, 16, Color.YELLOW, Color.BLACK, 20)
    light3 = Light(100, 450, 16, Color.YELLOW, Color.BLACK, 20)
    light4 = Light(60, 100, 16, Color.YELLOW, Color.BLACK, 20)

    build_robot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10, math.pi / 4)
    build_robot(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3, 20, math.pi / 2)

    scene.put(robots)

    scene.put(light)
    scene.put(light2)
    scene.put(light3)
    scene.put(light4)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    init_scene()

    tick = 0

    while True:
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                init_scene()
            elif event.type == KEYDOWN and event.key == K_PLUS:
                add_robot()
            elif event.type == KEYDOWN and event.key == K_MINUS:
                remove_robot()

        # teletrasporto ai margini
        for robot in robots:
            robot.sense_and_act()

            if robot.x < -SCREEN_MARGIN:
                robot.x = SCREEN_WIDTH + SCREEN_MARGIN
            if robot.x > SCREEN_WIDTH + SCREEN_MARGIN:
                robot.x = -SCREEN_MARGIN
            if robot.y < -SCREEN_MARGIN:
                robot.y = SCREEN_HEIGHT + SCREEN_MARGIN
            if robot.y > SCREEN_HEIGHT + SCREEN_MARGIN:
                robot.y = -SCREEN_MARGIN

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

        pygame.display.flip()
        clock.tick(25)

