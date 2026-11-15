import pygame as pg
import sys
from celestial_bodies import body
from utils import *
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 1250, 900

pg.init()

font = pg.font.SysFont('arial', 24)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('planetary simulation')

clock = pg.time.Clock()

bodies = []

#earth = body('earth', (1e11 * i ** 1.3, -1e11 * i ** 2), 5.97e24, 6.371e6)
#mars = body('mars', (2.25e11, 2.25e11), 6.42e23, 3.389e6)
#jupiter = body('jupiter', (2.25e12, -2.25e11), 1.898e27, 6.9e7)

star = body('star', (0, 0), 2.0e30, 7.0e8)
pA = body('planet A', (1.5e11, 0), 6.0e24, 6.0e6)
pB = body('planet B', (0, 7.8e11), 1.9e27, 7.0e7)

star.velocity = [0, 0]
pA.velocity = [0, 29800]
pB.velocity = [-13100, 0]

bodies.append(star)
bodies.append(pA)
bodies.append(pB)

largest_body = find_largest(bodies)
SCALE = largest_body * 20.0
print(SCALE)

time = 0.0

camera_pos = [0, 0]
zoom = 1e-8

RUNNING = True
while RUNNING:
    font_surf = font.render(str(round(time, 2)), True, pg.Color('white'))
    dt = clock.tick(240) / 1000
    sped_up_dt = dt * 100000000
    time += dt

    screen.fill(pg.Color('black'))

    for b in bodies:
        for other in bodies:
            if b != other:
                b.update_velocity(other, sped_up_dt)

    for b in bodies:
        b.update_position(sped_up_dt)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUNNING = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                RUNNING = False
        if event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                zoom *= 1.2
            if event.y < 0:
                zoom /= 1.2

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        camera_pos[1] -= 1e12 * dt

    if keys[pg.K_s]:
        camera_pos[1] += 1e12 * dt

    if keys[pg.K_a]:
        camera_pos[0] -= 1e12 * dt

    if keys[pg.K_d]:
        camera_pos[0] += 1e12 * dt

    for b in bodies:
        screen_pos = world_to_screen(b.position, camera_pos, zoom)
        screen_radius = max(2, int(b.radius * zoom))
        radius = b.radius * zoom * 1000
        if radius <= 1: radius = 1
        pg.draw.circle(screen, pg.Color('white'), screen_pos, screen_radius * 10)

    screen.blit(font_surf, (50, 50))
    pg.display.update()

pg.quit()