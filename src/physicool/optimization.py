"""A module for model calibration and optimization routines."""
from dataclasses import dataclass, field
from pathlib import Path
import platform
import subprocess
from typing import List, Dict, Optional, Tuple, Union
from distutils.dir_util import copy_tree, remove_tree

import numpy as np

from physicool.updaters import ParamsUpdater
from physicool.processing import (
    OutputProcessor,
    ErrorQuantification,
    compute_mean_squared_error,
    NEW_OUTPUTS_VERSION,
)
from physicool.plotting import SweeperPlot


def _create_project_command(project_name: str) -> str:
    """
    Creates a project command based on the current OS.

    Parameters
    -----------
    project_name:
        The base name of the PhysiCell executable file.

    Returns
    --------
    str
        The full command to be called in order to run the
        executable in the shell, adapted to the current OS.
    """
    if platform.system == "Windows":
        return f"{project_name}.exe"
    return f"./{project_name}"


def clean_outputs() -> None:
    """Removes the files from the output folder and creates it again (make data-cleanup)."""
    if Path("output").is_dir():
        remove_tree("output")
        Path("output").mkdir()


def clean_tmp_files() -> None:
    """Removes the temp folder if it exists."""
    if Path("temp").is_dir():
        remove_tree("temp")


def compile_project() -> None:
    """Compiles the current project by calling make."""
    subprocess.run("make", shell=True, stdout=None, stderr=None)


@dataclass
class PhysiCellBlackBox:
    """
    A class to run PhysiCell models through Python as a black box.
    Models can be run as they are, and it's possible to run replicates.

    Alternatively, users can decide to include a ParamsUpdater object to
    change values in the XML file before the model is run and/or a
    OutputProcessor to extract data from the output files and return a given
    user-defined metric.

    Output files can be kept or discarded. If kept, they will be stored
    inside a new "temp" folder.
    """

    updater: Optional[ParamsUpdater] = None
    processor: Optional[OutputProcessor] = None
    project_name: str = "project"
    project_command: str = field(init=False)
    version: str = NEW_OUTPUTS_VERSION

    def __post_init__(self):
        """Create the right command to call the PhysiCell project based on the OS."""
        self.project_command = _create_project_command(self.project_name)

    def run(
        self,
        params: Optional[Dict[str, float]] = None,
        number_of_replicates: int = 1,
        keep_files: bool = True,
    ) -> Optional[np.ndarray]:
        """
        Runs the black box pipeline.

        Parameters
        ----------
        params
            The new parameter values, to be updated in the XML file
            by the ParamsUpdater class.
        number_of_replicates
            The number of simulation replicates to be run.
        keep_files
            If the output files should be stored in a tmp folder.

        Returns
        -------
        Optional[np.ndarray]
            The output metrics computed by the OutputProcessor class
        """
        # Create a new directory to store the output files
        if keep_files:
            storage_folder = "temp"
            Path(storage_folder).mkdir()

        # Update the XML configuration file with the passed values
        if (self.updater is not None) and (params is not None):
            self.updater.update(new_values=params)

        # Create an array to store the metrics computed by the processor
        if self.processor:
            output_metrics = []

        # Run the PhysiCell model for each replicate
        # Create a new directory, run the model and save the files to this
        # location and compute and store the model output metrics
        for i in range(number_of_replicates):
            if (number_of_replicates > 1) & keep_files:
                storage_folder = f"temp/replicate{i}"
                Path(storage_folder).mkdir()

            subprocess.run(self.project_command, shell=True, stdout=subprocess.DEVNULL)

            if self.processor:
                output_metrics.append(self.processor(version=self.version))

            if keep_files:
                copy_tree("output", storage_folder)

        # Delete the files from the "output" folder
        clean_outputs()

        if self.processor:
            if number_of_replicates == 1:
                return output_metrics[0]

            return np.asarray(output_metrics)


def run_sweep(
    black_box: PhysiCellBlackBox, name: str, bounds: Tuple[float, float], step: float
) -> np.ndarray:
    input_values = np.arange(bounds[0], bounds[1], step)
    output_metrics = []
    for value in input_values:
        output_metrics.append(black_box.run({name: value}))

    return np.asarray(output_metrics)


