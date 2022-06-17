from abc import ABC, abstractclassmethod
from pathlib import Path
from sys import platform
import subprocess
from typing import List, Optional
from distutils.dir_util import copy_tree

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d

from physicool.config import ParamsUpdater
from physicool.processing import OutputProcessor, compute_error


class BlackBox(ABC):
    def __init__(
            self,
            project_name: str = "project",
            keep_files: bool = True
    ) -> None:
        # Define the paths where the PhysiCell files/folders can be found
        self.config_path = Path("config/PhysiCell_settings.xml")
        self.keep_files = keep_files

        # Define the command to be called to run the model based on the current OS
        if platform == "win32":
            self.project_command = f"{project_name}.exe"
        else:
            self.project_command = f"./{project_name}"

    @abstractclassmethod
    def run(self, number_of_replicates: int = 1) -> Optional[np.ndarray]:
        pass

    @staticmethod
    def _create_temp_folder():
        storage_folder = "temp"
        Path(storage_folder).mkdir(parents=True, exist_ok=True)

        return storage_folder

    @staticmethod
    def _create_replicate_folder(replicate: int):
        storage_folder = f"temp/replicate{replicate}"
        Path(storage_folder).mkdir(parents=True, exist_ok=True)

        return storage_folder

    @staticmethod
    def _copy_files_to_temp_folder(folder_name: str):
        copy_tree("output", folder_name)


class SimpleBlackBox(BlackBox):
    def run(self, number_of_replicates: int = 1) -> Optional[np.ndarray]:
        """
        Runs the black box pipeline: updates the config file,
        runs the model and retrieves the results.
        """
        if self.keep_files:
            storage_folder = self._create_temp_folder()

        for i in range(number_of_replicates):
            if self.keep_files & (number_of_replicates > 1):
                storage_folder = self._create_replicate_folder(replicate=i)
            # Run the PhysiCell simulation
            subprocess.run(self.project_command, shell=True)

            if self.keep_files:
                self._copy_files_to_temp_folder(storage_folder)

        return


class BlackBoxWithUpdater(BlackBox):
    def __init__(self, updater: Optional[ParamsUpdater] = None,
                 project_name: str = "project", keep_files: bool = True):
        self.updater = updater
        self.current_values = None
        super().__init__(project_name, keep_files)

    def run(self, number_of_replicates: int = 1) -> Optional[np.ndarray]:
        self.updater.write_params(new_values=self.current_values)
        self.updater.save_data()
        if self.keep_files:
            storage_folder = self._create_temp_folder()

        for i in range(number_of_replicates):
            if self.keep_files & (number_of_replicates > 1):
                storage_folder = self._create_replicate_folder(replicate=i)
            # Run the PhysiCell simulation
            subprocess.run(self.project_command, shell=True)

            if self.keep_files:
                self._copy_files_to_temp_folder(storage_folder)

        return

    def set_params(self, new_values: List[float]):
        self.current_values = new_values


class BlackBoxWithProcessor(BlackBox):
    def __init__(self, processor: Optional[OutputProcessor] = None,
                 project_name: str = "project", keep_files: bool = True):
        self.processor = processor
        super().__init__(project_name, keep_files)

    def run(self, number_of_replicates: int = 1) -> Optional[np.ndarray]:
        if self.keep_files:
            storage_folder = self._create_temp_folder()

        output_metrics = np.empty(shape=(number_of_replicates, 0))

        for i in range(number_of_replicates):
            if self.keep_files & (number_of_replicates > 1):
                storage_folder = self._create_replicate_folder(replicate=i)
            # Run the PhysiCell simulation
            subprocess.run(self.project_command, shell=True)
            output_metrics[i] = self.processor(Path("output"))

            if self.keep_files:
                self._copy_files_to_temp_folder(storage_folder)

        return output_metrics


class PhysiCellBlackBox:
    def __init__(
            self,
            updater: Optional[ParamsUpdater] = None,
            processor: Optional[OutputProcessor] = None,
            project_name: str = "project",
            keep_files: bool = True
    ) -> None:
        # Define the paths where the PhysiCell files/folders can be found
        self.config_path = Path("config/PhysiCell_settings.xml")
        self.keep_files = keep_files

        # Define the command to be called to run the model based on the current OS
        if platform == "win32":
            self.project_command = f"{project_name}.exe"
        else:
            self.project_command = f"./{project_name}"

        self.updater = updater
        self.processor = processor

    def run(self, params: Optional[List[float]] = None, number_of_replicates: int = 1):
        """
        Runs the black box pipeline: updates the config file, 
        runs the model and retrieves the results.
        """
        if self.keep_files:
            storage_folder = "temp"
            Path(storage_folder).mkdir(parents=True, exist_ok=True)

        if self.updater:
            self.updater.write_params(new_values=params)
            self.updater.save_data()

        if self.processor:
            x = np.empty(shape=(1,))

        for i in range(number_of_replicates):
            if (number_of_replicates > 1) & self.keep_files:
                storage_folder = f"temp/replicate{i}"
                Path(storage_folder).mkdir(parents=True, exist_ok=True)

            # Run the PhysiCell simulation
            subprocess.run(self.project_command, shell=True)

            if self.processor:
                return self.processor(Path("output"))

            if self.keep_files:
                copy_tree("output", storage_folder)


