from typing import Callable, List
from dataclasses import dataclass

import physicool.datatypes as dt
from physicool.config import ConfigFileParser

UpdaterFunction = Callable[[dt.CellParameters, List[float]], None]


def update_motility_values(cell_data: dt.CellParameters, new_values=List[float]):
    cell_data.motility.speed = new_values[0]
    cell_data.motility.persistence_time = new_values[1]
    cell_data.motility.migration_bias = new_values[2]


def update_mechanics_values(cell_data: dt.CellParameters, new_values=List[float]):
    cell_data.mechanics.cell_cell_adhesion_strength = new_values[0]
    cell_data.mechanics.cell_cell_repulsion_strength = new_values[1]
    cell_data.mechanics.relative_maximum_adhesion_distance = new_values[2]


@dataclass
class ParamsUpdater:
    """A class to update the XML config file."""

    updater_function: UpdaterFunction
    parser: ConfigFileParser = field(init=False)

    def __post_init__(self):
        self.parser = ConfigFileParser()

    def update(
            self, new_values: List[float], cell_definition_name: str = "default"
    ) -> None:
        cell_data = self.parser.read_cell_data(cell_definition_name)
        self.updater_function(cell_data, new_values)
        self.parser.update_params(name=cell_definition_name, new_parameters=cell_data)