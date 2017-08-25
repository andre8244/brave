from rot_surface import RotSurface


class Sensor(RotSurface):

    # applico al sensore gli stessi spostamenti (x, y, direction) del robot su cui e' montato

    def __init__(self, x, y, direction, surf, saturation_value):
        super().__init__(x, y, direction, surf)
        self.saturation_value = saturation_value
