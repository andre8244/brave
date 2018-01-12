from robot.sensor_driven_robot import SensorDrivenRobot
from sensor.proximity_sensor import ProximitySensor
from robot.actuator import Actuator
from robot.motor_controller import MotorController
from ga_obstacle_avoidance.genome import Genome


ROBOT_SIZE = 25
OBSTACLE_SENSOR_ERROR = 0.1

# OBSTACLE_SENSOR_MAX_DISTANCE = 100
# OBSTACLE_SENSOR_SATURATION_VALUE = 50
# MOTOR_CONTROLLER_COEFFICIENT = 300
# MOTOR_CONTROLLER_MIN_ACTUATOR_VALUE = 20


class GaEngine:

    def __init__(self, scene, initial_population):
        self.scene = scene
        self.population = []

        for i in range(initial_population):
            x = scene.width / 2
            y = scene.height / 2
            genome = Genome.random()
            # robot = self.build_robot(x, y, 10, math.pi / 8)
            robot = self.build_robot(x, y, genome)
            scene.put(robot)
            self.population.append(robot)

    def step(self):
        for robot in self.population:
            robot.sense_and_act()

            # ensure robots don't go accidentaly outside of the scene
            if robot.x < 0 or robot.x > self.scene.width or robot.y < 0 or robot.y > self.scene.height:
                self.kill_robot(robot)

            # todo check robot.collision_with_object and possibly remove robot from population AND scene
            # todo check population count and possibly create a new generation

    def build_robot(self, x, y, genome):
        robot = SensorDrivenRobot(x, y, ROBOT_SIZE, genome.robot_wheel_radius)
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

    def kill_robot(self, robot):
        self.scene.remove(robot)
        self.population.remove(robot)
        print('Killed robot', robot)
