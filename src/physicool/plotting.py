from typing import Optional, List
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d
import pandas as pd
import numpy as np


@dataclass
class SweeperPlot:
    fig: plt.Figure = field(init=False)
    ax: plt.Axes = field(init=False)

    def __post_init__(self):
        self.fig = plt.figure()
        self.ax = plt.axes(projection="3d")
        self.ax.view_init(elev=5.0, azim=75)

    def set_up_plotter(self, n_levels: int, param_labels: List[str]):
        """Defines the initial bounds and labels for the plotter."""
        self.ax.set_ylim(0, n_levels)
        self.ax.set_zlim(0, 5)
        self.ax.set_xlim(0, 1)
        self.ax.invert_xaxis()

        self.ax.set_zlabel(param_labels[0], labelpad=5)
        self.ax.set_ylabel("Optimization level", labelpad=10)
        self.ax.set_xlabel(param_labels[1], labelpad=10)

        self.fig.show()
        self.fig.canvas.draw()

    def draw(self):
        """Updates the figure."""
        self.fig.canvas.draw()

    def add_bounds_to_ax(self, x: np.ndarray, y: np.ndarray, z: int) -> None:
        """Draws the bounds for a level's parameter space."""
        width = max(y) - min(y)
        height = max(x) - min(x)

        p = Rectangle(
            (min(y), min(x)),
            width,
            height,
            edgecolor="black",
            facecolor="none",
            linestyle="--",
        )

        self.ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=z, zdir="y")
        self.draw()

    @staticmethod
    def get_colormap(level_values: np.ndarray) -> np.ndarray:
        """Convert the passed values to colormap."""
        color_dimension = level_values  # change to desired fourth dimension
        color_min, color_max = color_dimension.min(), color_dimension.max()
        norm = colors.Normalize(color_min, color_max)
        m = plt.cm.ScalarMappable(norm=norm, cmap="Spectral_r")
        m.set_array([])
        face_colors = m.to_rgba(color_dimension)

        return face_colors

    def plot_level_results(
        self, x: np.ndarray, y: np.ndarray, z: int, results: np.ndarray
    ) -> None:
        # Get the parameter space
        x, y = np.meshgrid(y, x)
        m = self.get_colormap(results)
        # Plot surface using color as a 4th dimension
        self.ax.plot_surface(
            x,
            np.ones((len(x), len(x))) * z,
            y,
            facecolors=m,
            edgecolor="white",
            linewidth=0.1,
            rstride=1,
            cstride=1,
        )

        self.fig.canvas.draw()


def plot_trajectories_2d(trajectories: pd.DataFrame, ax: Optional[plt.Axes] = None):
    """
    Plots the cell trajectories in 2D as a line and a point at the last coordinate.

    Parameters
    ----------
    trajectories
        A DataFrame with the cells' x and y coordinates.
    ax
      The axes object where the trajectories will be plotted (optional).
    """
    if ax is None:
        fig, ax = plt.subplots()

    for cell in trajectories:
        ax.plot(cell["position_x"].values, cell["position_y"].values)

        ax.scatter(
            cell["position_x"].values[-1], cell["position_y"].values[-1], marker="o"
        )

    return ax


def plot_trajectories_3d(trajectories: pd.DataFrame, ax: Optional[plt.Axes] = None):
    """
    Plots the cell trajectories in 3D as a line and a point at the last coordinate.

    Parameters
    ----------
    trajectories
        A DataFrame with the cells' x, y and z coordinates.
    ax
      The axes object where the trajectories will be plotted (optional).
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

    for cell in trajectories:
        ax.plot(
            cell["position_x"].values,
            cell["position_y"].values,
            cell["position_z"].values,
        )

        ax.scatter(
            cell["position_x"].values[-1],
            cell["position_y"].values[-1],
            cell["position_z"].values[-1],
            marker="o",
        )

    return ax
