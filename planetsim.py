import pygame as pg
import sys
from celestial_bodies import body
from utils import *
import matplotlib.pyplot as plt
from copy import deepcopy
import pprint

WIDTH, HEIGHT = 1250, 900

pg.init()

font = pg.font.SysFont('arial', 20)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('planetary simulation')

clock = pg.time.Clock()

bodies = []

#earth = body('earth', (1e11 * i ** 1.3, -1e11 * i ** 2), 5.97e24, 6.371e6)
#mars = body('mars', (2.25e11, 2.25e11), 6.42e23, 3.389e6)
#jupiter = body('jupiter', (2.25e12, -2.25e11), 1.898e27, 6.9e7)

star = body('star', (0, 0), 2.0e30, 7.0e8)
pA = body('planet A', (1.5e11, 0), 6.0e24, 6.0e6)
pB = body('planet B', (0, 7.8e11), 1.9e24, 7.0e7)

star.velocity = [0, 0]
pA.velocity = [0, 29800]
pB.velocity = [-13100, 0]

bodies.append(star)
bodies.append(pA)
bodies.append(pB)

copy_bodies = deepcopy(bodies)

time = 0.0
sped_time_passed = 0.0

camera_pos = [0, 0]
zoom = 1e-8

initial_speed_mult = 1000
dt_multiplier = initial_speed_mult

RUNNING = True
while RUNNING:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUNNING = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                RUNNING = False
            if event.key == pg.K_UP:
                dt_multiplier *= 2 #can speed up or slow down the sim
            if event.key == pg.K_DOWN:
                dt_multiplier /= 2
            if event.key == pg.K_r:
                bodies = deepcopy(copy_bodies)
                dt_multiplier = initial_speed_mult
                sped_time_passed = 0
                time = 0
                camera_pos = [0, 0]
        if event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                zoom *= 1.2
            if event.y < 0:
                zoom /= 1.2
    fps_text = font.render(str(round(time, 2)), True, pg.Color('white'))
    multiplier_text = font.render((str(round(dt_multiplier, 2)) + "x speed"), True, pg.Color('white'))

    dt = clock.tick(240) / 1000
    sped_up_dt = dt * dt_multiplier
    time += dt
    sped_time_passed += sped_up_dt

    time_passed_text = font.render(get_time_passed(sped_time_passed), True, pg.Color('white'))

    screen.fill(pg.Color('black'))

    force_list = []
    forces_dict = {}
    for b in bodies:
        forces_dict[b] = {}

        for other in bodies:
            if b != other:
                b.update_velocity(other, sped_up_dt)
                
                force = b.calculate_pull(other)
                force_list.append(force)
                forces_dict[b][other] = force

    max_force = max(force_list)
    force_line_color = max_force / 255 + 10
    #pprint.pp(forces_dict)


    for b in bodies:
        b.update_position(sped_up_dt)



    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        camera_pos[1] -= 1e12 * dt

    if keys[pg.K_s]:
        camera_pos[1] += 1e12 * dt

    if keys[pg.K_a]:
        camera_pos[0] -= 1e12 * dt

    if keys[pg.K_d]:
        camera_pos[0] += 1e12 * dt

    line_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

    for b in bodies:
        screen_pos = world_to_screen(b.position, camera_pos, zoom)
        screen_radius = max(2, int(b.radius * zoom))
        radius = b.radius * zoom
        radius = max(radius, 1)
        pg.draw.circle(screen, pg.Color('white'), screen_pos, radius)
        for other in forces_dict[b]:
            rgb_val = max(0, min(255, int(forces_dict[b][other] / force_line_color)))
            other_screen_pos = world_to_screen(other.position, camera_pos, zoom)
            pg.draw.line(line_surface, (255 - rgb_val, rgb_val, 0, 128), (screen_pos), (other_screen_pos), 1)

    screen.blit(line_surface, (0, 0))
    screen.blit(fps_text, (50, 50))
    screen.blit(multiplier_text, (50, 100))
    screen.blit(time_passed_text, (50, 150))

    pg.display.update()

pg.quit()