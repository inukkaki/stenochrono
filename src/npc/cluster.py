"""Module for clusters of NPCs."""

from src.npc.exceptions import CellRegisteringException


class Cluster:
    """Cluster of NPCs that has a population of 1 or more.

    Attributes:
        cell (src.field.cell.Cell): Cell where this cluster exists. Two
            different clusters cannot exist in the same cell at the same time.
        popl (int): Population. If this value is 0 or less, this cluster will
            perish.
        alive (bool): Indicates if this group is alive.
    """

    def __init__(self, cell, popl):
        """Cluster of NPCs that has a population of 1 or more.

        Args:
            cell (src.field.cell.Cell): Cell where this cluster exists. Two
                different clusters cannot exist in the same cell at the same
                time.
            popl (int): Initial population.
        """
        if cell.register_cluster(self):
            self.cell = cell
        else:
            raise CellRegisteringException(
                "Another cluster is already registered by the cell.")

        self.popl = popl

        self.alive = True
