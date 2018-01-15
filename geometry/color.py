import random


class Color:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)

    @staticmethod
    def random_color(min_r=0, min_g=0, min_b=0, max_r=255, max_g=255, max_b=255):
        r = random.randint(min_r, max_r)
        g = random.randint(min_g, max_g)
        b = random.randint(min_b, max_b)
        return r, g, b

    @staticmethod
    def random_bright(min_value=127):
        r = random.randint(min_value, 255)
        g = random.randint(min_value, 255)
        b = random.randint(min_value, 255)
        return r, g, b
