import numpy as np


class Cell:
    """Hexagonal cell that composes a field.

    Attributes:
        row (int): Row number where this cell is located on the field.
        col (int): Column number where this cell is located on the field.
        pos (numpy.NDArray): Position of this cell.
        elev (float): Elevation (m).
    """

    def __init__(self, row, col):
        """Hexagonal cell that composes a field.

        Args:
            row (int): Row number where this cell is located on the field.
            col (int): Column number where this cell is located on the field.
        """
        self.row = row
        self.col = col

        self.pos = np.array(
            [self.col + (self.row % 2)/2, self.row], dtype=np.float32)

        self.elev = 0.0  # Elevation (m)
