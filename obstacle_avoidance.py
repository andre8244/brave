import sys
import pygame
import math
import random

from pygame.locals import *
from robot.sensor_driven_robot import SensorDrivenRobot
from util.color import Color
from scene.scene import Scene
from scene.box import Box
from scene.wall import Wall
from sensor.proximity_sensor import ProximitySensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController
from geometry.point import Point
from util.side_panel import SidePanel

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
STATISTICS_PANEL_WIDTH = 400

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
N_INITIAL_BOXES = 0
N_INITIAL_WALLS = 0

BOX_SIZE = 40
BOX_SIZE_MIN = 20
BOX_SIZE_INTERVAL = 60

scene = None
screen = None
robots = None
obstacles = None
side_panel = None


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
    global obstacles

    box = Box(x, y, size, color)
    obstacles.append(box)
    return box


def build_wall(point1, point2, color):
    global obstacles

    wall = Wall(point1, point2, color)
    obstacles.append(wall)
    return wall


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


def create_boxes(number_to_add=1):
    global scene
    global obstacles

    for i in range(number_to_add):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)

        size = random.randint(BOX_SIZE_MIN, BOX_SIZE_INTERVAL)
        box = build_box(x, y, size, Color.random_bright())
        scene.put(box)

    print('number of obstacles:', len(obstacles))


def add_box_at_cursor():
    global scene
    global obstacles

    x, y = pygame.mouse.get_pos()
    box = build_box(x, y, BOX_SIZE, Color.random_bright())
    scene.put(box)


def remove_box_at_cursor():
    global scene
    global obstacles

    x, y = pygame.mouse.get_pos()

    for obstacle in obstacles:
        if issubclass(type(obstacle), Box):
            box = obstacle

            if x <= box.x + (box.size / 2) and x >= box.x - (box.size / 2) and y <= box.y + (
                    box.size / 2) and y >= box.y - (box.size / 2):
                scene.remove(box)
                obstacles.remove(box)
                break


def add_walls(number_to_add=1):
    global scene
    global obstacles

    for i in range(number_to_add):
        x1 = random.randint(0, SCREEN_WIDTH)
        y1 = random.randint(0, SCREEN_HEIGHT)
        point1 = Point(x1, y1)

        x2 = random.randint(0, SCREEN_WIDTH)
        y2 = random.randint(0, SCREEN_HEIGHT)
        point2 = Point(x2, y2)

        wall = build_wall(point1, point2, Color.random_color(127, 127, 127))
        scene.put(wall)

    print('number of obstacles:', len(obstacles))


# def remove_box():
#     global scene
#     global obstacles
#
#     if len(obstacles) > 0:
#         scene.remove(obstacles.pop(0))
#     print('number of obstacles:', len(obstacles))


def initialize():
    global scene
    global robots
    global obstacles
    global screen
    global side_panel

    robots = []
    obstacles = []
    scene = Scene(SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_SPEED_INITIAL, STATISTICS_PANEL_WIDTH)
    screen = scene.screen
    side_panel = SidePanel(scene)
    add_robots(N_ROBOTS)
    create_boxes(N_INITIAL_BOXES)
    add_walls(N_INITIAL_WALLS)

    # wall = Wall(Point(0,0), Point(300, 500), Color.YELLOW)
    # scene.put(wall)

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
    global scene

    if scene.speed < 200:
        scene.speed *= 1.5
    print('scene.speed:', scene.speed)


def decrease_scene_speed():
    global scene

    if scene.speed > 1:
        scene.speed /= 1.5
    print('scene.speed:', scene.speed)


# todo unire parti comuni con phototaxis in un unico file


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Obstacle avoidance - BRAVE")
    initialize()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                initialize()
            elif event.type == KEYDOWN and event.key == K_j:
                add_robots()
            elif event.type == KEYDOWN and event.key == K_k:
                remove_robot()
            # elif event.type == KEYDOWN and event.key == K_COMMA:
            #     add_boxes()
            # elif event.type == KEYDOWN and event.key == K_PERIOD:
            #     remove_box()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                add_box_at_cursor()
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                remove_box_at_cursor()
            elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93 or event.key == 270):
                increase_scene_speed()
            elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47 or event.key == 269):
                decrease_scene_speed()
            elif event.type == KEYDOWN and event.key == K_s:
                scene.save()

        # teleport at the margins
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

        side_panel.display_info('an obstacle')

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
