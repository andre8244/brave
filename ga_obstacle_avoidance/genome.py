class Genome:

    def __init__(self, robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                 sensor_delta_direction, sensor_saturation_value, sensor_max_distance):
        self.robot_wheel_radius = robot_wheel_radius
        self.motor_ctrl_coefficient = motor_ctrl_coefficient
        self.motor_ctrl_min_actuator_value = motor_ctrl_min_actuator_value
        self.sensor_delta_direction = sensor_delta_direction
        self.sensor_saturation_value = sensor_saturation_value
        self.sensor_max_distance = sensor_max_distance
