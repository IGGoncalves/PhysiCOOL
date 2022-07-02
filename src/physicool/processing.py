"""A module to process output PhysiCell files and extract metrics from the data."""
from pathlib import Path
from typing import Callable, Union, List
from xml.etree import ElementTree

import numpy as np
import pandas as pd
from scipy import io as sio

CELL_OUTPUT_LABELS = [
    "ID",
    "position_x",
    "position_y",
    "position_z",
    "total_volume",
    "cell_type",
    "cycle_model",
    "current_phase",
    "elapsed_time_in_phase",
    "nuclear_volume",
    "cytoplasmic_volume",
    "fluid_fraction",
    "calcified_fraction",
    "orientation_x",
    "orientation_y",
    "orientation_z",
    "polarity",
    "migration_speed",
    "motility_vector_x",
    "motility_vector_y",
    "motility_vector_z",
    "migration_bias",
    "motility_bias_direction_x",
    "motility_bias_direction_y",
    "motility_bias_direction_z",
    "persistence_time",
    "motility_reserved",
]


class Microenvironment:
    def __init__(self, time_point: int, path: Union[Path, str]):
        self.storage = path

        self.time = time_point
        self.substances = self.get_substances()
        self.mesh = self.get_mesh()
        self.mesh_shape = (len(self.mesh[1]), len(self.mesh[0]))

        self.data = self.get_data()

    def get_substances(self):
        """Returns a list of the substances stored in the XML output files."""

        # Open the first XML file to get list of stored substances
        tree = ElementTree.parse(self.storage / "output00000000.xml")
        root = tree.getroot()
        var_node = root.find("microenvironment/domain/variables")
        var_children = var_node.findall("variable")
        variables = [var.get("name") for var in var_children]

        return variables

    def get_mesh(self):
        """Returns a list with the coordinates of the microenvironment mesh."""

        # Open the first XML file to get list of stored substances
        tree = ElementTree.parse(self.storage / "output00000000.xml")
        root = tree.getroot()
        mesh_node = root.find("microenvironment/domain/mesh")

        # Get x, y and z coordinates
        # X coordinates
        coord_str = mesh_node.find("x_coordinates").text
        delimiter = mesh_node.find("x_coordinates").get("delimiter")
        x_coords = np.array(coord_str.split(delimiter), dtype=np.float)
        # Y coordinates
        coord_str = mesh_node.find("y_coordinates").text
        delimiter = mesh_node.find("y_coordinates").get("delimiter")
        y_coords = np.array(coord_str.split(delimiter), dtype=np.float)
        # Z coordinates
        coord_str = mesh_node.find("z_coordinates").text
        delimiter = mesh_node.find("z_coordinates").get("delimiter")
        z_coords = np.array(coord_str.split(delimiter), dtype=np.float)

        return [x_coords, y_coords, z_coords]

    def get_substance_data(self, substance):
        """Returns an array with the substance concentrations for all the planes of the domain."""

        timestep = str(self.time).zfill(8)

        me_file = self.storage / "output{}_microenvironment0.mat".format(timestep)

        # Load substance data
        me_data = sio.loadmat(me_file)["multiscale_microenvironment"]

        # Select the data corresponding to the chosen substance
        substance_index = self.substances.index(substance)
        substance_data = np.array(
            [
                np.reshape(
                    me_data[substance_index + 4, me_data[2, :] == z_level],
                    self.mesh_shape,
                )
                for z_level in self.mesh[2]
            ]
        )

        return substance_data

    def get_data(self):
        """Returns a dictionary with the data for all the substances in the simulation."""

        me_data = {
            substance: self.get_substance_data(substance)
            for substance in self.substances
        }

        return me_data


def read_mat_file_cells(path: str, variables: List[str]) -> pd.DataFrame:
    # Make sure that the variables can be found in the file
    if any([var not in CELL_OUTPUT_LABELS for var in variables]):
        raise ValueError("The passed variables are not valid names.")

    cell_data = sio.loadmat(path)["cells"]
    # Select and save the variables of interest
    variables_indexes = [CELL_OUTPUT_LABELS.index(var) for var in variables]
    cells = pd.DataFrame.from_dict(
        {var: cell_data[index, :] for var, index in zip(variables, variables_indexes)}
    )

    return cells


