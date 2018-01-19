import sys
import random

from ga_obstacle_avoidance.ga_robot import GaRobot
from sensor.proximity_sensor import ProximitySensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController
from ga_obstacle_avoidance.genome import Genome


ROBOT_SIZE = 25
OBSTACLE_SENSOR_ERROR = 0.1
ELITISM_NUM = 3
SELECTION_PERCENTAGE = 30  # 0 < SELECTION_PERCENTAGE < 100

# OBSTACLE_SENSOR_MAX_DISTANCE = 100
# OBSTACLE_SENSOR_SATURATION_VALUE = 50
# MOTOR_CONTROLLER_COEFFICIENT = 300
# MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20
# WHEEL_RADIUS = 10
# SENSOR_DIRECTION = math.pi / 8


class GaEngine:

    # todo keep last genomes in a variable (for save to file feature)

    def __init__(self, scene, population_num):
        self.scene = scene
        self.population_num = population_num
        self.robots = []
        self.genomes = []
        self.genomes_last_generation = []
        self.generation_num = 1

        for i in range(self.population_num):
            x = scene.width / 2
            y = scene.height / 2
            genome = Genome.random(self.generation_num)
            self.genomes.append(genome)
            robot = self.build_robot(x, y, genome)
            scene.put(robot)
            self.robots.append(robot)

    def step(self):
        for robot in self.robots:
            robot.sense_and_act()

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

    def build_robot(self, x, y, genome):
        robot = GaRobot(x, y, ROBOT_SIZE, genome)
        robot.direction = 0

        left_obstacle_sensor = ProximitySensor(robot, genome.sensor_delta_direction, genome.sensor_saturation_value,
                                               OBSTACLE_SENSOR_ERROR, genome.sensor_max_distance, self.scene)
        right_obstacle_sensor = ProximitySensor(robot, -genome.sensor_delta_direction, genome.sensor_saturation_value,
                                                OBSTACLE_SENSOR_ERROR, genome.sensor_max_distance, self.scene)
        left_wheel_actuator = Actuator()
        right_wheel_actuator = Actuator()
        left_motor_controller = MotorController(left_obstacle_sensor, genome.motor_ctrl_coefficient,
                                                left_wheel_actuator, genome.motor_ctrl_min_actuator_value)
        right_motor_controller = MotorController(right_obstacle_sensor, genome.motor_ctrl_coefficient,
                                                 right_wheel_actuator, genome.motor_ctrl_min_actuator_value)

        robot.set_left_motor_controller(left_motor_controller)
        robot.set_right_motor_controller(right_motor_controller)

        return robot

    def destroy_robot(self, robot):
        # save fitness value
        fitness_value = robot.mileage
        robot.genome.fitness = fitness_value

        self.scene.remove(robot)
        self.robots.remove(robot)
        print('Destroyed robot with fitness value', fitness_value)

    def create_new_generation(self):
        self.genomes_last_generation = self.genomes

        # parents of the new generation
        genomes_selected = self.ga_selection()
        print("\ngenomes selected", genomes_selected)

        new_genomes = self.ga_crossover(genomes_selected)

        sys.exit()

    def ga_selection(self):
        # sort genomes by fitness
        print('\nbefore:', str(self.genomes))  # todo del
        sorted_genomes = sorted(self.genomes, key=lambda genome: genome.fitness, reverse=True)
        print('\nafter:', str(sorted_genomes))  # todo del
        num_genomes_to_select = round(self.population_num * SELECTION_PERCENTAGE / 100)
        genomes_selected = []

        # elitism: keep the best genomes in the new generation
        for i in range(ELITISM_NUM):
            elite_genome = sorted_genomes.pop(0)
            # elite_genome.elite = True todo delete
            genomes_selected.append(elite_genome)
            num_genomes_to_select -= 1
            print("elite selected", elite_genome)

        while num_genomes_to_select > 0:
            genome_selected = self.roulette_select(sorted_genomes)
            print("genome selected", genome_selected)
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

    def ga_crossover(self, parents):
        num_genomes_to_create = self.population_num
        new_genomes = []

        # elitism: keep the best genomes in the new generation
        for i in range(ELITISM_NUM):
            new_genomes.append(parents[i])
            num_genomes_to_create -= 1

        while num_genomes_to_create > 0:
            parent_a, parent_b = self.choose_parents(parents)
            print('\nparents chosen', parent_a, parent_b)
            # todo

    def choose_parents(self, parents):
        pos_a = random.randrange(len(parents))
        parent_a = parents[pos_a]
        parents.remove(parent_a)  # avoid choosing the same parent two times
        pos_b = random.randrange(len(parents))
        parent_b = parents[pos_b]
        parents.insert(pos_a, parent_a)  # reinsert the first parent in the list
        return parent_a, parent_b
