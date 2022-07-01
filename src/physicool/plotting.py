from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def plot_trajectories_2d(trajectories: pd.DataFrame, ax: Optional[plt.Axes]):
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
        ax.plot(cell["position_x"].values,
                cell["position_y"].values)

        ax.scatter(cell["position_x"].values[-1],
                   cell["position_y"].values[-1], marker="o")

    return ax


def plot_trajectories_3d(trajectories: pd.DataFrame, ax: Optional[plt.Axes]):
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
        ax = fig.add_subplot(projection='3d')

    for cell in trajectories:
        ax.plot(cell["position_x"].values,
                cell["position_y"].values,
                cell["position_z"].values)

        ax.scatter(cell["position_x"].values[-1],
                   cell["position_y"].values[-1],
                   cell["position_z"].values[-1], marker="o")

    return ax
