"""Module for rendering cells and fields."""

import itertools

import pygame

RENDER_CELL_WIDTH = 4.0
RENDER_CELL_HEIGHT = 4.0


def calc_cell_rect(cell):
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


def render_cell(surface, cell, color_func):
    """Renders a cell on a surface.

    Args:
        surface (pygame.Surface): Surface for rendering the cell.
        cell (src.field.cell.Cell): Cell to render.
        color_func (Callable[src.field.cell.Cell, numpy.NDArray]): Function to
            calculate the rendering color.
    """
    color = color_func(cell)
    rect = calc_cell_rect(cell)
    pygame.draw.rect(surface, color, rect)


def render_field(surface, field, color_func):
    """Render a field on a surface.

    Args:
        surface (pygame.Surface): Surface for rendering the cell.
        field (src.field.field.Field): Field to render.
        color_func (Callable[src.field.cell.Cell, numpy.NDArray]): Function to
            calculate the rendering color.
    """
    for cell in itertools.chain.from_iterable(field.cells):
        render_cell(surface, cell, color_func)
