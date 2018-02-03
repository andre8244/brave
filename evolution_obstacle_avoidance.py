import sys
import pygame
import math
import argparse

from pygame.locals import *

from ga_obstacle_avoidance.statistics import Statistics
from geometry.color import Color
from scene.scene import Scene
from ga_obstacle_avoidance.ga_engine import GaEngine
from robot.sensor_driven_robot import SensorDrivenRobot
from time_util import TimeUtil


DEFAULT_SCENE_PATH = 'saved_scenes/boxes_900.txt'
DEFAULT_SCENE_SPEED = 0  # 0 = maximum fps
SCENE_MAX_SPEED = 3000
STATISTICS_PANEL_WIDTH = 500

population_num = None
scene_speed = None
scene_path = None
elitism_num = None
robot_random_direction = None
scene = None
screen = None
engine = None
statistics = None


def initialize():
    global scene
    global screen
    global engine
    global population_num
    global scene_speed
    global elitism_num
    global scene_path
    global robot_random_direction
    global statistics

    scene, screen = Scene.load_from_file(scene_path, scene_speed, STATISTICS_PANEL_WIDTH)

    # redefine pygame screen in order to display statistics
    # screen_width = scene.width + STATISTICS_PANEL_WIDTH
    # screen_height = scene.height
    # screen = pygame.display.set_mode((screen_width, screen_height))
    # scene.screen = screen

    statistics = Statistics(scene, screen)
    engine = GaEngine(scene, statistics, population_num, elitism_num, robot_random_direction)


def increase_scene_speed():
    global scene

    if scene.speed < SCENE_MAX_SPEED:
        scene.speed *= 1.5
    print('scene.speed:', scene.speed)


def decrease_scene_speed():
    global scene

    if scene.speed == 0:
        scene.speed = SCENE_MAX_SPEED

    if scene.speed > 1:
        scene.speed /= 1.5
    print('scene.speed:', scene.speed)


def parse_cli_arguments():
    global population_num
    global scene_speed
    global elitism_num
    global scene_path
    global robot_random_direction
    global DEFAULT_SCENE_SPEED
    global DEFAULT_SCENE_PATH

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--population', help='Number of vehicles in each generation. Default: ' +
                                      str(GaEngine.DEFAULT_POPULATION_NUM), type=int, metavar='POPULATION_NUM')
    parser.add_argument('-e', '--elite',
                        help='Number of vehicles carried over unaltered to a new generation. Default: ' + str(
                            GaEngine.DEFAULT_ELITISM_NUM), type=int, metavar='ELITISM_NUM')
    parser.add_argument('-r', '--randdir', help='Set an initial random direction to every vehicle', action="store_true")
    parser.add_argument('-s', '--scene', help='Path of the scene file. Default: ' + DEFAULT_SCENE_PATH,
                        metavar='SCENE_FILE')
    parser.add_argument('-f', '--fps',
                        help='Number of frames per second (0 = maximum fps). Default: ' + str(DEFAULT_SCENE_SPEED),
                        type=int, metavar='FPS_NUM')
    args = parser.parse_args()

    elitism_num = GaEngine.DEFAULT_ELITISM_NUM if args.elite is None else args.elite
    population_num = GaEngine.DEFAULT_POPULATION_NUM if args.population is None else args.population
    robot_random_direction = args.randdir
    scene_speed = DEFAULT_SCENE_SPEED if args.fps is None else args.fps
    scene_path = DEFAULT_SCENE_PATH if args.scene is None else args.scene

    # check parameters value
    if elitism_num < 0:
        raise ValueError('Error: elite argument must be >= 0')

    if population_num <= elitism_num:
        raise ValueError(
            'Error: pop argument value (' + str(population_num) + ') must be > elite argument value (' + str(
                elitism_num) + ')')

    if scene_speed < 0:
        raise ValueError('Error: fps argument must be >= 0')


if __name__ == '__main__':
    parse_cli_arguments()
    pygame.init()
    clock = pygame.time.Clock()
    initialize()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                initialize()
            elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93):
                increase_scene_speed()
            elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47):
                decrease_scene_speed()
            # elif event.type == KEYDOWN and event.key == K_s:
            #     scene.save()

        # start_time = TimeUtil.current_time_millis()
        engine.step()
        # end_time = TimeUtil.current_time_millis()
        # step_duration = end_time - start_time
        # print('total step duration', step_duration)

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

            if issubclass(type(obj), SensorDrivenRobot) and obj.label is not None:
                obj.draw_label(screen)

        statistics.show()

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
