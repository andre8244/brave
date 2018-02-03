import sys
import pygame
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
DEFAULT_VERBOSE_VALUE = 0 # 0, 1, 2
SCENE_MAX_SPEED = 3000
STATISTICS_PANEL_WIDTH = 500

scene = None
screen = None
engine = None
statistics = None
population_num = None
scene_speed = None
scene_path = None
elitism_num = None
robot_random_direction = None
multicore = None
obstacle_sensor_error = None
mutation_probability = None
mutation_coefficient = None
selection_ratio = None
verbose = None


def initialize():
    global scene
    global screen
    global engine
    global population_num
    global scene_speed
    global elitism_num
    global scene_path
    global robot_random_direction
    global multicore
    global statistics
    global obstacle_sensor_error
    global mutation_probability
    global mutation_coefficient
    global selection_ratio
    global verbose

    scene, screen = Scene.load_from_file(scene_path, scene_speed, STATISTICS_PANEL_WIDTH)

    statistics = Statistics(scene, screen, population_num)
    engine = GaEngine(scene, statistics, population_num, elitism_num, robot_random_direction, multicore,
                      obstacle_sensor_error, mutation_probability, mutation_coefficient, selection_ratio, verbose)


def increase_scene_speed():
    global scene

    if scene.speed < SCENE_MAX_SPEED:
        scene.speed *= 1.5

    print('Scene speed:', scene.speed)


def decrease_scene_speed():
    global scene

    if scene.speed == 0:
        scene.speed = SCENE_MAX_SPEED

    if scene.speed > 1:
        scene.speed /= 1.5

    print('Scene speed:', scene.speed)


def parse_cli_arguments():
    global DEFAULT_SCENE_SPEED
    global DEFAULT_SCENE_PATH
    global DEFAULT_VERBOSE_VALUE
    global population_num
    global scene_speed
    global elitism_num
    global scene_path
    global robot_random_direction
    global multicore
    global obstacle_sensor_error
    global mutation_probability
    global mutation_coefficient
    global selection_ratio
    global verbose

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', help='Set verbosity. Default: 0', type=int, choices=range(0, 3))

    parser.add_argument('-p', '--population', help='Number of vehicles in each generation. Default: ' +
                                      str(GaEngine.DEFAULT_POPULATION_NUM), type=int, metavar='NUM')

    parser.add_argument('-e', '--elite',
                        help='Number of vehicles carried over unaltered to a new generation. Default: ' + str(
                            GaEngine.DEFAULT_ELITISM_NUM), type=int, metavar='NUM')

    parser.add_argument('-m', '--mutation_prob',
                        help='Probability that a mutation occurs on a single gene. Default: ' + str(
                            GaEngine.DEFAULT_MUTATION_PROBABILITY), type=float, metavar='NUM')

    parser.add_argument('-M', '--mutation_coeff',
                        help='Coefficient used to alter a gene value during mutation. Default: ' + str(
                            GaEngine.DEFAULT_MUTATION_COEFFICIENT), type=float, metavar='NUM')

    parser.add_argument('-s', '--selection_ratio',
                        help='Ratio of parents selected to breed a new generation. Default: ' + str(
                            GaEngine.DEFAULT_SELECTION_RATIO), type=float, metavar='NUM')

    parser.add_argument('-S', '--scene', help='Path of the scene file. Default: ' + DEFAULT_SCENE_PATH,
                        metavar='FILE')

    parser.add_argument('-f', '--fps',
                        help='Number of frames per second (0 = maximum fps). Default: ' + str(DEFAULT_SCENE_SPEED),
                        type=int, metavar='NUM')

    parser.add_argument('-r', '--random_direction', help='Set an initial random direction for the vehicles',
                        action="store_true")

    parser.add_argument('-E', '--sensor_error',
                        help='Coefficient used to simulate the obstacle sensor read error. Default: ' + str(
                            GaEngine.DEFAULT_OBSTACLE_SENSOR_ERROR) + ', recommended: < 0.2', type=float, metavar='NUM')

    parser.add_argument('-c', '--multicore', help='Enable multicore support (experimental)', action="store_true")

    args = parser.parse_args()

    elitism_num = GaEngine.DEFAULT_ELITISM_NUM if args.elite is None else args.elite
    population_num = GaEngine.DEFAULT_POPULATION_NUM if args.population is None else args.population
    mutation_probability = GaEngine.DEFAULT_MUTATION_PROBABILITY if args.mutation_prob is None else args.mutation_prob
    mutation_coefficient = GaEngine.DEFAULT_MUTATION_COEFFICIENT if args.mutation_coeff is None else args.mutation_coeff
    robot_random_direction = args.random_direction
    scene_speed = DEFAULT_SCENE_SPEED if args.fps is None else args.fps
    scene_path = DEFAULT_SCENE_PATH if args.scene is None else args.scene
    obstacle_sensor_error = GaEngine.DEFAULT_OBSTACLE_SENSOR_ERROR if args.sensor_error is None else args.sensor_error
    selection_ratio = GaEngine.DEFAULT_SELECTION_RATIO if args.selection_ratio is None else args.selection_ratio
    multicore = args.multicore
    verbose = DEFAULT_VERBOSE_VALUE if args.verbose is None else args.verbose

    # check parameters value
    if elitism_num < 0:
        raise ValueError('Elite argument must be >= 0')

    if population_num < 2:
        raise ValueError('Population argument must be >= 2')

    if population_num <= elitism_num:
        raise ValueError('Population argument (' + str(population_num) + ') must be > elite argument (' +
                         str(elitism_num) + ')')

    if scene_speed < 0:
        raise ValueError('FPS argument must be >= 0')

    if obstacle_sensor_error < 0:
        raise ValueError('Sensor error argument must be >= 0')

    if mutation_probability < 0 or mutation_probability > 1:
        raise ValueError('Mutation probability must be between 0 and 1')

    if mutation_coefficient < 0:
        raise ValueError('Mutation coefficient must be >= 0')

    if selection_ratio <= 0 or selection_ratio > 1:
        raise ValueError('Selection ratio must be between 0 (exclusive) and 1 (inclusive)')

    if round(population_num * selection_ratio) < 2:
        raise ValueError('The number of parents selected to breed a new generation is < 2. ' +
                         'Please increase population (' + str(population_num) + ') or selection ratio (' +
                         str(selection_ratio) + ')')


if __name__ == '__main__':
    parse_cli_arguments()
    pygame.init()
    pygame.display.set_caption("Obstacle avoidance evolution - BRAVE")
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

        if verbose < 2:
            engine.step()
        else:
            start_time = TimeUtil.current_time_millis()
            engine.step()
            end_time = TimeUtil.current_time_millis()
            step_duration = end_time - start_time
            print('Step duration: ', step_duration)

        screen.fill(Color.BLACK)

        for obj in scene.objects:
            obj.draw(screen)

            if issubclass(type(obj), SensorDrivenRobot) and obj.label is not None:
                obj.draw_label(screen)

        statistics.show()

        pygame.display.flip()
        int_scene_speed = int(round(scene.speed))
        clock.tick(int_scene_speed)
