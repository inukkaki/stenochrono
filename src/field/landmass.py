"""Module for landmass such as continents or islands."""


class Landmass:
    """Continuous stretch of land surrounded by water.

    Attributes:
        num (int): Landmass number.
        cells (list[src.field.cell.Cell]): Cells that make up this landmass.
    """

    def __init__(self, num, cells):
        """Continuous stretch of land surrounded by water.

        Args:
            num (int): Landmass number.
            cells (list[src.field.cell.Cell]): Cells that make up this
                landmass.
        """
        self.num = num

        self.cells = cells
        for cell in self.cells:
            cell.landmass = self
