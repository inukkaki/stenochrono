import ctypes
import time

import pygame
import pygame.locals

#DEBUG
from src.field.field import Field
from src.field.cell import Cell
from src.field.render import (
    render_cell, render_field, RENDER_CELL_WIDTH, RENDER_CELL_HEIGHT,
    calc_cell_rect,
)


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

    field_surface = pygame.Surface(size=[1026, 514], flags=pygame.SRCALPHA)
    render_field(field_surface, field, lambda _: [255, 255, 255])

    window.fill([0, 0, 0])
    window.blit(field_surface, [0, 0])
    pygame.display.update()

    r = 0
    c = 0

    # Main loop
    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            #DEBUG
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: r -= 1
                if event.key == pygame.K_a: c -= 1
                if event.key == pygame.K_s: r += 1
                if event.key == pygame.K_d: c += 1
        if not running:
            break

        #DEBUG
        r %= field.height
        c %= field.width

        window.blit(field_surface, [0, 0])
        cell = field.cells[r][c]
        pygame.draw.rect(window, [255, 0, 0], calc_cell_rect(cell))
        for neighbor in cell.neighborhood:
            pygame.draw.rect(window, [0, 255, 255], calc_cell_rect(neighbor))
        pygame.display.update()

        time.sleep(0.0167)

    pygame.quit()
