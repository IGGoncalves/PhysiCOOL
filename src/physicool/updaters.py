"""A module to create model updater functions for the PhysiCOOL black-box."""
from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import List, Union, Callable
from dataclasses import dataclass, field

import physicool.datatypes as dt
from physicool.config import ConfigFileParser

CellUpdaterFunction = Callable[[dt.CellParameters, List[float]], None]


def update_motility_values(cell_data: dt.CellParameters, new_values=List[float]):
    cell_data.motility.speed = new_values[0]
    cell_data.motility.persistence_time = new_values[1]
    cell_data.motility.migration_bias = new_values[2]


def update_mechanics_values(cell_data: dt.CellParameters, new_values=List[float]):
    cell_data.mechanics.cell_cell_adhesion_strength = new_values[0]
    cell_data.mechanics.cell_cell_repulsion_strength = new_values[1]
    cell_data.mechanics.relative_maximum_adhesion_distance = new_values[2]


MicroenvironmentUpdaterFunction = Callable[[dt.Substance, List[float]], None]


@dataclass
class ParamsUpdater(ABC):
    """A class to update the XML config file."""
    config_path: Union[str, Path]
    parser: ConfigFileParser = field(init=False)

    def __post_init__(self):
        self.parser = ConfigFileParser(path=self.config_path)

    @abstractclassmethod
    def update(self, new_values: List[float]) -> None:
        pass


@dataclass
class CellUpdater(ParamsUpdater):
    updater_function: CellUpdaterFunction
    cell_definition_name: str = "default"

    def update(self, new_values: List[float]) -> None:
        cell_data = self.parser.read_cell_data(name=self.cell_definition_name)
        self.updater_function(cell_data, new_values)
        self.parser.write_cell_params(cell_data=cell_data)
