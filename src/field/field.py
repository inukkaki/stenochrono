"""Module for fields."""

import itertools

from src.field.cell import Cell

FIELD_SCALE = 32

FIELD_BASE_WIDTH = 8
FIELD_BASE_HEIGHT = 4

FIELD_WIDTH = FIELD_SCALE*FIELD_BASE_WIDTH
FIELD_HEIGHT = FIELD_SCALE*FIELD_BASE_HEIGHT + 1


class Field:
    """Hexagonal map of cells.

    Attributes:
        scale (int): Scale indicating the level of detail of the terrain. The
            higher this value is, the more detailed the terrain is generated.
        width (int): Number of columns in the cell array.
        height (int): Number of rows in the cell array.
        cells (list[list[src.field.cell.Cell]]): 2D array of cells.
    """

    def __init__(self):
        """Hexagonal map of cells."""
        self.scale = FIELD_SCALE
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT

        self.cells = []
        for row in range(self.height):
            temp_cells = []
            for col in range(self.width):
                cell = Cell(row, col)
                temp_cells.append(cell)
            self.cells.append(temp_cells)
        self.set_neighborhood_of_cells()

    def set_neighborhood_of_cells(self):
        """Sets every cell's neighborhood in the array."""
        for cell in itertools.chain.from_iterable(self.cells):
            cell.neighborhood.clear()
            r, c = cell.row, cell.col
            if r >= 1:
                if r % 2 == 0:
                    cell_1 = self.cells[r - 1][(c - 1) % self.width]
                    cell_2 = self.cells[r - 1][c]
                else:
                    cell_1 = self.cells[r - 1][c]
                    cell_2 = self.cells[r - 1][(c + 1) % self.width]
                cell.neighborhood.append(cell_1)
                cell.neighborhood.append(cell_2)
            cell_3 = self.cells[r][(c - 1) % self.width]
            cell_4 = self.cells[r][(c + 1) % self.width]
            cell.neighborhood.append(cell_3)
            cell.neighborhood.append(cell_4)
            if r <= self.height - 2:
                if r % 2 == 0:
                    cell_5 = self.cells[r + 1][(c - 1) % self.width]
                    cell_6 = self.cells[r + 1][c]
                else:
                    cell_5 = self.cells[r + 1][c]
                    cell_6 = self.cells[r + 1][(c + 1) % self.width]
                cell.neighborhood.append(cell_5)
                cell.neighborhood.append(cell_6)
