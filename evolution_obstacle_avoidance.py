import sys
import pygame
import argparse
import util.cli_parser

from pygame.locals import *

from util.side_panel import SidePanel
from util.color import Color
from scene.scene import Scene
from ga_obstacle_avoidance.ga_engine import GaEngine
from robot.sensor_driven_robot import SensorDrivenRobot
from util.time_util import TimeUtil


class EvolutionObstacleAvoidance:

    DEFAULT_SCENE_PATH = 'saved_scenes/boxes_900.txt'
    DEFAULT_SCENE_SPEED = 0  # 0 = maximum fps
    DEFAULT_VERBOSE_VALUE = 0  # 0, 1, 2
    SCENE_MAX_SPEED = 3000
    STATISTICS_PANEL_WIDTH = 450

    def __init__(self):
        self.scene = None
        self.screen = None
        self.engine = None
        self.side_panel = None
        self.population_num = None
        self.scene_speed = None
        self.scene_path = None
        self.elitism_num = None
        self.robot_random_direction = None
        self.multicore = None
        self.obstacle_sensor_error = None
        self.mutation_probability = None
        self.mutation_coefficient = None
        self.selection_ratio = None
        self.verbose = None

        self.parse_cli_arguments()
        pygame.init()
        pygame.display.set_caption("Obstacle avoidance evolution - BRAVE")
        clock = pygame.time.Clock()
        self.initialize()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_r:
                    self.initialize()
                elif event.type == KEYDOWN and (event.key == K_PLUS or event.key == 93 or event.key == 270):
                    self.increase_scene_speed()
                elif event.type == KEYDOWN and (event.key == K_MINUS or event.key == 47 or event.key == 269):
                    self.decrease_scene_speed()
                elif event.type == KEYDOWN and event.key == K_s:
                    self.engine.save_genomes()

            start_time = TimeUtil.current_time_millis()
            self.engine.step()
            end_time = TimeUtil.current_time_millis()
            step_duration = end_time - start_time
            self.printd(2, 'Step duration: ', step_duration)

            self.screen.fill(Color.BLACK)

            for obj in self.scene.objects:
                obj.draw(self.screen)

                if issubclass(type(obj), SensorDrivenRobot) and obj.label is not None:
                    obj.draw_label(self.screen)

            self.side_panel.display_ga_info()

            pygame.display.flip()
            int_scene_speed = int(round(self.scene.speed))
            clock.tick(int_scene_speed)

    def initialize(self):
        # global scene
        # global screen
        # global engine
        # global population_num
        # global scene_speed
        # global elitism_num
        # global scene_path
        # global robot_random_direction
        # global multicore
        # global side_panel
        # global obstacle_sensor_error
        # global mutation_probability
        # global mutation_coefficient
        # global selection_ratio
        # global verbose

        self.scene = Scene.load_from_file(self.scene_path, self.scene_speed, self.STATISTICS_PANEL_WIDTH)
        self.screen = self.scene.screen
        self.side_panel = SidePanel(self.scene, self.population_num)
        self.engine = GaEngine(self.scene, self.side_panel, self.population_num, self.elitism_num, self.robot_random_direction, self.multicore,
                               self.obstacle_sensor_error, self.mutation_probability, self.mutation_coefficient, self.selection_ratio, self.verbose)

    def increase_scene_speed(self):
        # global scene

        if self.scene.speed < self.SCENE_MAX_SPEED:
            self.scene.speed *= 1.5

        print('Scene speed:', self.scene.speed)

    def decrease_scene_speed(self):
        # global scene

        if self.scene.speed == 0:
            self.scene.speed = self.SCENE_MAX_SPEED

        if self.scene.speed > 1:
            self.scene.speed /= 1.5

        print('Scene speed:', self.scene.speed)

    def parse_cli_arguments(self):
        # global DEFAULT_SCENE_SPEED
        # global DEFAULT_SCENE_PATH
        # global DEFAULT_VERBOSE_VALUE
        # global population_num
        # global scene_speed
        # global elitism_num
        # global scene_path
        # global robot_random_direction
        # global multicore
        # global obstacle_sensor_error
        # global mutation_probability
        # global mutation_coefficient
        # global selection_ratio
        # global verbose

        # parser = argparse.ArgumentParser()
        #
        # parser.add_argument('-v', '--verbose', help='Set verbosity. Default: 0', type=int, choices=range(0, 3))
        #
        # parser.add_argument('-p', '--population', help='Number of vehicles in each generation. Default: ' +
        #                                   str(GaEngine.DEFAULT_POPULATION_NUM), type=int, metavar='NUM')
        #
        # parser.add_argument('-e', '--elite',
        #                     help='Number of vehicles carried over unaltered to a new generation. Default: ' + str(
        #                         GaEngine.DEFAULT_ELITISM_NUM), type=int, metavar='NUM')
        #
        # parser.add_argument('-m', '--mutation_prob',
        #                     help='Probability that a mutation occurs on a single gene. Default: ' + str(
        #                         GaEngine.DEFAULT_MUTATION_PROBABILITY), type=float, metavar='NUM')
        #
        # parser.add_argument('-M', '--mutation_coeff',
        #                     help='Coefficient used to alter a gene value during mutation. Default: ' + str(
        #                         GaEngine.DEFAULT_MUTATION_COEFFICIENT), type=float, metavar='NUM')
        #
        # parser.add_argument('-S', '--selection_ratio',
        #                     help='Ratio of parents selected to breed a new generation. Default: ' + str(
        #                         GaEngine.DEFAULT_SELECTION_RATIO), type=float, metavar='NUM')
        #
        # parser.add_argument('-s', '--scene', help='Path of the scene file. Default: ' + self.DEFAULT_SCENE_PATH,
        #                     metavar='FILE')
        #
        # parser.add_argument('-f', '--fps',
        #                     help='Number of frames per second (0 = maximum fps). Default: ' + str(self.DEFAULT_SCENE_SPEED),
        #                     type=int, metavar='NUM')
        #
        # parser.add_argument('-r', '--random_direction', help='Set an initial random direction for the vehicles',
        #                     action="store_true")
        #
        # parser.add_argument('-E', '--sensor_error',
        #                     help='Coefficient used to simulate the obstacle sensor read error. Default: ' + str(
        #                         GaEngine.DEFAULT_OBSTACLE_SENSOR_ERROR) + ', recommended: < 0.2', type=float, metavar='NUM')
        #
        # parser.add_argument('-c', '--multicore', help='Enable multicore support (experimental)', action="store_true")
        #
        # args = parser.parse_args()
        #
        # self.elitism_num = GaEngine.DEFAULT_ELITISM_NUM if args.elite is None else args.elite
        # self.population_num = GaEngine.DEFAULT_POPULATION_NUM if args.population is None else args.population
        # self.mutation_probability = GaEngine.DEFAULT_MUTATION_PROBABILITY if args.mutation_prob is None else args.mutation_prob
        # self.mutation_coefficient = GaEngine.DEFAULT_MUTATION_COEFFICIENT if args.mutation_coeff is None else args.mutation_coeff
        # self.robot_random_direction = args.random_direction
        # self.scene_speed = self.DEFAULT_SCENE_SPEED if args.fps is None else args.fps
        # self.scene_path = self.DEFAULT_SCENE_PATH if args.scene is None else args.scene
        # self.obstacle_sensor_error = GaEngine.DEFAULT_OBSTACLE_SENSOR_ERROR if args.sensor_error is None else args.sensor_error
        # self.selection_ratio = GaEngine.DEFAULT_SELECTION_RATIO if args.selection_ratio is None else args.selection_ratio
        # self.multicore = args.multicore
        # self.verbose = self.DEFAULT_VERBOSE_VALUE if args.verbose is None else args.verbose
        #
        # # check parameters value
        # if self.elitism_num < 0:
        #     raise ValueError('Elite argument must be >= 0')
        #
        # if self.population_num < 2:
        #     raise ValueError('Population argument must be >= 2')
        #
        # if self.population_num <= self.elitism_num:
        #     raise ValueError('Population argument (' + str(self.population_num) + ') must be > elite argument (' +
        #                      str(self.elitism_num) + ')')
        #
        # if self.scene_speed < 0:
        #     raise ValueError('FPS argument must be >= 0')
        #
        # if self.obstacle_sensor_error < 0:
        #     raise ValueError('Sensor error argument must be >= 0')
        #
        # if self.mutation_probability < 0 or self.mutation_probability > 1:
        #     raise ValueError('Mutation probability must be between 0 and 1')
        #
        # if self.mutation_coefficient < 0:
        #     raise ValueError('Mutation coefficient must be >= 0')
        #
        # if self.selection_ratio <= 0 or self.selection_ratio > 1:
        #     raise ValueError('Selection ratio must be between 0 (exclusive) and 1 (inclusive)')
        #
        # if round(self.population_num * self.selection_ratio) < 2:
        #     raise ValueError('The number of parents selected to breed a new generation is < 2. ' +
        #                      'Please increase population (' + str(self.population_num) + ') or selection ratio (' +
        #                      str(self.selection_ratio) + ')')

        parser = util.cli_parser.CliParser()
        parser.parse_args(True)

        self.elitism_num = parser.elitism_num
        self.population_num = parser.population_num
        self.mutation_probability = parser.mutation_probability
        self.mutation_coefficient = parser.mutation_coefficient
        self.robot_random_direction = parser.robot_random_direction
        self.scene_speed = parser.scene_speed
        self.scene_path = parser.scene_path
        self.obstacle_sensor_error = parser.obstacle_sensor_error
        self.selection_ratio = parser.selection_ratio
        self.multicore = parser.multicore
        self.verbose = parser.verbose

    def printd(self, min_debug_level, *args):
        # global verbose

        if self.verbose >= min_debug_level:
            msg = ''

            for arg in args:
                msg += str(arg) + ' '

            print(msg)


if __name__ == '__main__':
    EvolutionObstacleAvoidance()