class MultiSweep:
    def __init__(self, model, data, n_levels: int, npdir: int, ppdir: int):
        """Initialized the multisweep class."""

        # Settings
        self.n_levels = n_levels
        self.npdir = npdir
        self.ppdir = ppdir
        self.model = model
        self.data = data

        # Storage
        self.results = np.zeros((n_levels, npdir, npdir))
        self.x = np.zeros((npdir, 1))
        self.y = np.zeros((npdir, 1))
        self.parameters_in_sweep = {}

        # Visualization
        self.xlim = [-1, 1]
        self.ylim = [-1, 1]

        self.level = 0
        self.opt_point = [0, 0]
        self.param_labels = ["x", "y"]
        self.param_bounds = [[None, None], [None, None]]

    def set_param_bounds(self, param1=None, param2=None):

        if param1 is None:
            param1 = [None, None]

        if param2 is None:
            param2 = [None, None]

        self.param_bounds = [param1, param2]

    def set_bounds(self):
        factor = self.ppdir / (self.level * 2 + 1)

        min_limit = self.opt_point[0] - factor * self.opt_point[0]
        max_limit = self.opt_point[0] + factor * self.opt_point[0]
        if any(self.param_bounds[0]):
            if self.param_bounds[0][0] is not None:
                if min_limit < self.param_bounds[0][0]:
                    min_limit = self.param_bounds[0][0]
            if self.param_bounds[0][1] is not None:
                if max_limit > self.param_bounds[0][1]:
                    max_limit = self.param_bounds[0][1]

        self.x = np.linspace(min_limit, max_limit, self.npdir)

        min_limit = self.opt_point[1] - factor * self.opt_point[1]
        max_limit = self.opt_point[1] + factor * self.opt_point[1]
        if any(self.param_bounds[1]):
            if self.param_bounds[1][0] is not None:
                if min_limit < self.param_bounds[1][0]:
                    min_limit = self.param_bounds[1][0]
            if self.param_bounds[1][1] is not None:
                if max_limit > self.param_bounds[1][1]:
                    max_limit = self.param_bounds[1][1]
        self.y = np.linspace(min_limit, max_limit, self.npdir)

    def compute_objective(self):
        # Sweep through the parameter combinations
        for i, x_value in enumerate(self.x):
            for j, y_value in enumerate(self.y):
                # Select parameters and run the model
                self.parameters_in_sweep[self.param_labels[0]] = x_value
                self.parameters_in_sweep[self.param_labels[1]] = y_value
                N_model = self.model.run([self.parameters_in_sweep["x"], self.parameters_in_sweep["y"]])

                # Compute error
                self.results[self.level][i][j] = compute_error(N_model, self.data)

    def get_new_params(self):
        I = np.argmin(self.results[self.level])
        i = int(np.floor(I / self.npdir))
        j = int(I - self.npdir * i)

        return self.x[i], self.y[j]

    def get_new_ax_lims(self):
        if self.level == 0:
            self.xlim[0] = min(self.x)
            self.xlim[1] = max(self.x)
            self.ylim[0] = min(self.y)
            self.ylim[1] = max(self.y)

        else:
            # Updtate ax xlims
            if min(self.x) < self.xlim[0]:
                self.xlim[0] = min(self.x)

            if max(self.x) > self.xlim[1]:
                self.xlim[1] = max(self.x)

            # Update ax zlims
            if min(self.y) < self.ylim[0]:
                self.ylim[0] = min(self.y)

            if max(self.y) > self.ylim[1]:
                self.ylim[1] = max(self.y)

    def add_bounds_to_ax(self, ax):
        width = max(self.y) - min(self.y)
        heigth = max(self.x) - min(self.x)

        p = Rectangle((min(self.y), min(self.x)), width, heigth,
                      edgecolor='black', facecolor='none', linestyle='--')
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=self.level, zdir="y")

    def get_colormap(self):
        color_dimension = self.results[0]
        maxx = color_dimension.max()
        minn = 0
        norm = colors.Normalize(minn, maxx)
        m = plt.cm.ScalarMappable(norm=norm, cmap="Spectral_r")
        return m

    def run_level(self, fig, ax):
        self.set_bounds()
        self.get_new_ax_lims()

        # Draw parameter bounds
        self.add_bounds_to_ax(ax)
        fig.canvas.draw()

        self.compute_objective()

        # Get the parameter space
        x, y = np.meshgrid(self.y, self.x)

        # Convert the error data to colormap
        color_dimension = self.results[self.level]  # change to desired fourth dimension
        minn, maxx = color_dimension.min(), color_dimension.max()
        norm = colors.Normalize(minn, maxx)
        m = plt.cm.ScalarMappable(norm=norm, cmap='Spectral_r')
        m.set_array([])
        fcolors = m.to_rgba(color_dimension)

        # Plot surface using color as a 4th dimension
        ax.plot_surface(x, np.ones((len(self.x), len(self.x))) * self.level, y,
                        facecolors=fcolors,
                        edgecolor='white', linewidth=0.1, rstride=1, cstride=1,
                        vmin=minn, vmax=maxx)

        fig.canvas.draw()

        if self.level == 0:
            fig.colorbar(m, shrink=0.6)

        param1, param2 = self.get_new_params()

        self.opt_point[0] = param1
        self.opt_point[1] = param2

    def set_fit_value(self, x, y):
        self.opt_point[0] = x
        self.opt_point[1] = y

    def select_params(self, label1, label2):
        self.param_labels[0] = label1
        self.param_labels[1] = label2

    def run_sweep(self):
        # Creating figure
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.view_init(elev=5.0, azim=75)
        ax.set_ylim(0, self.n_levels)
        ax.set_zlim(0, 5)
        ax.set_xlim(0, 1)
        ax.invert_xaxis()

        ax.set_xlabel(self.param_labels[0], labelpad=5)
        ax.set_ylabel("Optimization level", labelpad=10)
        ax.set_zlabel(self.param_labels[1], labelpad=10)

        fig.show()
        fig.canvas.draw()

        while self.level < self.n_levels:
            self.run_level(fig, ax)
            self.level += 1

        return self.opt_point[0], self.opt_point[1]
