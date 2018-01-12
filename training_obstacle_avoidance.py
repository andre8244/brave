import sys
import pygame
import math

from pygame.locals import *
from robot.sensor_driven_robot import SensorDrivenRobot
from color import Color
from scene.scene import Scene
from sensor.proximity_sensor import ProximitySensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController


ROBOT_SIZE = 25

OBSTACLE_SENSOR_MAX_DISTANCE = 100
OBSTACLE_SENSOR_SATURATION_VALUE = 50
OBSTACLE_SENSOR_ERROR = 0.1

MOTOR_CONTROLLER_COEFFICIENT = 300
MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20

SCENE_SPEED_INITIAL = 25

N_ROBOTS = 10

scene = None
robots = None
screen = None


def build_robot(x, y, robot_wheel_radius, obstacle_sensor_direction):
    global scene
    global robots

    robot = SensorDrivenRobot(x, y, ROBOT_SIZE, robot_wheel_radius)
    robot.direction = 0

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


def init_scene():
    global scene
    global screen
    global robots

    robots = []
    scene, screen = Scene.load_from_file('saved_scenes/scene_training_obstacle_avoidance.txt', SCENE_SPEED_INITIAL)
    x = scene.width / 2
    y = scene.height / 2
    robot = build_robot(x, y, 10, math.pi / 8)
    scene.put(robot)


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


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    init_scene()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                init_scene()
            elif event.type == KEYDOWN and event.key == K_PLUS:
                increase_scene_speed()
            elif event.type == KEYDOWN and event.key == K_MINUS:
                decrease_scene_speed()
            # elif event.type == KEYDOWN and event.key == K_s:
            #     scene.save()

        for robot in robots:
            robot.sense_and_act()

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