def get_cell_data(
    timestep: int, variables: List[str], output_path: Union[str, Path] = Path("output")
) -> pd.DataFrame:
    """
    Reads the PhysiCell output data into a Pandas DataFrame.

    Parameters
    ----------
    timestep
        The time point to be read.
    variables
        The variables to be extracted from the file.
    output_path
        The path to where the output files can be found.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the passed variables for every cell.
    """
    # Create path name
    if isinstance(output_path, str):
        output_path = Path(output_path)

    time_str = str(timestep).zfill(8)
    file_name = "output{}_cells_physicell.mat".format(time_str)
    path_name = output_path / file_name

    # Make sure that the timestep has been recorded and saved
    if path_name not in output_path.glob("output*_cells_physicell.mat"):
        raise ValueError("The passed time point does not match any file.")

    # Read output file into a DataFrame
    # (changing Path to a string with its absolute path. loadmat takes strings as input)
    cells = read_mat_file_cells(
        path=path_name.absolute().as_posix(), variables=variables
    )

    cells["timestep"] = timestep

    return cells


def get_cells_in_z_slice(data: pd.DataFrame, size: float) -> pd.DataFrame:
    """
    Returns the cells inside a z-axis slice and returns them.
    The slice will be centered at 0 and have the passed size.

    Parameters
    ----------
    data
        A DataFrame with the cells' coordinates
        (must contain a column called "position_z").
    size
        The size of the z-slice.

    Returns
    -------
    pd.DataFrame
        A DataFrame that only contains the cells inside the slice.
    """
    if "position_z" not in data.columns:
        raise ValueError("The DataFrame doesn't include the cells' z coordinates.")

    return data[
        (data["position_z"] >= -size / 2) & (data["position_z"] <= size / 2)
    ].copy()


def get_cell_trajectories(output_path: Union[str, Path]):
    """
    Reads the PhysiCell output data into a Pandas DataFrame.

    Parameters
    ----------
    output_path
        The path to where the output files can be found.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the passed variables for every cell.
    """
    # Create path name
    if isinstance(output_path, str):
        output_path = Path(output_path)

    variables = ["ID", "position_x", "position_y", "position_z"]
    data = []

    # Make sure that the timestep has been recorded and saved
    pattern = "output*_cells_physicell.mat"
    number_of_timepoints = len([file for file in output_path.glob(pattern)])

    for i in range(number_of_timepoints):
        cells = get_cell_data(timestep=i, variables=variables, output_path=output_path)
        cells["timestep"] = i
        data.append(cells)

    new_data = pd.concat(data)
    trajectories = [
        new_data[new_data["ID"] == cell_id][["position_x", "position_y", "position_z"]]
        for cell_id in new_data["ID"].unique()
    ]

    return trajectories


OutputProcessor = Callable[[Path], Union[float, np.ndarray]]


def get_cell_numbers_over_time(output_path: Path = Path("output")) -> np.ndarray:
    """
    Returns the number of cells over time (one value for each simulation time point).

    Parameters
    ----------
    output_path
        The path to where the output files can be found.

    Returns
    -------
    np.ndarray
        An array with the number of cells at every simulation time point.
    """
    if isinstance(output_path, str):
        output_path = Path(output_path)

    pattern = "output*_cells_physicell.mat"
    number_of_timepoints = len([file for file in output_path.glob(pattern)])
    number_of_cells = np.empty(shape=(number_of_timepoints,))

    for i in range(number_of_timepoints):
        cells = get_cell_data(timestep=i, variables=["ID"], output_path=output_path)
        number_of_cells[i] = cells["ID"].size

    return number_of_cells


def get_final_y_position(output_path: Path = Path("output")) -> np.ndarray:
    """
    Returns the number of cells over time (one value for each simulation time point).

    Parameters
    ----------
    output_path
        The path to where the output files can be found.

    Returns
    -------
    np.ndarray
        An array with the number of cells at every simulation time point.
    """
    if isinstance(output_path, str):
        output_path = Path(output_path)

    pattern = "output*_cells_physicell.mat"
    last_point = len([file for file in output_path.glob(pattern)])
    cells = get_cell_data(
        timestep=last_point - 1, variables=["position_y"], output_path=output_path
    )

    return cells["position_y"].values


ErrorQuantification = Callable[[np.ndarray, np.ndarray], float]


def compute_mean_squared_error(
    model_data: np.ndarray, reference_data: np.ndarray
) -> float:
    """Returns the mean squared error value between the reference and simulated datasets."""
    return ((model_data - reference_data) ** 2).sum()
