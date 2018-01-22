import random
import math

ROBOT_WHEEL_RADIUS_MIN = 8
ROBOT_WHEEL_RADIUS_MAX = 30

MOTOR_CTRL_COEFFICIENT_MIN = 50
MOTOR_CTRL_COEFFICIENT_MAX = 600

MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN = 10
MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX = 40

SENSOR_DELTA_DIRECTION_MIN = math.pi / 32
SENSOR_DELTA_DIRECTION_MAX = math.pi / 2

SENSOR_SATURATION_VALUE_MIN = 20
SENSOR_SATURATION_VALUE_MAX = 100

SENSOR_MAX_DISTANCE_MIN = 20
SENSOR_MAX_DISTANCE_MAX = 150


class Genome:

    def __init__(self, generation_num, robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                 sensor_delta_direction, sensor_saturation_value, sensor_max_distance):
        self.generation_num = generation_num
        self.robot_wheel_radius = robot_wheel_radius
        self.motor_ctrl_coefficient = motor_ctrl_coefficient
        self.motor_ctrl_min_actuator_value = motor_ctrl_min_actuator_value
        self.sensor_delta_direction = sensor_delta_direction
        self.sensor_saturation_value = sensor_saturation_value
        self.sensor_max_distance = sensor_max_distance
        self.fitness = None

    @staticmethod
    def random(generation_num):
        robot_wheel_radius = random.uniform(ROBOT_WHEEL_RADIUS_MIN, ROBOT_WHEEL_RADIUS_MAX)
        motor_ctrl_coefficient = random.uniform(MOTOR_CTRL_COEFFICIENT_MIN, MOTOR_CTRL_COEFFICIENT_MAX)
        motor_ctrl_min_actuator_value = random.uniform(MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN,
                                                       MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX)
        sensor_delta_direction = random.uniform(SENSOR_DELTA_DIRECTION_MIN, SENSOR_DELTA_DIRECTION_MAX)
        sensor_saturation_value = random.uniform(SENSOR_SATURATION_VALUE_MIN, SENSOR_SATURATION_VALUE_MAX)
        sensor_max_distance = random.uniform(SENSOR_MAX_DISTANCE_MIN, SENSOR_MAX_DISTANCE_MAX)

        return Genome(generation_num, robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                      sensor_delta_direction, sensor_saturation_value, sensor_max_distance)

    def crossover(self, other_parent, generation_num):
        # apply uniform crossover to generate a new genome
        robot_wheel_radius = self.robot_wheel_radius if random.random() < 0.5 else other_parent.robot_wheel_radius
        motor_ctrl_coefficient = self.motor_ctrl_coefficient if random.random() < 0.5 else \
            other_parent.motor_ctrl_coefficient
        motor_ctrl_min_actuator_value = self.motor_ctrl_min_actuator_value if random.random() < 0.5 else \
            other_parent.motor_ctrl_min_actuator_value
        sensor_delta_direction = self.sensor_delta_direction if random.random() < 0.5 else \
            other_parent.sensor_delta_direction
        sensor_saturation_value = self.sensor_saturation_value if random.random() < 0.5 else \
            other_parent.sensor_saturation_value
        sensor_max_distance = self.sensor_max_distance if random.random() < 0.5 else other_parent.sensor_max_distance

        # print('\nparent_a', self.to_string())
        # print('\nparent_b', parent_b.to_string())

        return Genome(generation_num, robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                      sensor_delta_direction, sensor_saturation_value, sensor_max_distance)

    def mutation(self, mutation_probability, mutation_coefficient):
        # print('\nbefore mutation', self.to_string())

        self.robot_wheel_radius = self.mutate_with_probability(self.robot_wheel_radius, mutation_probability,
                                                               mutation_coefficient)
        self.motor_ctrl_coefficient = self.mutate_with_probability(self.motor_ctrl_coefficient, mutation_probability,
                                                                   mutation_coefficient)
        self.motor_ctrl_min_actuator_value = self.mutate_with_probability(self.motor_ctrl_min_actuator_value,
                                                                          mutation_probability, mutation_coefficient)
        self.sensor_delta_direction = self.mutate_with_probability(self.sensor_delta_direction, mutation_probability,
                                                                   mutation_coefficient)
        self.sensor_saturation_value = self.mutate_with_probability(self.sensor_saturation_value, mutation_probability,
                                                                    mutation_coefficient)
        self.sensor_max_distance = self.mutate_with_probability(self.sensor_max_distance, mutation_probability,
                                                                mutation_coefficient)
        self.check_parameter_bounds()
        # print('\nafter mutation', self.to_string())

    def mutate_with_probability(self, value, mutation_probability, mutation_coefficient):
        if random.random() < mutation_probability:
            percentage_std_dev = mutation_coefficient * value
            # return random.gauss(value, mutation_coefficient)  # todo del
            return random.gauss(value, percentage_std_dev)
        else:
            return value

    def check_parameter_bounds(self):
        if self.robot_wheel_radius < ROBOT_WHEEL_RADIUS_MIN:
            self.robot_wheel_radius = ROBOT_WHEEL_RADIUS_MIN
        elif self.robot_wheel_radius > ROBOT_WHEEL_RADIUS_MAX:
            self.robot_wheel_radius = ROBOT_WHEEL_RADIUS_MAX

        if self.motor_ctrl_coefficient < MOTOR_CTRL_COEFFICIENT_MIN:
            self.motor_ctrl_coefficient = MOTOR_CTRL_COEFFICIENT_MIN
        elif self.motor_ctrl_coefficient > MOTOR_CTRL_COEFFICIENT_MAX:
            self.motor_ctrl_coefficient = MOTOR_CTRL_COEFFICIENT_MAX

        if self.motor_ctrl_min_actuator_value < MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN:
            self.motor_ctrl_min_actuator_value = MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN
        elif self.motor_ctrl_min_actuator_value > MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX:
            self.motor_ctrl_min_actuator_value = MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX

        if self.sensor_delta_direction < SENSOR_DELTA_DIRECTION_MIN:
            self.sensor_delta_direction = SENSOR_DELTA_DIRECTION_MIN
        elif self.sensor_delta_direction > SENSOR_DELTA_DIRECTION_MAX:
            self.sensor_delta_direction = SENSOR_DELTA_DIRECTION_MAX

        if self.sensor_saturation_value < SENSOR_SATURATION_VALUE_MIN:
            self.sensor_saturation_value = SENSOR_SATURATION_VALUE_MIN
        elif self.sensor_saturation_value > SENSOR_SATURATION_VALUE_MAX:
            self.sensor_saturation_value = SENSOR_SATURATION_VALUE_MAX

        if self.sensor_max_distance < SENSOR_MAX_DISTANCE_MIN:
            self.sensor_max_distance = SENSOR_MAX_DISTANCE_MIN
        elif self.sensor_max_distance > SENSOR_MAX_DISTANCE_MAX:
            self.sensor_max_distance = SENSOR_MAX_DISTANCE_MAX

    def __repr__(self):
        fitness_value = None if self.fitness is None else round(self.fitness, 2)
        return self.__class__.__name__ + '(fitness:' + repr(fitness_value) + ' generation_num:' + repr(
            self.generation_num) + ')'

    def to_string(self):
        fitness_value = None if self.fitness is None else round(self.fitness, 2)
        return self.__class__.__name__ + '(fitness:' + repr(fitness_value) + ' generation_num:' + repr(
            self.generation_num) + ' robot_wheel_radius:' + repr(
            round(self.robot_wheel_radius, 2)) + ' motor_ctrl_coefficient:' + repr(
            round(self.motor_ctrl_coefficient, 2)) + ' motor_ctrl_min_actuator_value:' + repr(
            round(self.motor_ctrl_min_actuator_value, 2)) + ' sensor_delta_direction:' + repr(
            round(self.sensor_delta_direction, 2)) + ' sensor_saturation_value:' + repr(
            round(self.sensor_saturation_value, 2)) + ' sensor_max_distance:' + repr(
            round(self.sensor_max_distance, 2)) + ')'
