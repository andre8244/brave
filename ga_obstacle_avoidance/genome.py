import random
import math

ROBOT_WHEEL_RADIUS_MIN = 3
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

    def __init__(self, robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                 sensor_delta_direction, sensor_saturation_value, sensor_max_distance):
        self.robot_wheel_radius = robot_wheel_radius
        self.motor_ctrl_coefficient = motor_ctrl_coefficient
        self.motor_ctrl_min_actuator_value = motor_ctrl_min_actuator_value
        self.sensor_delta_direction = sensor_delta_direction
        self.sensor_saturation_value = sensor_saturation_value
        self.sensor_max_distance = sensor_max_distance

    @staticmethod
    def random():
        robot_wheel_radius = random.uniform(ROBOT_WHEEL_RADIUS_MIN, ROBOT_WHEEL_RADIUS_MAX)
        motor_ctrl_coefficient = random.uniform(MOTOR_CTRL_COEFFICIENT_MIN, MOTOR_CTRL_COEFFICIENT_MAX)
        motor_ctrl_min_actuator_value = random.uniform(MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN,
                                                       MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX)
        sensor_delta_direction = random.uniform(SENSOR_DELTA_DIRECTION_MIN, SENSOR_DELTA_DIRECTION_MAX)
        sensor_saturation_value = random.uniform(SENSOR_SATURATION_VALUE_MIN, SENSOR_SATURATION_VALUE_MAX)
        sensor_max_distance = random.uniform(SENSOR_MAX_DISTANCE_MIN, SENSOR_MAX_DISTANCE_MAX)

        return Genome(robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                      sensor_delta_direction, sensor_saturation_value, sensor_max_distance)
