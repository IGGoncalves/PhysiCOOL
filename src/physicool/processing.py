from pathlib import Path
from typing import List, Dict

import numpy as np
import pandas as pd
from scipy import io as sio


def get_number_of_timepoints(storage_path: Path = Path("output/")) -> int:
    """Returns the number of output XML files in the storage directory."""
    return len(list(storage_path.glob('output*.xml')))


def get_cell_data(timepoint: int, variables: List[str],
                  output_path: Path = Path("output/")) -> Dict[str, np.ndarray]:
    """
    Returns a dictionary with the cell output data for the selected variables.

    Arguments
    ---------
    timepoint : int
        The time point at which the output was recorded
    output_path: Path
        The path to the folder where the output (.mat) files are stored
    variables : List[str]
        The variables to be extracted from the output files. If variables
        are not defined, all the available outputs will be saved.

    Returns
    -------
    cells: Dict[str, np.ndarray]
        A dictionary with the variable name and values for the passed variables.
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
    time_str = str(timepoint).zfill(8)
    file_name = 'output{}_cells_physicell.mat'.format(time_str)
    path_name = output_path / file_name

    # Read output file
    cell_data = sio.loadmat(path_name)['cells']

    # Select and save the variables of interest
    variables_indexes = [data_labels.index(var) for var in variables]
    cells = {var: cell_data[index, :]
             for var, index in zip(variables, variables_indexes)}

    return cells


def read_output(storage_path, variables):
    cells_through_time = []
    timesteps = get_number_of_timepoints(storage_path)
    for timestep in range(timesteps):
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


def compute_traveled_distances(cells_df):
    distance_traveled_by_cells = []

    # For each cell, compute the Euclidian distances between time points and get the total distance
    for cell_id in range(int(cells_df['ID'].max())):
        single_cell = cells_df[cells_df['ID'] == cell_id]
        y_distance = single_cell['position_y'].values

        distance_traveled_by_cells.append(y_distance)

    distance_traveled_by_cells = np.mean(np.array(distance_traveled_by_cells), axis=1)

    return distance_traveled_by_cells


def compute_error(self):
    """Returns the mean squared error value between the reference and simulated datasets."""
    return ((self.model_data - self.reference_data) ** 2).sum()
