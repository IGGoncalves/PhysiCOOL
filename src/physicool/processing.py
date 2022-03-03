from pathlib import Path
from typing import Callable, Union
from xml.etree import ElementTree
import numpy as np
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


class Cells:
    def __init__(self, time, storage_path):
        self.time = time
        self.storage = storage_path

    def get_cell_positions(self):
        """Returns a dictionary with the cell output data for the selected variables."""

        variables = ["position_x", "position_y", "position_z"]

        # Create path name
        time_str = str(self.time).zfill(8)
        file_name = "output{}_cells_physicell.mat".format(time_str)
        path_name = self.storage / file_name

        # Read output file
        cell_data = sio.loadmat(path_name)["cells"]

        # Select and save the variables of interest
        variables_indexes = [CELL_OUTPUT_LABELS.index(var) for var in variables]
        cells = {
            var: cell_data[index, :] for var, index in zip(variables, variables_indexes)
        }

        return [
            (x, y, z)
            for x, y, z in zip(
                cells["position_x"], cells["position_y"], cells["position_z"]
            )
        ]


def compute_error(model_data, reference_data):
    """Returns the mean squared error value between the reference and simulated datasets."""
    return ((model_data - reference_data) ** 2).sum()


OutputProcessor = Callable[[Path], Union[float, np.ndarray]]


def process_final_y_distance_data(storage_path: Path) -> np.ndarray:
    # Read the data saved at each time point
    coordinates = Cells(0, storage_path).get_cell_positions()
    y_component = [coordinate[1] for coordinate in coordinates]

    return np.array(y_component)
