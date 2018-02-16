import argparse

from evolution_obstacle_avoidance import EvolutionObstacleAvoidance
from ga_obstacle_avoidance.ga_engine import GaEngine
from util.scene_type import SceneType


class CliParser:

    def __init__(self):
        self.elitism_num = None
        self.population_num = None
        self.mutation_probability = None
        self.mutation_coefficient = None
        self.robot_random_direction = None
        self.obstacle_sensor_error = None
        self.selection_ratio = None
        self.multicore = None
        self.verbose = None
        self.scene_path = None
        self.scene_speed = None
        self.genomes_path = None

    def parse_args(self, default_scene_path, default_scene_speed, scene_type):
        parser = argparse.ArgumentParser()

        if scene_type == SceneType.GA_OBSTACLE_AVOIDANCE:
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

            parser.add_argument('-S', '--selection_ratio',
                                help='Ratio of parents selected to breed a new generation. Default: ' + str(
                                    GaEngine.DEFAULT_SELECTION_RATIO), type=float, metavar='NUM')

            parser.add_argument('-r', '--random_direction', help='Set an initial random direction for the vehicles',
                                action="store_true")

            parser.add_argument('-E', '--sensor_error',
                                help='Coefficient used to simulate the obstacle sensor read error. Default: ' + str(
                                    GaEngine.DEFAULT_OBSTACLE_SENSOR_ERROR) + ', recommended: < 0.2', type=float, metavar='NUM')

            parser.add_argument('-c', '--multicore', help='Enable multicore support (experimental)', action="store_true")

        if scene_type == SceneType.OBSTACLE_AVOIDANCE:
            parser.add_argument('-g', '--genomes', help='Path of the genome file. Default: none', metavar='FILE')

        parser.add_argument('-s', '--scene', help='Path of the scene file. Default: ' + default_scene_path,
                            metavar='FILE')

        parser.add_argument('-f', '--fps',
                            help='Maximum frame rate (0 = no limit). Default: ' + str(default_scene_speed),
                            type=int, metavar='NUM')

        args = parser.parse_args()

        if scene_type == SceneType.GA_OBSTACLE_AVOIDANCE:
            self.elitism_num = GaEngine.DEFAULT_ELITISM_NUM if args.elite is None else args.elite
            self.population_num = GaEngine.DEFAULT_POPULATION_NUM if args.population is None else args.population
            self.mutation_probability = GaEngine.DEFAULT_MUTATION_PROBABILITY if args.mutation_prob is None else args.mutation_prob
            self.mutation_coefficient = GaEngine.DEFAULT_MUTATION_COEFFICIENT if args.mutation_coeff is None else args.mutation_coeff
            self.robot_random_direction = args.random_direction
            self.obstacle_sensor_error = GaEngine.DEFAULT_OBSTACLE_SENSOR_ERROR if args.sensor_error is None else args.sensor_error
            self.selection_ratio = GaEngine.DEFAULT_SELECTION_RATIO if args.selection_ratio is None else args.selection_ratio
            self.multicore = args.multicore
            self.verbose = EvolutionObstacleAvoidance.DEFAULT_VERBOSE_VALUE if args.verbose is None else args.verbose

        if scene_type == SceneType.OBSTACLE_AVOIDANCE:
            self.genomes_path = args.genomes

        self.scene_path = default_scene_path if args.scene is None else args.scene
        self.scene_speed = default_scene_speed if args.fps is None else args.fps

        # check parameters value

        if self.scene_speed < 0:
            raise ValueError('FPS argument must be >= 0')

        if scene_type == SceneType.GA_OBSTACLE_AVOIDANCE:
            if self.elitism_num < 0:
                raise ValueError('Elite argument must be >= 0')

            if self.population_num < 2:
                raise ValueError('Population argument must be >= 2')

            if self.population_num <= self.elitism_num:
                raise ValueError('Population argument (' + str(self.population_num) + ') must be > elite argument (' +
                                 str(self.elitism_num) + ')')

            if self.obstacle_sensor_error < 0:
                raise ValueError('Sensor error argument must be >= 0')

            if self.mutation_probability < 0 or self.mutation_probability > 1:
                raise ValueError('Mutation probability must be between 0 and 1')

            if self.mutation_coefficient < 0:
                raise ValueError('Mutation coefficient must be >= 0')

            if self.selection_ratio <= 0 or self.selection_ratio > 1:
                raise ValueError('Selection ratio must be between 0 (exclusive) and 1 (inclusive)')

            if round(self.population_num * self.selection_ratio) < 2:
                raise ValueError('The number of parents selected to breed a new generation is < 2. ' +
                                 'Please increase population (' + str(self.population_num) + ') or selection ratio (' +
                                 str(self.selection_ratio) + ')')
