from pathlib import Path
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d

import config


def run_simulation(project):
    command = project
    subprocess.run(command, shell=True)


def get_timesteps(storage_path):
    """Returns the number of output XML files in the storage directory."""
    number_of_output_files = len(list(storage_path.glob('output*.xml')))
    timesteps = range(number_of_output_files)

    return timesteps


def read_output(storage_path, variables):
    cells_through_time = []
    timesteps = get_timesteps(storage_path)
    for timestep in timesteps:
        # Read the data saved at each time point
        cells = get_cell_data(timestep, storage_path, variables)
        number_of_cells = len(cells['ID'])

        # Store the data for each cell
        for i in range(number_of_cells):
            cells_data = [cells[variable][i] for variable in variables] + [timestep]
            cells_through_time.append(cells_data)

    variables = variables + ['time']

    cells_df = pd.DataFrame(cells_through_time, columns=variables)

    return cells_df


class OptModel:
    def __init__(self, metric, project='project',
                 config_path='config/PhysiCell_settings.xml', storage_path='output'):

        # TODO: check system platform
        self.project = f'./{project}'
        self.metric = metric
        self.storage_path = Path(storage_path)
        self.config_path = Path(config_path)
        self.variables = ['ID']

        # TODO: introduce other metrics
        if metric == 'position_y':
            self.variables.append('position_y')

    def model(self, params):
        update_config_file(params, self.config_path)
        run_simulation(self.project)
        cells = read_output(self.storage_path, self.variables)
        if self.metric == 'position_y':
            distances = compute_traveled_distances(cells)

        return distances

    def create_model(self):
        return self.model


def compute_error(model_data, reference_data):
    """Returns the summ of the squared differences between model and reference data."""
    error = ((model_data - reference_data) ** 2).sum()

    return error


class MultiSweep:
    def __init__(self, model, data, n_levels, npdir, ppdir):
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
        self.param_labels = ['x', 'y']
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
        self.y = np.linspace(min_limit, max_limit, self.npdir)

    def compute_objective(self):
        # Sweep through the parameter combinations
        for i, x_value in enumerate(self.x):
            for j, y_value in enumerate(self.y):
                # Select parameters and run the model
                self.parameters_in_sweep[self.param_labels[0]] = x_value
                self.parameters_in_sweep[self.param_labels[1]] = y_value
                N_model = self.model(self.parameters_in_sweep)

                # Compute error
                self.results[self.level][i][j] = compute_error(N_model, self.data)

    def get_new_params(self):
        I = np.argmin(self.results[self.level])
        x = int(np.floor(I / self.npdir))
        y = int(I - self.npdir * x)

        return self.x[x], self.y[y]

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
        width = max(self.x) - min(self.x)
        heigth = max(self.y) - min(self.y)

        p = Rectangle((min(self.x), min(self.y)), width, heigth,
                      edgecolor='black', facecolor='none', linestyle='--')
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=self.level, zdir='y')

    def get_colormap(self):
        color_dimension = self.results[0]
        maxx = color_dimension.max()
        minn = 0
        norm = colors.Normalize(minn, maxx)
        m = plt.cm.ScalarMappable(norm=norm, cmap='Spectral_r')
        return m

    def run_level(self, fig, ax):
        self.set_bounds()
        self.get_new_ax_lims()

        # Draw parameter bounds
        ax.set_ylim(0, self.n_levels)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_zlim(self.ylim[0], self.ylim[1])
        self.add_bounds_to_ax(ax)
        fig.canvas.draw()

        self.compute_objective()

        # Get the parameter space
        x, y = np.meshgrid(self.x, self.y)

        # Convert the error data to colormap
        m = self.get_colormap()
        color_dimension = self.results[self.level]  # change to desired fourth dimension
        m.set_array([])
        fcolors = m.to_rgba(color_dimension)

        # Plot surface using color as a 4th dimension
        ax.plot_surface(x, np.ones((len(self.x), len(self.y))) * self.level, y,
                        facecolors=fcolors, linewidth=0.1, rstride=1, cstride=1)

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
        ax = plt.axes(projection='3d')
        ax.view_init(elev=5., azim=75)

        ax.set_xlabel(self.param_labels[0], labelpad=5)
        ax.set_ylabel('Optimization level', labelpad=10)
        ax.set_zlabel(self.param_labels[1], labelpad=10)

        fig.show()
        fig.canvas.draw()

        while self.level < self.n_levels:
            self.run_level(fig, ax)
            self.level += 1

        return self.opt_point[0], self.opt_point[1]
