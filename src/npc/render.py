"""Module for rendering NPCs."""

import matplotlib.cm as cm
import numpy as np
import pygame

from src.field.render import calc_cell_rect

RENDER_POPL_MAX = 250


def calc_popl_color(cluster):
    """Calculates the rendering color based on the population of a cluster.

    Args:
        cluster (src.npc.cluster.Cluster): Cluster to render.

    Returns:
        out (numpy.NDArray): Color vector (RGBA).
    """
    x = np.clip(cluster.popl, 0, RENDER_POPL_MAX)/RENDER_POPL_MAX
    color = 255.0*np.array(cm.viridis(x), dtype=np.float32)
    return color


def render_cluster(surface, cluster, color_func):
    """Renders a cluster on a surface.

    Args:
        surface (pygame.Surface): Surface for rendering the cluster.
        cluster (src.npc.cluster.Cluster): Cluster to render.
        color_func (Callable[src.npc.cluster.Cluster, numpy.NDArray]): Function
            to calculate the rendering color.
    """
    if not cluster.alive:
        return
    color = color_func(cluster)
    rect = calc_cell_rect(cluster.cell)
    pygame.draw.rect(surface, color, rect)
