import sys
import pygame
import math
import random

from pygame.locals import *
from sensor_driven_robot import SensorDrivenRobot
from color import Color
from scene import Scene
from obstacle import Obstacle
from proximity_sensor import ProximitySensor
from actuator import Actuator
from motor_controller import MotorController


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

ROBOT_SIZE = 25
ROBOT_WHEEL_SPEED_DELTA = 3

OBSTACLE_SENSOR_MAX_DISTANCE = 100
OBSTACLE_SENSOR_SATURATION_VALUE = 50
OBSTACLE_SENSOR_ERROR = 0.1

MOTOR_CONTROLLER_COEFFICIENT = 300
MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20

SCREEN_MARGIN = ROBOT_SIZE / 2

SCENE_SPEED_INITIAL = 25

N_ROBOTS = 10
N_BOXES = 10

scene = None
robots = None
boxes = None


def build_robot(x, y, robot_wheel_radius, obstacle_sensor_direction):
    global scene
    global robots

    robot = SensorDrivenRobot(x, y, ROBOT_SIZE, robot_wheel_radius)

    left_obstacle_sensor = ProximitySensor(robot, obstacle_sensor_direction, OBSTACLE_SENSOR_SATURATION_VALUE,
                                           OBSTACLE_SENSOR_ERROR, OBSTACLE_SENSOR_MAX_DISTANCE, scene)
    right_obstacle_sensor = ProximitySensor(robot, -obstacle_sensor_direction, OBSTACLE_SENSOR_SATURATION_VALUE,
                                            OBSTACLE_SENSOR_ERROR, OBSTACLE_SENSOR_MAX_DISTANCE, scene)
    left_wheel_actuator = Actuator()
    right_wheel_actuator = Actuator()
    left_motor_controller = MotorController(left_obstacle_sensor, MOTOR_CONTROLLER_COEFFICIENT, left_wheel_actuator,
                                            MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)
    right_motor_controller = MotorController(right_obstacle_sensor, MOTOR_CONTROLLER_COEFFICIENT, right_wheel_actuator,
                                             MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE)

    robot.set_left_motor_controller(left_motor_controller)
    robot.set_right_motor_controller(right_motor_controller)

    robots.append(robot)
    return robot


def build_box(x, y, size, color):
    global boxes

    box = Obstacle(x, y, size, color)
    boxes.append(box)
    return box


def add_robots(number_to_add=1):
    global scene
    global robots

    for i in range(number_to_add):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        robot = build_robot(x, y, 10, math.pi / 8)
        scene.put(robot)
    print('number of robots:', len(robots))


def remove_robot():
    global scene
    global robots

    if len(robots) > 0:
        scene.remove(robots.pop(0))
    print('number of robots:', len(robots))


def add_boxes(number_to_add=1):
    global scene
    global boxes

    for i in range(number_to_add):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)

        size = random.randint(20, 60)
        box = build_box(x, y, size, Color.random_color(127, 127, 127))
        scene.put(box)

    print('number of boxes:', len(boxes))


def remove_box():
    global scene
    global boxes

    if len(boxes) > 0:
        scene.remove(boxes.pop(0))
    print('number of boxes:', len(boxes))


def init_scene(screen):
    global scene
    global robots
    global boxes

    robots = []
    boxes = []
    scene = Scene(SCENE_SPEED_INITIAL, screen)

    add_robots(N_ROBOTS)
    add_boxes(N_BOXES)

    # build_robot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10, math.pi / 4)
    # build_robot(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3, 20, math.pi / 2)

    # build_robot(400, 300, 10, math.pi / 4)
    # robots[0].direction = 0

    # build_box(550, 280, 100, Color.YELLOW)
    # build_box(450, 220, 60, Color.YELLOW)

    # commentare in caso di robot generati casualmente
    # scene.put(robots)
    # scene.put(boxes)


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
                add_boxes()
            elif event.type == KEYDOWN and event.key == K_PERIOD:
                remove_box()
            elif event.type == KEYDOWN and event.key == K_PLUS:
                increase_scene_speed()
            elif event.type == KEYDOWN and event.key == K_MINUS:
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

            # print("robot rect:", robot.rect)

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
