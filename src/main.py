import ctypes
import time

import pygame
import pygame.locals

from src.field.field import Field
from src.field.render import render_field, calc_elev_color, calc_stpn_color
from src.field.terrain import generate_terrain
from src.npc.cluster import Cluster
from src.npc.render import render_cluster, calc_popl_color

#DEBUG
import numpy as np


if __name__ == "__main__":
    # Make the screen's DPI high (for Windows users)
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
    except:
        pass

    # Window
    pygame.init()

    window = pygame.display.set_mode(size=(1026, 514))
    pygame.display.set_caption(title="StenoChrono")

    #DEBUG
    field = Field()
    seed = 186
    # 119, 137, 153, 156, *186, 258, 281, 374, 394, 473, 573, 662
    generate_terrain(field, seed)

    field_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    render_field(field_surface, field, calc_elev_color)
    mode = 0

    cluster = Cluster(field.cells[50][100], 100)

    popl_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    render_cluster(popl_surface, cluster, calc_popl_color)

    window.fill([0, 0, 0])
    window.blit(field_surface, [0, 0])
    window.blit(popl_surface, [0, 0])
    pygame.display.update()

    # Main loop
    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            #DEBUG
            if event.type == pygame.KEYDOWN:
                changed = False
                if event.key == pygame.K_LEFT:
                    mode -= 1
                    changed = True
                if event.key == pygame.K_RIGHT:
                    mode += 1
                    changed = True
                mode %= 2
                if changed:
                    if mode == 0:
                        color_func = calc_elev_color
                    else:
                        color_func = calc_stpn_color
                    render_field(field_surface, field, color_func)
                    window.blit(field_surface, [0, 0])
                    pygame.display.update()
        if not running:
            break

        time.sleep(0.0167)

    pygame.quit()
