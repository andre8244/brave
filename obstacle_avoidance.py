import sys
import pygame
import random
import util.cli_parser

from pygame.locals import *

from ga_obstacle_avoidance.genome import Genome
from robot.sensor_driven_robot import SensorDrivenRobot
from util.color import Color
from scene.scene import Scene
from scene.box import Box
from scene.wall import Wall
from geometry.point import Point
from util.scene_type import SceneType
from util.side_panel import SidePanel


class ObstacleAvoidance:

    N_ROBOTS = 10
    N_INITIAL_BOXES = 0
    N_INITIAL_WALLS = 0

    WHEEL_RADIUS = ROBOT_SIZE = 25
    MOTOR_CONTROLLER_COEFFICIENT = 500
    MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 10
    SENSOR_DELTA_DIRECTION = 0.44
    SENSOR_SATURATION_VALUE = 85
    SENSOR_MAX_DISTANCE = 140
    SENSOR_ERROR = 0.1

    DEFAULT_SCENE_FILE = 'saved_scenes/four_boxes_and_walls_700.txt'
    DEFAULT_SCENE_SPEED = 30
    SCENE_MAX_SPEED = 200
    SCENE_MIN_SPEED = 1
    SCENE_SPEED_CHANGE_COEFF = 1.5
    SAVED_SCENE_FILENAME = 'obstacle_avoidance_scene'

    SCREEN_MARGIN = int(ROBOT_SIZE / 2)
    SIDE_PANEL_WIDTH = 400

    BOX_SIZE = 40
    BOX_SIZE_MIN = 20
    BOX_SIZE_INTERVAL = 60

    N_GENOMES_TO_LOAD_FROM_FILE = 10

    def __init__(self):
        self.scene = None
        self.screen = None
        self.robots = None
        self.obstacles = None
        self.side_panel = None
        self.scene_speed = None
        self.scene_file = None
        self.genome_file = None
        self.load_all_genomes = None

        self.parse_cli_arguments()
        pygame.init()
        pygame.display.set_caption("Obstacle avoidance - BRAVE")
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
                #     add_boxes()
                # elif event.type == KEYDOWN and event.key == K_PERIOD:
                #     remove_box()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.add_box_at_cursor()
                elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                    self.remove_box_at_cursor()
                elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93 or event.key == 270):
                    self.increase_scene_speed()
                elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47 or event.key == 269):
                    self.decrease_scene_speed()
                elif event.type == KEYDOWN and event.key == K_s:
                    self.scene.save(self.SAVED_SCENE_FILENAME)

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

                # Draw object label
                if self.genome_file is not None and issubclass(type(obj), SensorDrivenRobot) \
                        or self.scene_file != self.DEFAULT_SCENE_FILE:
                    obj.draw_label(self.screen)

            # draw a black background for the side panel
            side_panel_bg_rect = pygame.Rect(self.scene.width, 0, self.SIDE_PANEL_WIDTH, self.scene.height)
            pygame.draw.rect(self.screen, Color.BLACK, side_panel_bg_rect)

            self.side_panel.display_info('an obstacle')

            pygame.display.flip()
            int_scene_speed = int(round(self.scene.speed))
            clock.tick(int_scene_speed)

    def build_box(self, x, y, size, color):
        box = Box(x, y, size, color)
        self.obstacles.append(box)
        return box

    def build_wall(self, point1, point2, color):
        wall = Wall(point1, point2, color)
        self.obstacles.append(wall)
        return wall

    def add_robots(self, number_to_add=1):
        genome = Genome(self.WHEEL_RADIUS, self.MOTOR_CONTROLLER_COEFFICIENT, self.MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE,
                        self.SENSOR_DELTA_DIRECTION, self.SENSOR_SATURATION_VALUE, self.SENSOR_MAX_DISTANCE)
        # initial_direction = random.random() * 2 * math.pi
        # delta_direction = 2 * math.pi / number_to_add

        for i in range(number_to_add):
            x = self.scene.width / 2
            y = self.scene.height / 2
            robot = genome.build_obstacle_avoidance_robot(x, y, self.ROBOT_SIZE, self.SENSOR_ERROR, self.scene)
            # robot.direction = initial_direction + i * delta_direction
            self.scene.put(robot)
            self.robots.append(robot)
        print('Number of robots:', len(self.robots))

    def remove_robot(self):
        if len(self.robots) > 0:
            self.scene.remove(self.robots.pop(0))
        print('Number of robots:', len(self.robots))

    def create_boxes(self, number_to_add=1):
        for i in range(number_to_add):
            x = random.randint(0, self.scene.width)
            y = random.randint(0, self.scene.height)

            size = random.randint(self.BOX_SIZE_MIN, self.BOX_SIZE_INTERVAL)
            box = self.build_box(x, y, size, Color.random_bright())
            self.scene.put(box)

    def add_box_at_cursor(self):
        x, y = pygame.mouse.get_pos()
        box = self.build_box(x, y, self.BOX_SIZE, Color.random_bright())
        self.scene.put(box)

    def remove_box_at_cursor(self):
        x, y = pygame.mouse.get_pos()

        for obstacle in self.obstacles:
            if issubclass(type(obstacle), Box):
                box = obstacle

                if x <= box.x + (box.size / 2) and x >= box.x - (box.size / 2) and y <= box.y + (
                        box.size / 2) and y >= box.y - (box.size / 2):
                    self.scene.remove(box)
                    self.obstacles.remove(box)
                    break

    def add_walls(self, number_to_add=1):
        for i in range(number_to_add):
            x1 = random.randint(0, self.scene.width)
            y1 = random.randint(0, self.scene.height)
            point1 = Point(x1, y1)

            x2 = random.randint(0, self.scene.width)
            y2 = random.randint(0, self.scene.height)
            point2 = Point(x2, y2)

            wall = self.build_wall(point1, point2, Color.random_color(127, 127, 127))
            self.scene.put(wall)

    def initialize(self):
        self.robots = []
        self.obstacles = []
        self.init_scene()
        self.screen = self.scene.screen
        self.side_panel = SidePanel(self.scene)

        if self.genome_file is None:
            self.add_robots(self.N_ROBOTS)
        else:
            self.load_genomes_from_file()

        self.create_boxes(self.N_INITIAL_BOXES)
        self.add_walls(self.N_INITIAL_WALLS)

    def init_scene(self):
        self.scene = Scene.load_from_file(self.scene_file, self.scene_speed, self.SIDE_PANEL_WIDTH)

        for obj in self.scene.objects:
            if issubclass(type(obj), Box):
                self.obstacles.append(obj)

    def increase_scene_speed(self):
        if self.scene.speed < self.SCENE_MAX_SPEED:
            self.scene.speed *= self.SCENE_SPEED_CHANGE_COEFF
        print('scene.speed:', self.scene.speed)

    def decrease_scene_speed(self):
        if self.scene.speed > self.SCENE_MIN_SPEED:
            self.scene.speed /= self.SCENE_SPEED_CHANGE_COEFF
        print('scene.speed:', self.scene.speed)

    def parse_cli_arguments(self):
        parser = util.cli_parser.CliParser()
        parser.parse_args(self.DEFAULT_SCENE_FILE, self.DEFAULT_SCENE_SPEED, SceneType.OBSTACLE_AVOIDANCE)

        self.scene_speed = parser.scene_speed
        self.scene_file = parser.scene_file
        self.genome_file = parser.genome_file
        self.load_all_genomes = parser.load_all_genomes

    def load_genomes_from_file(self):
        n_genomes_loaded = 0
        x = self.scene.width / 2
        y = self.scene.height / 2

        with open(self.genome_file) as f:
            line_number = 1

            for line in f:
                # load only the first N_GENOMES_TO_LOAD genomes (genomes file could be very large)
                if not self.load_all_genomes and n_genomes_loaded == self.N_GENOMES_TO_LOAD_FROM_FILE:
                    print('Loaded ' + str(self.N_GENOMES_TO_LOAD_FROM_FILE) +
                          ' genomes. To load all of them, use --load_all_genomes parameter')
                    break

                values = line.split()

                # skip empty lines
                if len(values) == 0:
                    line_number += 1
                    continue

                # skip comments in file
                if values[0][0] == '#':
                    line_number += 1
                    continue

                robot_wheel_radius = float(values[0])
                motor_ctrl_coefficient = float(values[1])
                motor_ctrl_min_actuator_value = float(values[2])
                sensor_delta_direction = float(values[3])
                sensor_saturation_value = float(values[4])
                sensor_max_distance = float(values[5])

                genome = Genome(robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                                sensor_delta_direction, sensor_saturation_value, sensor_max_distance)

                robot = genome.build_obstacle_avoidance_robot(x, y, self.ROBOT_SIZE, self.SENSOR_ERROR,
                                                              self.scene)
                robot.label = line_number
                self.robots.append(robot)
                self.scene.put(robot)
                n_genomes_loaded += 1
                line_number += 1
        f.closed

        print('Number of robots:', len(self.robots))


if __name__ == '__main__':
    ObstacleAvoidance()
