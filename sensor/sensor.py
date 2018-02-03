class Sensor:

    def __init__(self, robot, delta_direction, saturation_value, error, scene):
        self.robot = robot
        self.delta_direction = delta_direction
        self.saturation_value = saturation_value
        self.error = error
        self.scene = scene
        self.value = 0

    def get_value(self):
        # defined by subclasses
        pass

    def draw(self):
        # defined by subclasses
        pass
