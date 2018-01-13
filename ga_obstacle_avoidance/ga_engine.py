from ga_obstacle_avoidance.ga_robot import GaRobot
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
# WHEEL_RADIUS = 10
# SENSOR_DIRECTION = math.pi / 8


class GaEngine:

    # todo keep genomes in a list?
    # todo keep last genomes in a variable (for save to file feature)

    def __init__(self, scene, initial_population):
        self.scene = scene
        self.population = []
        self.genomes = []
        self.generation_count = 1

        for i in range(initial_population):
            x = scene.width / 2
            y = scene.height / 2
            genome = Genome.random()
            self.genomes.append(genome)
            robot = self.build_robot(x, y, genome)
            scene.put(robot)
            self.population.append(robot)

    def step(self):
        for robot in self.population:
            robot.sense_and_act()

            # ensure robot doesn't accidentaly go outside of the scene
            if robot.x < 0 or robot.x > self.scene.width or robot.y < 0 or robot.y > self.scene.height:
                self.destroy_robot(robot)

            # destroy robot if it collides an obstacle
            if robot.collision_with_object:
                self.destroy_robot(robot)

            # check population extinction
            if not self.population:
                print('Extinction!')
                # todo create a new generation

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
        self.population.remove(robot)
        print('Destroyed robot with fitness value', fitness_value)
