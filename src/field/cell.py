"""Modules for cells."""

import numpy as np


class Cell:
    """Hexagonal cell that composes a field.

    Attributes:
        row (int): Row number where this cell is located on the field.
        col (int): Column number where this cell is located on the field.
        pos (numpy.NDArray): Position of this cell.
        neighborhood (list[src.field.cell.Cell]): List of neighbor cells.
        elev (float): Elevation (m).
        stpn (float): Steepness. This value is calculated as the average
            elevation difference every 100 meters between neighbor cells.
        surface (int): State of this cell's surface.
        cluster (src.npc.cluster.Cluster): Cluster that exists in this cell.
    """
    SURFACE_SEA = 0
    SURFACE_LAND = 1

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

        self.neighborhood = []

        self.elev = 0.0  # Elevation (m)
        self.stpn = 0.0  # Steepness

        self.surface = Cell.SURFACE_SEA

        self.cluster = None

    def register_cluster(self, cluster):
        """Register that a cluster exists in this cell.

        Args:
            cluster (src.npc.cluster.Cluster): Cluster to register.

        Returns:
            out (bool): True unless another cluster is already registered;
                otherwise, False.
        """
        result = False
        if self.cluster is None:
            self.cluster = cluster
            result = True
        return result
