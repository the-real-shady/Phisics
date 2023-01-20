import random
from random import randint, uniform
from math import hypot, atan, pi, cos, sin
import pygame
import sys


WIDTH, HEIGHT = (800, 800)
FPS = 60


class Luza(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, radius):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.friction = 0.2
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius, 0)

    def coll(self, washer):
        d = hypot(washer.xy[0] - self.x, washer.xy[1] - self.y)
        if d < self.radius + washer.r:
            washer.slip()

    def update(self):
        pygame.draw.circle(screen, center=(self.x, self.y), radius=self.radius, color=(121, 220, 84))


class Washer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.xy = [uniform(0 + 30, WIDTH - 30), uniform(30, HEIGHT - 30)]
        self.r = randint(5, 30)
        self.relative_mass = self.r * self.r
        self.color = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.v = [uniform(-40, 40) / self.r, uniform(-40, 40) / self.r]

    def __move__(self):
        self.xy[0] += self.v[0]
        self.xy[1] += self.v[1]
        if self.xy[0] < self.r:
            self.xy[0] = self.r
            self.v[0] *= -1
        elif self.xy[0] > self.width - self.r:
            self.xy[0] = self.width - self.r
            self.v[0] *= -1
        if self.xy[1] < self.r:
            self.xy[1] = self.r
            self.v[1] *= -1
        elif self.xy[1] > self.height - self.r:
            self.xy[1] = self.height - self.r
            self.v[1] *= -1

    def collide(self, other):
        dx = self.xy[0] - other.xy[0]
        dy = self.xy[1] - other.xy[1]
        sum_r = self.r + other.r
        if dx * dx + dy * dy > sum_r * sum_r:
            return False, 0, 0, 0, 0, 0, 0, 0, 0
        dist = hypot(dx, dy)
        ndx = dx / dist
        ndy = dy / dist
        proj = (ndx * (other.v[0] - self.v[0]) + ndy * (other.v[1] - self.v[1]))
        dvx = ndx * proj
        dvy = ndy * proj
        coef1 = 2 * other.relative_mass / (self.relative_mass + other.relative_mass)
        coef2 = 2 * self.relative_mass / (self.relative_mass + other.relative_mass)
        dvx1 = + dvx * coef1
        dvy1 = + dvy * coef1
        dvx2 = - dvx * coef2
        dvy2 = - dvy * coef2
        fix = (sum_r - dist) * 1.01 / (self.r ** 2 + other.r ** 2)
        fix1 = fix * other.r ** 2
        fix2 = fix * self.r ** 2
        dx1 = + ndx * fix1
        dy1 = + ndy * fix1
        dx2 = - ndx * fix2
        dy2 = - ndy * fix2
        return True, dvx1, dvy1, dvx2, dvy2, dx1, dy1, dx2, dy2

    def slip(self):
        new_angle = pi - atan(self.v[0] / self.v[1])
        self.v[0] -= (9.8 * 0.2 / 60 * abs(self.v[0]) / self.v[0] * cos(new_angle)) * 4
        self.v[0] -= (9.8 * 0.2 / 60 * abs(self.v[1]) / self.v[1] * sin(new_angle)) * 4


CIRCLES = [Washer(height=HEIGHT, width=WIDTH) for i in range(10)]
MAX_R = max(circ.r for circ in CIRCLES)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def collide_circles(circs):
    circs.sort(key=lambda circ: circ.xy[0])
    for left in range(len(circs) - 1):
        right = left
        while right < len(circs) - 1 and circs[right].xy[0] < circs[left].xy[0] + 2 * MAX_R:
            right += 1
            circ1 = circs[left]
            circ2 = circs[right]
            collision, dvx1, dvy1, dvx2, dvy2, dx1, dy1, dx2, dy2 = circ1.collide(circ2)
            if collision:
                circ1.v[0] += dvx1
                circ1.v[1] += dvy1
                circ2.v[0] += dvx2
                circ2.v[1] += dvy2
                circ1.xy[0] += dx1
                circ1.xy[1] += dy1
                circ2.xy[0] += dx2
                circ2.xy[1] += dy2


def update():
    for i in CIRCLES:
        i.__move__()
    collide_circles(CIRCLES)


def render():
    screen.fill((0, 0, 0))
    l.update()
    for circ in CIRCLES:
        pygame.draw.circle(screen, circ.color, circ.xy, circ.r, 0)
    pygame.display.update()
    fps.tick(FPS)


pygame.init()
all_balls = pygame.sprite.Group()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fps = pygame.time.Clock()
l = Luza(screen, random.randint(50, 800), random.randint(50, 800), random.randint(10, 150))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
    for i in CIRCLES:
        l.coll(i)
    update()
    render()
