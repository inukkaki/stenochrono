import ctypes
import time

import pygame
import pygame.locals

#DEBUG
from src.field.cell import Cell
from src.field.render import render_cell


if __name__ == "__main__":
    # Make the screen's DPI high (for Windows users)
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
    except:
        pass

    # Window
    pygame.init()

    window = pygame.display.set_mode(size=(1024, 512))
    pygame.display.set_caption(title="StenoChrono")

    #DEBUG
    cell = Cell(0, 0)

    window.fill([0, 0, 0])
    render_cell(window, cell, lambda _: [255, 255, 255])
    pygame.display.update()

    # Main loop
    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        if not running:
            break

        time.sleep(0.0167)

    pygame.quit()
