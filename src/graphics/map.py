"""Module for rendering map elements."""

import pygame

RENDER_CELL_WIDTH = 4.0
RENDER_CELL_HEIGHT = 4.0


def calc_map_cell_rect(cell):
    """Calculates a rect that encloses a cell's area.

    Args:
        cell (src.field.cell.Cell): Cell to render.

    Returns:
        out (pygame.Rect): Rect that encloses the cell's area.
    """
    return pygame.Rect(
        float(RENDER_CELL_WIDTH*cell.pos[0]),
        float(RENDER_CELL_HEIGHT*cell.pos[1]),
        RENDER_CELL_WIDTH,
        RENDER_CELL_HEIGHT,
    )


def render_map_cell(surface, cell, color):
    """Renders a cell of the map on a surface.

    Args:
        surface (pygame.Surface): Surface for rendering the cell.
        cell (src.field.cell.Cell): Cell to render.
        color (numpy.NDArray): Color vector (RGBA).
    """
    rect = calc_map_cell_rect(cell)
    pygame.draw.rect(surface, color, rect)
