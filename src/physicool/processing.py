import numpy as np


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