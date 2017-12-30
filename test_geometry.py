import sys
import pygame
import geometry

from pygame.locals import *
from color import Color
from point import Point
from scene.obstacle import Obstacle


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

test_num = 0
tests = None


class Test:
    def __init__(self, point1, point2, point3, point4):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4


def build_test_data():
    global tests

    tests = []

    a1 = Point(50, 50)
    a2 = Point(200, 300)
    a3 = Point(20, 20)
    a4 = Point(400, 500)
    test1 = Test(a1, a2, a3, a4)
    tests.append(test1)

    b1 = Point(800, 300)
    b2 = Point(200, 500)
    b3 = Point(300, 300)
    b4 = Point(200, 50)
    test2 = Test(b1, b2, b3, b4)
    tests.append(test2)

    c1 = Point(200, 300)
    c2 = Point(400, 300)
    c3 = Point(250, 200)
    c4 = Point(250, 500)
    test3 = Test(c1, c2, c3, c4)
    tests.append(test3)


def next_test():
    global tests
    global test_num
    test_num = (test_num + 1) % len(tests)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    build_test_data()

    while True:
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            elif event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_SPACE):
                next_test()

        screen.fill(Color.BLACK)

        test = tests[test_num]

        a1 = test.point1
        a2 = test.point2
        seg_1 = [a1, a2]

        b1 = test.point3
        b2 = test.point4
        seg_2 = [b1, b2]

        pygame.draw.line(screen, Color.GREEN, (a1.x, a1.y), (a2.x, a2.y))
        pygame.draw.line(screen, Color.RED, (b1.x, b1.y), (b2.x, b2.y))

        # intersect = geometry.check_segments_instersect(seg_1, seg_2)
        intersect = geometry.segments_intersection(seg_1, seg_2)
        print("intersect:", intersect)

        if intersect is not None:
            color_res = Color.GREEN
        else:
            color_res = Color.RED

        pygame.draw.circle(screen, color_res, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT /2)), 30)

        point_list = [(300, 300), (400, 500), (200, 400)]
        # pygame.draw.polygon(screen, Color.YELLOW, point_list)

        box = Obstacle(700, 200, 50, Color.YELLOW)
        box.draw(screen)

        pygame.display.flip()
        clock.tick(15)
