import ctypes
import time

import pygame
import pygame.locals

from src.field.field import Field
from src.field.render import (
    render_field, calc_elev_color, calc_stpn_color, render_landmasses)
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

    elev_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    stpn_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    land_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    render_field(elev_surface, field, calc_elev_color)
    render_field(stpn_surface, field, calc_stpn_color)
    render_landmasses(land_surface, field)
    mode = 0

    #cluster = Cluster(field.cells[50][100], 100)

    #popl_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    #render_cluster(popl_surface, cluster, calc_popl_color)

    window.fill([0, 0, 0])
    window.blit(elev_surface, [0, 0])
    #window.blit(popl_surface, [0, 0])
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
                mode %= 3
                if changed:
                    surface = [
                        elev_surface,
                        stpn_surface,
                        land_surface][mode]
                    window.blit(surface, [0, 0])
                    pygame.display.update()
        if not running:
            break

        time.sleep(0.0167)

    pygame.quit()
