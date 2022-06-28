"""A module to create model updater functions for the PhysiCOOL black-box."""
from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import Dict, Union, Callable
from dataclasses import dataclass, field

import physicool.datatypes as dt
from physicool.config import ConfigFileParser

CellUpdaterFunction = Callable[[dt.CellParameters, Dict[str, float]], None]


def update_motility_values(cell_data: dt.CellParameters, new_values: Dict[str, float]):
    """
    Updates the numerical values for the Motility class.

    Parameters
    ----------
    cell_data:
        The cell data structure to be modified.
    new_values:
        The new values to be written to the motility section
        of the CellParameters class. Keys should be the same as those in the XML file,
        but it is not required to include all the keys.
    """
    if "speed" in new_values.keys():
        cell_data.motility.speed = new_values["speed"]
    if "persistence_time" in new_values.keys():
        cell_data.motility.persistence_time = new_values["persistence_time"]
    if "migration_bias" in new_values.keys():
        cell_data.motility.migration_bias = new_values["migration_bias"]


def update_mechanics_values(cell_data: dt.CellParameters, new_values: Dict[str, float]):
    """
    Updates the numerical values for the Mechanics class.

    Parameters
    ----------
    cell_data:
        The cell data structure to be modified.
    new_values:
        The new values to be written to the mechanics section
        of the CellParameters class. Keys should be the same as those in the XML file,
        but it is not required to include all the keys.
    """
    if "cell_cell_adhesion_strength" in new_values.keys():
        cell_data.mechanics.cell_cell_adhesion_strength = new_values["cell_cell_adhesion_strength"]
    if "cell_cell_repulsion_strength" in new_values.keys():
        cell_data.mechanics.cell_cell_repulsion_strength = new_values["cell_cell_repulsion_strength"]
    if "relative_maximum_adhesion_distance" in new_values.keys():
        cell_data.mechanics.relative_maximum_adhesion_distance = new_values["relative_maximum_adhesion_distance"]


@dataclass
class ParamsUpdater(ABC):
    config_path: Union[str, Path]
    parser: ConfigFileParser = field(init=False)

    def __post_init__(self):
        """Creates the ConfigFileParser instance to be accessed by the class."""
        self.parser = ConfigFileParser(path=self.config_path)

    @abstractclassmethod
    def update(self, new_values: Dict[str, float]) -> None:
        """Updates the XML file with the values passed as input."""
        pass


@dataclass
class CellUpdater(ParamsUpdater):
    updater_function: CellUpdaterFunction
    cell_definition_name: str = "default"

    def update(self, new_values: Dict[str, float]) -> None:
        """Updates the XML file with the values passed as input."""
        cell_data = self.parser.read_cell_data(name=self.cell_definition_name)
        self.updater_function(cell_data, new_values)
        self.parser.write_cell_params(cell_data=cell_data)


def update_substance_values(substance: dt.Substance, new_values: Dict[str, float]):
    """
    Updates the numerical values for a Substance class (microenvironment).

    Parameters
    ----------
    substance
        The substance data to be updated.
    new_values
        The new values to be written to the substance class. Keys should be the same
        as those in the XML file, but it is not required to include all the keys.
    """
    if "diffusion_coefficient" in new_values.keys():
        substance.diffusion_coefficient = new_values["diffusion_coefficient"]
    if "decay_rate" in new_values.keys():
        substance.decay_rate = new_values["decay_rate"]
    if "initial_condition" in new_values.keys():
        substance.initial_condition = new_values["initial_condition"]
    if "dirichlet_boundary_condition" in new_values.keys():
        substance.dirichlet_boundary_condition = new_values["dirichlet_boundary_condition"]


@dataclass
class MicroenvironmentUpdater(ParamsUpdater):
    substance_name: str

    def update(self, new_values: Dict[str, float]) -> None:
        """Updates the XML file with the values passed as input."""
        substances = self.parser.read_me_params()
        substance = [substance for substance in substances if substance.name == self.substance_name][0]
        update_substance_values(substance=substance, new_values=new_values)
        self.parser.write_substance_params(substance)
