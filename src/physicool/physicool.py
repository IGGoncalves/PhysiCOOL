from xml.etree import ElementTree
from pathlib import Path
import subprocess
from scipy import io as sio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d

# To avoid having to write the full string for each XML element, I use this simple dict
# The goal is to only specify the name of the parameter (i.g., 'cell_cell_adhesion_strength')
# The get_xml_stem() function will take care of the rest using this dict
CELL_DEFINITIONS_DICT = {
    # TODO: What is the role of the "set relative/absolute" distances?
    # Should these parameters be included?
    'cycle': [
        'phase_transition_rates/rate'
    ],
    'mechanics': [
        'cell_cell_adhesion_strength',
        'cell_cell_repulsion_strength',
        'relative_maximum_adhesion_distance'
    ],
    # TODO: should the options be represented here?
    # For a parameter sweep, I don't think they are relevant because they are Booleans
    # or categorical values, and they change the cell behaviour significantly (2D vs 3D,...)
    'motility': [
        'speed',
        'persistence_time',
        'migration_bias'
    ]
}


def get_cell_xml_stem(key, definition_name='cancer'):
    """Returns the XML element name that corresponds to the passed parameter key."""
    for group, params in CELL_DEFINITIONS_DICT.items():
        if key in params:
            return f'cell_definitions/cell_definition[@name="{definition_name}"]/phenotype/{group}/{key}'


def get_me_xml_stem(key, substance='substrate'):
    """Returns the XML element name that corresponds to the passed parameter key."""
    return f'microenvironment_setup/variable[@name={substance}/{key}]'


def update_config_file(params_dict, config_path):
    """Updates configuration file with the specified input values."""
    tree = ElementTree.parse(config_path)

    for param, value in params_dict.items():
        param_type, key = param.split('/')
        # Expects the structure "cell/key}'
        if param_type == 'cell':
            param_name = get_cell_xml_stem(key)
        # Expects the structure "me/{substance}:{key}'
        elif param_type == 'me':
            substance, substance_key = key.split(':')
            param_name = get_me_xml_stem(substance_key, substance)
        else:
            param_name = f'custom_variables/{key}'

        tree.find(param_name).text = str(value)

    tree.write(config_path)


def get_cell_data(timestep, folder_name, variables='all'):
    """Returns a dictionary with the cell output data for the selected variables.

    Parameters
    ----------
    timestep : int
        The time point at which the output was recorded
    folder_name: Path
        The path to the folder where the output (.mat) files are stored
    variables : list
        The variables to be extracted from the output files. If variables
        are not defined, all the available outputs will be saved.
    """

    # All possible output variables written by PhysiCell
    data_labels = [
        'ID',
        'position_x', 'position_y', 'position_z',
        'total_volume',
        'cell_type',
        'cycle_model', 'current_phase', 'elapsed_time_in_phase',
        'nuclear_volume', 'cytoplasmic_volume',
        'fluid_fraction', 'calcified_fraction',
        'orientation_x', 'orientation_y', 'orientation_z',
        'polarity',
        'migration_speed',
        'motility_vector_x', 'motility_vector_y', 'motility_vector_z',
        'migration_bias',
        'motility_bias_direction_x', 'motility_bias_direction_y', 'motility_bias_direction_z',
        'persistence_time',
        'motility_reserved'
    ]

    # Create path name
    time_str = str(timestep).zfill(8)
    file_name = 'output{}_cells_physicell.mat'.format(time_str)
    path_name = folder_name / file_name

    # Read output file
    cell_data = sio.loadmat(path_name)['cells']

    # Select and save the variables of interest
    variables_indexes = [data_labels.index(var) for var in variables]
    cells = {var: cell_data[index, :]
             for var, index in zip(variables, variables_indexes)}

    return cells


def compute_traveled_distances(cells_df):
    distance_traveled_by_cells = []

    # For each cell, compute the Euclidian distances between time points and get the total distance
    for cell_id in range(int(cells_df['ID'].max())):
        single_cell = cells_df[cells_df['ID'] == cell_id]
        y_distance = single_cell['position_y'].values

        distance_traveled_by_cells.append(y_distance)

    distance_traveled_by_cells = np.mean(np.array(distance_traveled_by_cells), axis=1)

    return distance_traveled_by_cells


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
