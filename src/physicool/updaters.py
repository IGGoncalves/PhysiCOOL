"""A module to create model updater functions for the PhysiCOOL black-box."""
from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import Dict, Union, Callable
from dataclasses import dataclass, field

import physicool.datatypes as dt
from physicool.config import ConfigFileParser

CellUpdaterFunction = Callable[[dt.CellParameters, Dict[str, float]], None]


def update_cycle_values(cell_data: dt.CellParameters, new_values: Dict[str, float]):
    """
    Updates the numerical values for the Cycle class.

    Parameters
    ----------
    cell_data:
        The cell data structure to be modified.
    new_values:
        The new values to be written to the volume section
        of the CellParameters class. Keys should follow the pattern "phase_{i}"
        where i represents the id of the phase to be updated. All transition
        rates/durations must be specified.
    """
    if cell_data.cycle.phase_durations:
        if len(cell_data.cycle.phase_durations) != len(new_values):
            raise ValueError(
                "The passed values do not match the number of rates/durations."
            )

        cell_data.cycle.phase_durations = [
            new_values[f"phase_{i}"] for i, _ in enumerate(new_values)
        ]

    if cell_data.cycle.phase_transition_rates:
        if len(cell_data.cycle.phase_transition_rates) != len(new_values):
            raise ValueError(
                "The passed values do not match the number of rates/durations."
            )

        cell_data.cycle.phase_transition_rates = [
            new_values[f"phase_{i}"] for i, _ in enumerate(new_values)
        ]


def update_volume_values(cell_data: dt.CellParameters, new_values: Dict[str, float]):
    """
    Updates the numerical values for the Volume class.

    Parameters
    ----------
    cell_data:
        The cell data structure to be modified.
    new_values:
        The new values to be written to the volume section
        of the CellParameters class. Keys should be the same as those in the XML file,
        but it is not required to include all the keys.
    """
    if "total" in new_values.keys():
        cell_data.volume.total = new_values["total"]
    if "fluid_fraction" in new_values.keys():
        cell_data.volume.fluid_fraction = new_values["fluid_fraction"]
    if "nuclear" in new_values.keys():
        cell_data.volume.nuclear = new_values["nuclear"]
    if "fluid_change_rate" in new_values.keys():
        cell_data.volume.nuclear = new_values["fluid_change_rate"]
    if "cytoplasmic_biomass_change_rate" in new_values.keys():
        cell_data.volume.cytoplasmic_biomass_change_rate = new_values[
            "cytoplasmic_biomass_change_rate"
        ]
    if "nuclear_biomass_change_rate" in new_values.keys():
        cell_data.volume.nuclear_biomass_change_rate = new_values[
            "nuclear_biomass_change_rate"
        ]
    if "calcified_fraction" in new_values.keys():
        cell_data.volume.calcified_fraction = new_values["calcified_fraction"]
    if "calcification_rate" in new_values.keys():
        cell_data.volume.calcification_rate = new_values["calcification_rate"]
    if "relative_rupture_volume" in new_values.keys():
        cell_data.volume.relative_rupture_volume = new_values["relative_rupture_volume"]


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
        cell_data.mechanics.cell_cell_adhesion_strength = new_values[
            "cell_cell_adhesion_strength"
        ]
    if "cell_cell_repulsion_strength" in new_values.keys():
        cell_data.mechanics.cell_cell_repulsion_strength = new_values[
            "cell_cell_repulsion_strength"
        ]
    if "relative_maximum_adhesion_distance" in new_values.keys():
        cell_data.mechanics.relative_maximum_adhesion_distance = new_values[
            "relative_maximum_adhesion_distance"
        ]


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
        substance.dirichlet_boundary_condition = new_values[
            "dirichlet_boundary_condition"
        ]


@dataclass
class MicroenvironmentUpdater(ParamsUpdater):
    substance_name: str

    def update(self, new_values: Dict[str, float]) -> None:
        """Updates the XML file with the values passed as input."""
        substances = self.parser.read_me_params()
        substance = [
            substance
            for substance in substances
            if substance.name == self.substance_name
        ][0]
        update_substance_values(substance=substance, new_values=new_values)
        self.parser.write_substance_params(substance)
