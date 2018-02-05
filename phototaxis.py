import sys
import pygame
import math
import random

from pygame.locals import *
from robot.sensor_driven_robot import SensorDrivenRobot
from util.color import Color
from scene.scene import Scene
from scene.light import Light
from sensor.light_sensor import LightSensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
ROBOT_SIZE = 30

LIGHT_SENSOR_SATURATION_VALUE = 100
LIGHT_SENSOR_ERROR = 0.1

MOTOR_CONTROLLER_COEFFICIENT = 0.5
MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20

SCREEN_MARGIN = ROBOT_SIZE / 2

SCENE_SPEED_INITIAL = 25

N_ROBOTS = 5
N_LIGHTS = 5

PHOTOTAXIS = True  # toggle between phototaxis and anti-phototaxis

scene = None
robots = None
lights = None


def build_robot(x, y, robot_wheel_radius, light_sensor_direction):
    global scene
    global robots

    robot = SensorDrivenRobot(x, y, ROBOT_SIZE, robot_wheel_radius)

    left_light_sensor = LightSensor(robot, light_sensor_direction, LIGHT_SENSOR_SATURATION_VALUE, LIGHT_SENSOR_ERROR, scene)
    right_light_sensor = LightSensor(robot, -light_sensor_direction, LIGHT_SENSOR_SATURATION_VALUE, LIGHT_SENSOR_ERROR, scene)
    left_wheel_actuator = Actuator()
    right_wheel_actuator = Actuator()

    if PHOTOTAXIS:
        left_motor_controller = MotorController(right_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator,
                                                MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
        right_motor_controller = MotorController(left_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator,
                                                 MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
    else:
        # ANTI-PHOTOTAXIS
        left_motor_controller = MotorController(left_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator,
                                                MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
        right_motor_controller = MotorController(right_light_sensor, MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator,
                                                 MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)

    robot.set_left_motor_controller(left_motor_controller)
    robot.set_right_motor_controller(right_motor_controller)

    robots.append(robot)
    return robot


def build_light(x, y, emitting_power, color_fg, color_bg):
    global lights
    light = Light(x, y, emitting_power, color_fg, color_bg)
    lights.append(light)
    return light


def add_robots(number_to_add=1):
    global scene
    global robots

    for i in range(number_to_add):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        robot = build_robot(x, y, 10, math.pi / 4)
        scene.put(robot)
    print('number of robots:', len(robots))


def remove_robot():
    global scene
    global robots

    if len(robots) > 0:
        scene.remove(robots.pop(0))
    print('number of robots:', len(robots))


def add_lights(number_to_add=1):
    global scene
    global lights

    for i in range(number_to_add):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        emitting_power = random.randint(10, 25)
        light = build_light(x, y, emitting_power, Color.YELLOW, Color.BLACK)
        scene.put(light)
    print('number of lights:', len(lights))


def remove_light():
    global scene
    global lights

    if len(lights) > 0:
        scene.remove(lights.pop(0))
    print('number of lights:', len(lights))


def init_scene(screen):
    global scene
    global robots
    global lights

    robots = []
    lights = []
    scene = Scene(SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_SPEED_INITIAL, screen)

    add_robots(N_ROBOTS)
    add_lights(N_LIGHTS)

    # build_light(600, 200, 20, Color.YELLOW, Color.BLACK)
    # build_light(700, 250, 10, Color.YELLOW, Color.BLACK)
    # build_light(100, 450, 30, Color.YELLOW, Color.BLACK)
    # build_light(60, 100, 20, Color.YELLOW, Color.BLACK)
    #
    # build_robot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10, math.pi / 4)
    # build_robot(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3, 20, math.pi / 2)


def increase_scene_speed():
    if scene.speed < 200:
        scene.speed *= 1.5
    print('scene.speed:', scene.speed)


def decrease_scene_speed():
    if scene.speed > 1:
        scene.speed /= 1.5
    print('scene.speed:', scene.speed)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Phototaxis - BRAVE")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    init_scene(screen)

    # tick = 0

    while True:
        # keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                init_scene(screen)
            elif event.type == KEYDOWN and event.key == K_k:
                add_robots()
            elif event.type == KEYDOWN and event.key == K_l:
                remove_robot()
            elif event.type == KEYDOWN and event.key == K_COMMA:
                add_lights()
            elif event.type == KEYDOWN and event.key == K_PERIOD:
                remove_light()
            elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93 or event.key == 270):
                increase_scene_speed()
            elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47 or event.key == 269):
                decrease_scene_speed()

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
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)