@dataclass
class MultiLevelSweep:
    black_box: PhysiCellBlackBox
    target_data: np.ndarray
    n_levels: int
    points_dir: int
    percentage_dir: float
    parameters: List[str]
    error_estimator: ErrorQuantification = compute_mean_squared_error
    plotter: SweeperPlot = field(init=False)
    results: np.ndarray = field(init=False)
    current_level: int = field(init=False)
    current_opt_point: Tuple[float, float] = field(init=False)
    param_bounds: List[Tuple[Union[None, float], Union[None, float]]] = field(
        init=False
    )

    def __post_init__(self) -> None:
        """Sets up everything needed for the sweeper."""
        self.results = np.zeros((self.n_levels, self.points_dir, self.points_dir))
        self.current_level = 0
        self.current_opt_point = (0.0, 0.0)
        self.param_bounds = [(None, None), (None, None)]
        self.plotter = SweeperPlot()

    def set_param_bounds(
        self,
        param1_bounds: Optional[Tuple[Union[None, float], Union[None, float]]] = None,
        param2_bounds: Optional[Tuple[Union[None, float], Union[None, float]]] = None,
    ) -> None:
        """Defines the parameter bounds to be considered when creating a parameter space."""
        if param1_bounds is None:
            param1_bounds = (None, None)

        if param2_bounds is None:
            param2_bounds = (None, None)

        self.param_bounds = [param1_bounds, param2_bounds]

    def get_parameter_range(self, factor: float, idx: int) -> np.ndarray:
        """Returns the parameter values to be tested based on the current level and bounds."""
        min_limit = self.current_opt_point[idx] - factor * self.current_opt_point[idx]
        max_limit = self.current_opt_point[idx] + factor * self.current_opt_point[idx]

        if any(self.param_bounds[idx]):
            if self.param_bounds[idx][0] is not None:
                if min_limit < self.param_bounds[idx][0]:
                    min_limit = self.param_bounds[idx][0]

            if self.param_bounds[idx][1] is not None:
                if max_limit > self.param_bounds[idx][1]:
                    max_limit = self.param_bounds[idx][1]

        return np.linspace(min_limit, max_limit, self.points_dir)

    def get_parameter_space(self):
        """Returns the parameter values to be tested at the current level."""
        factor = self.percentage_dir / (self.current_level * 2 + 1)
        x = self.get_parameter_range(factor=factor, idx=0)
        y = self.get_parameter_range(factor=factor, idx=1)
        return x, y

    def get_optimal_idx(self) -> Tuple[int, int]:
        """Returns the indexes for the smallest error in the current level."""
        best_result = np.argmin(self.results[self.current_level])
        i = int(np.floor(best_result / self.points_dir))
        j = int(best_result - self.points_dir * i)

        return i, j

    def compute_objective(self, x: np.ndarray, y: np.ndarray) -> None:
        """
        Runs the black box for each cell of the parameter space defined by x and y.
        Also chooses the best optimal point found in the parameter space.
        """
        for i, x_value in enumerate(x):
            for j, y_value in enumerate(y):
                clean_tmp_files()
                # Select parameters and run the model
                results = self.black_box.run(
                    {self.parameters[0]: x_value, self.parameters[1]: y_value}
                )

                # Compute error between simulated data and target data
                self.results[self.current_level][i][j] = self.error_estimator(
                    results, self.target_data
                )

        i, j = self.get_optimal_idx()
        self.current_opt_point = (x[i], y[j])

    def run_level(self) -> None:
        """Run a single level of the multilevel sweep."""
        # Find the new parameter space for the current level
        x, y = self.get_parameter_space()
        # Add the bounds of the parameter space to the plot
        self.plotter.add_bounds_to_ax(x, y, self.current_level)

        # RUn the model for each cell of the parameter space and save the results
        self.compute_objective(x, y)
        # Plot the results as a heatmap
        self.plotter.plot_level_results(
            x, y, self.current_level, self.results[self.current_level]
        )

    def run_sweep(self, initial_point: Tuple[float, float]) -> Tuple[float, float]:
        """Runs all sweep levels from an initial value and returns the best values found."""
        self.current_opt_point = initial_point
        self.plotter.set_up_plotter(
            n_levels=self.n_levels, param_labels=self.parameters
        )

        while self.current_level < self.n_levels:
            self.run_level()
            self.current_level += 1

        return self.current_opt_point[0], self.current_opt_point[1]
