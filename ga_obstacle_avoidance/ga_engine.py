import random
import multiprocessing
import math

from ga_obstacle_avoidance.ga_robot import GaRobot
from ga_obstacle_avoidance.thread_ga_robot import ThreadGaRobot
from sensor.proximity_sensor import ProximitySensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController
from ga_obstacle_avoidance.genome import Genome
from time_util import TimeUtil


class GaEngine:

    ROBOT_SIZE = 25
    DEFAULT_POPULATION_NUM = 500
    DEFAULT_ELITISM_NUM = 3
    DEFAULT_OBSTACLE_SENSOR_ERROR = 0
    DEFAULT_MUTATION_PROBABILITY = 0.3  # 0 < MUTATION_PROBABILITY < 1
    DEFAULT_MUTATION_COEFFICIENT = 0.07
    SELECTION_PERCENTAGE = 0.3  # 0 < SELECTION_PERCENTAGE < 1

    def __init__(self, scene, statistics, population_num, elitism_num, robot_random_direction, multicore,
                 obstacle_sensor_error, mutation_probability, mutation_coefficient):
        if population_num <= elitism_num:
            raise ValueError(
                'Error: population_num (' + str(population_num) + ') must be greater than elitism_num (' + str(
                    elitism_num) + ')')

        self.scene = scene
        self.statistics = statistics
        self.population_num = population_num
        self.elitism_num = elitism_num
        self.robot_random_direction = robot_random_direction
        self.multicore = multicore
        self.obstacle_sensor_error = obstacle_sensor_error
        self.mutation_probability = mutation_probability
        self.mutation_coefficient = mutation_coefficient
        self.robots = []
        self.genomes = []
        self.genomes_last_generation = []
        self.best_genome = None
        self.generation_num = 1
        self.num_cpu = multiprocessing.cpu_count()
        self.start_total_time = TimeUtil.current_time_millis()
        self.start_generation_time = self.start_total_time

        for i in range(self.population_num):
            x, y = self.robot_start_position()
            genome = Genome.random(self.generation_num)
            self.genomes.append(genome)
            robot = self.build_robot(x, y, genome, None)
            scene.put(robot)
            self.robots.append(robot)

        self.statistics.update_data(self.generation_num, None, None)
        self.statistics.update_time(0, 0)

        print('\nGeneration', self.generation_num, 'started')
        print('multicore:', self.multicore)

    def step(self):
        # start_time = TimeUtil.current_time_millis()

        if self.multicore:
            threads = []

            # print('')

            num_robots = len(self.robots)
            num_robots_per_cpu = math.floor(num_robots / self.num_cpu)

            # print('num_robots_per_cpu', num_robots_per_cpu)

            for i in range(self.num_cpu - 1):
                start_pos = i * num_robots_per_cpu
                end_pos = (i + 1) * num_robots_per_cpu
                # print('core', str(i+1), 'positions', start_pos, ':', end_pos)
                robot_list = self.robots[start_pos:end_pos]

                thread = ThreadGaRobot(robot_list)
                thread.start()
                # print('thread', str(i+1), 'started')
                threads.append(thread)

            # last sublist of robots
            start_pos = (self.num_cpu - 1) * num_robots_per_cpu
            # print('last core, start_pos', start_pos)
            robot_list = self.robots[start_pos:]

            thread = ThreadGaRobot(robot_list)
            thread.start()
            # print('last thread started')
            threads.append(thread)

            for t in threads:
                t.join()

            # end_time = TimeUtil.current_time_millis()
            # partial_duration = end_time - start_time
            # print('   partial duration', partial_duration)

            for robot in self.robots:
                # ensure robot doesn't accidentaly go outside of the scene
                if robot.x < 0 or robot.x > self.scene.width or robot.y < 0 or robot.y > self.scene.height:
                    self.destroy_robot(robot)

                # destroy robot if it collides an obstacle
                if robot.collision_with_object:
                    self.destroy_robot(robot)
        else:
            # multicore = False
            for robot in self.robots:
                robot.sense_and_act()

                # thread = ThreadGaRobot(robot)
                # thread.start()
                # threads.append(thread)

                # ensure robot doesn't accidentaly go outside of the scene
                if robot.x < 0 or robot.x > self.scene.width or robot.y < 0 or robot.y > self.scene.height:
                    self.destroy_robot(robot)

                # destroy robot if it collides an obstacle
                if robot.collision_with_object:
                    self.destroy_robot(robot)

        # check population extinction
        if not self.robots:
            print('Generation', self.generation_num, 'terminated')
            self.create_new_generation()
            self.statistics.update_data(self.generation_num, self.best_genome, self.best_genome.fitness)

        # update statistics time
        current_time = TimeUtil.current_time_millis()
        total_time_seconds = math.floor((current_time - self.start_total_time) / 1000)
        generation_time_seconds = math.floor((current_time - self.start_generation_time) / 1000)
        self.statistics.update_time(total_time_seconds, generation_time_seconds)

    def build_robot(self, x, y, genome, label):
        robot = GaRobot(x, y, self.ROBOT_SIZE, genome)

        if not self.robot_random_direction:
            robot.direction = 0

        left_obstacle_sensor = ProximitySensor(robot, genome.sensor_delta_direction, genome.sensor_saturation_value,
                                               self.obstacle_sensor_error, genome.sensor_max_distance, self.scene)
        right_obstacle_sensor = ProximitySensor(robot, -genome.sensor_delta_direction, genome.sensor_saturation_value,
                                                self.obstacle_sensor_error, genome.sensor_max_distance, self.scene)
        left_wheel_actuator = Actuator()
        right_wheel_actuator = Actuator()
        left_motor_controller = MotorController(left_obstacle_sensor, genome.motor_ctrl_coefficient,
                                                left_wheel_actuator, genome.motor_ctrl_min_actuator_value)
        right_motor_controller = MotorController(right_obstacle_sensor, genome.motor_ctrl_coefficient,
                                                 right_wheel_actuator, genome.motor_ctrl_min_actuator_value)

        robot.set_left_motor_controller(left_motor_controller)
        robot.set_right_motor_controller(right_motor_controller)
        robot.label = label

        return robot

    def destroy_robot(self, robot):
        # save fitness value
        fitness_value = robot.mileage
        robot.genome.fitness = fitness_value

        self.scene.remove(robot)
        self.robots.remove(robot)
        # print('Destroyed robot with fitness value', fitness_value)

    def create_new_generation(self):
        self.genomes_last_generation = self.genomes
        genomes_selected = self.ga_selection()  # parents of the new generation
        # print("\ngenomes selected", genomes_selected)
        self.generation_num += 1
        new_genomes = self.ga_crossover_mutation(genomes_selected)
        self.genomes = new_genomes

        # draw a label for the elite individuals
        elite_label = 1

        for genome in self.genomes:
            if elite_label <= self.elitism_num:
                label = elite_label
                elite_label += 1
            else:
                label = None

            x, y = self.robot_start_position()
            robot = self.build_robot(x, y, genome, label)
            self.scene.put(robot)
            self.robots.append(robot)

        # reset generation time
        self.start_generation_time = TimeUtil.current_time_millis()
        print('\nGeneration', self.generation_num, 'started')

    def ga_selection(self):
        # sort genomes by fitness
        sorted_genomes = sorted(self.genomes, key=lambda genome: genome.fitness, reverse=True)
        best_genome_current_generation = sorted_genomes[0]

        if self.best_genome is None or best_genome_current_generation.fitness > self.best_genome.fitness:
            self.best_genome = best_genome_current_generation
            print('New best:', self.best_genome.to_string())

        num_genomes_to_select = round(self.population_num * self.SELECTION_PERCENTAGE)

        if num_genomes_to_select < 2:
            raise ValueError('The number of parents for the new generation is < 2. ' +
                             'Please increase population (' + str(self.population_num) + ') or selection percentage (' +
                             str(self.SELECTION_PERCENTAGE) + ')')

        genomes_selected = []

        # elitism: keep the best genomes in the new generation
        for i in range(self.elitism_num):
            elite_genome = sorted_genomes.pop(0)
            genomes_selected.append(elite_genome)
            num_genomes_to_select -= 1
            print("Elite:", elite_genome.to_string())

        while num_genomes_to_select > 0:
            genome_selected = self.roulette_select(sorted_genomes)
            genomes_selected.append(genome_selected)
            sorted_genomes.remove(genome_selected)
            num_genomes_to_select -= 1

        return genomes_selected

    def roulette_select(self, genomes):
        fitness_sum = 0

        for genome in genomes:
            fitness_sum += genome.fitness

        value = random.uniform(0, fitness_sum)

        for i in range(len(genomes)):
            value -= genomes[i].fitness

            if value < 0:
                return genomes[i]

        return genomes[-1]

    def ga_crossover_mutation(self, parents):
        num_genomes_to_create = self.population_num
        new_genomes = []

        # elitism: keep the best genomes in the new generation
        for i in range(self.elitism_num):
            new_genomes.append(parents[i])
            num_genomes_to_create -= 1

        while num_genomes_to_create > 0:
            parent_a, parent_b = self.choose_parents(parents)
            new_genome = parent_a.crossover(parent_b, self.generation_num)
            new_genome.mutation(self.mutation_probability, self.mutation_coefficient)
            new_genomes.append(new_genome)
            num_genomes_to_create -= 1

        return new_genomes

    def choose_parents(self, parents):
        pos_a = random.randrange(len(parents))
        parent_a = parents[pos_a]
        parents.remove(parent_a)  # avoid choosing the same parent two times
        pos_b = random.randrange(len(parents))
        parent_b = parents[pos_b]
        parents.insert(pos_a, parent_a)  # reinsert the first parent in the list
        return parent_a, parent_b

    def robot_start_position(self):
        x = self.scene.width / 2
        y = self.scene.height / 2
        return x, y
