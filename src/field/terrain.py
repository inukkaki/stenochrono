"""Module for terrain generation."""

import itertools

import numpy as np

from src.field import (
    ELEV_MEAN,
    ELEV_STD,
    SEA_LEVEL,
)
from src.field.cell import Cell

ELEV_GEN_N = -0.75  # Elevation at the northen end
ELEV_GEN_S = 0.5    # Elevation at the southern end
ELEV_GEN_WE = -0.8  # Elevation at the western/eastern end

ELEV_GEN_MEAN = 0.0
ELEV_GEN_STD = 1.0

ELEV_GEN_COMPLEXITY = 1.0

ELEV_GEN_ADJUST_OFFSET = -0.25
ELEV_GEN_ADJUST_SCALE = 0.5

STPN_FACTOR = 1/100  # m -1


def create_close_list(field):
    """Creates a close list consistent with cells in a field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.

    Returns:
        out (list[list[bool]]): Close list. The default value for all elements
            is False.
    """
    close_list = []
    for _ in range(field.height):
        temp_list = []
        for _ in range(field.width):
            temp_list.append(False)
        close_list.append(temp_list)
    return close_list


def init_elevs(field, rng, close_list):
    """Initializes the elevation of cells in a field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        rng (numpy.random.Generator): Random number generator for terrain
            generation.
        close_list (list[list[bool]]): Close list.
    """
    s = field.scale
    for i in range(field.height):
        for j in range(field.width):
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            is_initial_cell = (r % s == 0) and (c % s == ((r//s) % 2)*s//2)
            if r == 0:
                # Cells at the northern end
                cell.elev = ELEV_GEN_N
                close_list[i][j] = True
            elif r == field.height - 1:
                # Cells at the southern end
                cell.elev = ELEV_GEN_S
                close_list[i][j] = True
            elif c == 0:
                # Cells at the western/eastern end
                cell.elev = ELEV_GEN_WE
                close_list[i][j] = True
            elif is_initial_cell:
                # Cells that have an initial elevation
                cell.elev = rng.normal(loc=ELEV_GEN_MEAN, scale=ELEV_GEN_STD)
                close_list[i][j] = True


def interpolate_elevs_horizontally(field, rng, close_list, scale, complexity):
    """Interpolates the elevation of cells in a field horizontally.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        rng (numpy.random.Generator): Random number generator for terrain
            generation.
        close_list (list[list[bool]]): Close list.
        scale (int): Interpolation scale.
        complexity (float): Complexity of the elevation.
    """
    for i in range(0, field.height, scale):
        for j in range(0, field.width, scale//2):
            if close_list[i][j]:
                continue
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            ref_cell_1 = field.cells[r][(c - scale//2) % field.width]
            ref_cell_2 = field.cells[r][(c + scale//2) % field.width]
            cell.elev = (ref_cell_1.elev + ref_cell_2.elev)/2
            cell.elev += rng.normal(loc=0.0, scale=complexity)
            close_list[i][j] = True


def interpolate_elevs_vertically_nw_se(
        field, rng, close_list, scale, complexity):
    """Interpolates the elevation of cells in a field vertically, referencing
    to the elevation of the north-west and south-east cells.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        rng (numpy.random.Generator): Random number generator for terrain
            generation.
        close_list (list[list[bool]]): Close list.
        scale (int): Interpolation scale.
        complexity (float): Complexity of the elevation.
    """
    for i in range(scale//2, field.height, scale):
        j_start = (2*((i//scale) % 2) + 1)*scale//4
        for j in range(j_start, field.width, scale):
            if close_list[i][j]:
                continue
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            ref_cell_1 = field.cells[r - scale//2][c - scale//4]
            ref_cell_2 = \
                field.cells[r + scale//2][(c + scale//4) % field.width]
            cell.elev = (ref_cell_1.elev + ref_cell_2.elev)/2
            cell.elev += rng.normal(loc=0.0, scale=complexity)
            close_list[i][j] = True


def interpolate_elevs_vertically_ne_sw(
        field, rng, close_list, scale, complexity):
    """Interpolates the elevation of cells in a field vertically, referencing
    to the elevation of the north-east and south-west cells.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        rng (numpy.random.Generator): Random number generator for terrain
            generation.
        close_list (list[list[bool]]): Close list.
        scale (int): Interpolation scale.
        complexity (float): Complexity of the elevation.
    """
    for i in range(scale//2, field.height, scale):
        j_start = (3 - 2*((i//scale) % 2))*scale//4
        for j in range(j_start, field.width, scale):
            if close_list[i][j]:
                continue
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            ref_cell_1 = \
                field.cells[r - scale//2][(c + scale//4) % field.width]
            ref_cell_2 = field.cells[r + scale//2][c - scale//4]
            cell.elev = (ref_cell_1.elev + ref_cell_2.elev)/2
            cell.elev += rng.normal(loc=0.0, scale=complexity)
            close_list[i][j] = True


def interpolate_elevs(field, rng, close_list):
    """Interpolates the elevation of cells in a field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        rng (numpy.random.Generator): Random number generator for terrain
            generation.
        close_list (list[list[bool]]): Close list.
    """
    scale = field.scale
    complexity = ELEV_GEN_COMPLEXITY
    while scale > 1:
        interpolate_elevs_horizontally(
            field, rng, close_list, scale, complexity)
        interpolate_elevs_vertically_nw_se(
            field, rng, close_list, scale, complexity)
        interpolate_elevs_vertically_ne_sw(
            field, rng, close_list, scale, complexity)
        scale //= 2
        complexity /= 2


def lower_elevs_in_south_half(field):
    """Lowers the elevation of cells in the southern half of the field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
    """
    for cell in itertools.chain.from_iterable(field.cells):
        phase = 2*np.pi*cell.row/(field.height - 1)
        cell.elev += ELEV_GEN_ADJUST_OFFSET
        cell.elev += ELEV_GEN_ADJUST_SCALE*np.sin(phase)


def rescale_elevs(field, mean, std):
    """Rescales the distribution of the elevation in the field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        mean (float): Mean of the elevation.
        std (float): Standard deviation of the elevation.
    """
    scale = std/ELEV_GEN_STD
    for cell in itertools.chain.from_iterable(field.cells):
        cell.elev = scale*cell.elev + mean


def generate_elevs(field, rng):
    """Generates the elevation of cells in a field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        rng (numpy.random.Generator): Random number generator for terrain
            generation.
    """
    close_list = create_close_list(field)
    init_elevs(field, rng, close_list)
    interpolate_elevs(field, rng, close_list)
    lower_elevs_in_south_half(field)
    rescale_elevs(field, ELEV_MEAN, ELEV_STD)


def determine_sea_or_land(field):
    """Determines if the surface of cells in a field is sea or land.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
    """
    for cell in itertools.chain.from_iterable(field.cells):
        if cell.elev < SEA_LEVEL:
            cell.surface = Cell.SURFACE_SEA
        else:
            cell.surface = Cell.SURFACE_LAND


def calc_stpns(field):
    """Calculates the steepness of cells in a field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
    """
    for cell in itertools.chain.from_iterable(field.cells):
        cell.stpn = 0.0
        for neighbor in cell.neighborhood:
            cell.stpn += STPN_FACTOR*abs(neighbor.elev - cell.elev)
        cell.stpn /= len(cell.neighborhood)


def generate_terrain(field, seed):
    """Generates the terrain on a field.

    Args:
        field (src.field.field.Field): Field to generate the terrain on.
        seed (int): Seed value for terrain generation.
    """
    field.seed = seed
    rng = np.random.default_rng(field.seed)
    generate_elevs(field, rng)
    determine_sea_or_land(field)
    calc_stpns(field)
