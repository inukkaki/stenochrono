"""Module for rendering cells and fields."""

import itertools

import matplotlib.cm as cm
import numpy as np

from src.field import (
    ELEV_STD,
    SEA_LEVEL,
)
from src.field.cell import Cell
from src.graphics.map import render_map_cell

RENDER_ELEV_SEA_COLOR_DEEP = 7.0
RENDER_ELEV_LAND_COLOR_SHALLOW = 23.0

RENDER_ELEV_MIN = -4_000.0  # m
RENDER_ELEV_MAX = 4_000.0   # m

RENDER_ELEV_TONE_WIDTH = 500.0  # m
RENDER_ELEV_LAND_MAX_STEP = (
    (RENDER_ELEV_MAX - RENDER_ELEV_MIN)/RENDER_ELEV_TONE_WIDTH)

RENDER_ELEV_LAND_COLOR_MIN = 47.0
RENDER_ELEV_LAND_COLOR_MAX = 255.0
RENDER_ELEV_LAND_COLOR_WIDTH = (
    RENDER_ELEV_LAND_COLOR_MAX - RENDER_ELEV_LAND_COLOR_MIN)

RENDER_STPN_MAX = 5.0


def calc_elev_sea_color(elev):
    """Calculates the rendering color based on the elevation of a sea cell.

    Args:
        elev (float): Elevation of the cell whose surface is sea.

    Returns:
        out (float): Monochrome color value.
    """
    if elev < SEA_LEVEL - ELEV_STD:
        c = RENDER_ELEV_SEA_COLOR_DEEP
    else:
        c = RENDER_ELEV_LAND_COLOR_SHALLOW
    return c


def calc_elev_land_color(elev):
    """Calculates the rendering color based on the elevation of a land cell.

    Args:
        elev (float): Elevation of the cell whose surface is land.

    Returns:
        out (float): Monochrome color value.
    """
    if elev < RENDER_ELEV_MIN:
        c = RENDER_ELEV_LAND_COLOR_MIN
    elif RENDER_ELEV_MAX < elev:
        c = RENDER_ELEV_LAND_COLOR_MAX
    else:
        step = (elev - RENDER_ELEV_MIN)//RENDER_ELEV_TONE_WIDTH
        c = RENDER_ELEV_LAND_COLOR_WIDTH/np.power(RENDER_ELEV_LAND_MAX_STEP, 3)
        c *= np.power(step, 3)
        c += RENDER_ELEV_LAND_COLOR_MIN
        c = float(int(c))
    return c


def calc_elev_color(cell):
    """Calculates the rendering color based on the elevation of a cell.

    Args:
        cell (src.field.cell.Cell): Cell to render.

    Returns:
        out (numpy.NDArray): Color vector (RGBA).
    """
    if cell.surface == Cell.SURFACE_SEA:
        c = calc_elev_sea_color(cell.elev)
        color = np.array([c, c, c, 255.0], dtype=np.float32)
    elif cell.surface == Cell.SURFACE_LAND:
        c = calc_elev_land_color(cell.elev)
        color = np.array([c, c, c, 255.0], dtype=np.float32)
    else:
        color = np.array([255.0, 0.0, 255.0, 255.0], dtype=np.float32)
    return color


def calc_stpn_color(cell):
    """Calculates the rendering color based on the steepness of a cell.

    Args:
        cell (src.field.cell.Cell): Cell to render.

    Returns:
        out (numpy.NDArray): Color vector (RGBA).
    """
    if cell.surface == Cell.SURFACE_SEA:
        c = calc_elev_sea_color(cell.elev)
        color = np.array([c, c, c, 255.0], dtype=np.float32)
    elif cell.surface == Cell.SURFACE_LAND:
        x = min(cell.stpn, RENDER_STPN_MAX)/RENDER_STPN_MAX
        color = 255.0*np.array(cm.viridis(x), dtype=np.float32)
    else:
        color = np.array([255.0, 0.0, 255.0, 255.0], dtype=np.float32)
    return color


def render_cell(surface, cell, color_func):
    """Renders a cell on a surface.

    Args:
        surface (pygame.Surface): Surface for rendering the cell.
        cell (src.field.cell.Cell): Cell to render.
        color_func (Callable[src.field.cell.Cell, numpy.NDArray]): Function to
            calculate the rendering color.
    """
    color = color_func(cell)
    render_map_cell(surface, cell, color)


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
