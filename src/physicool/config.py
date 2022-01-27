# This module enables users to programmatically modify their PhysiCell XML config file
from pathlib import Path
from xml.etree import ElementTree
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


class PhysiCellConfigError(Exception):
    """
    A class of exceptions to deal with errors that do not fit the expected formatting for the
    PhysiCell XML configuration file.
    """
    pass


class NegativeValueError(PhysiCellConfigError):
    """
    An exception to be raised when a non-negative config parameter is given a negative value.

    Attributes
    ----------
    value: float
        The value that raised the exception
    parameter: str
        The parameter from the config file for which the exception was raised
    """

    def __init__(self, value: float, parameter: str) -> None:
        self.value = value
        self.parameter = parameter

    def __str__(self) -> str:
        """String representation of the exception, to be printed when exception is raised"""
        return f"Invalid value for {self.parameter}: {self.value}. Should be positive"


class RangeValueError(PhysiCellConfigError):
    """
    An exception to be raised when a config parameter is given a value that is not inside the fixed bounds.
    By default, the exception expects a range between 0 and 1, but other ranges can be used.

    Attributes
    ----------
    value: float
        The value that raised the exception
    parameter: str
        The parameter from the config file for which the exception was raised
    expected_range: (float, float)
        The range of values in which the invalid value should have been
    """

    def __init__(self, value: float, parameter: str, expected_range: Tuple[float, float] = (0.0, 1.0)) -> None:
        self.value = value
        self.parameter = parameter
        self.expected_range = expected_range

    def __str__(self):
        """String representation of the exception, to be printed when exception is raised"""
        return f"Invalid value for {self.parameter}: {self.value}.\n" \
               f"Should be between ({self.expected_range[0]}, {self.expected_range[1]})"


class InvalidCellDefinition(PhysiCellConfigError):
    """
    An exception to be raised when the user tries to extract data from a cell definition that does not match
    any of the definitions found in the XML file.

    Attributes
    ----------
    value: float
        The value that raised the exception
    valid_cell_definitions: [str]
        A list of the cell definitions found in the XML file
    """

    def __init__(self, value: str, valid_cell_definitions: List[str]):
        self.value = value
        self.valid_cell_definitions = valid_cell_definitions

    def __str__(self):
        """String representation of the exception, to be printed when exception is raised"""
        return f"Invalid cell definition: {self.value}. Choose a valid option: {self.valid_cell_definitions}"


@dataclass
class MechanicsParams:
    """Class that represents the cell mechanics parameters stored in the config file"""
    cell_cell_adhesion_strength: float
    cell_cell_repulsion_strength: float
    relative_maximum_adhesion_distance: float
    set_relative_equilibrium_distance: Optional[float] = None
    set_absolute_equilibrium_distance: Optional[float] = None

    _cell_cell_adhesion_strength: float = field(init=False, repr=False)
    _cell_cell_repulsion_strength: float = field(init=False, repr=False)
    _relative_maximum_adhesion_distance: float = field(init=False, repr=False)

    @property
    def cell_cell_adhesion_strength(self) -> float:
        """Returns the cell-cell adhesion value"""
        return self._cell_cell_adhesion_strength

    @cell_cell_adhesion_strength.setter
    def cell_cell_adhesion_strength(self, cell_cell_adhesion_strength: float) -> None:
        """Sets the cell-cell adhesion value, with validation"""
        if cell_cell_adhesion_strength < 0:
            raise NegativeValueError(cell_cell_adhesion_strength, "cell-cell adhesion")

        self._cell_cell_adhesion_strength = cell_cell_adhesion_strength

    @property
    def cell_cell_repulsion_strength(self) -> float:
        """Returns the cell-cell repulsion value"""
        return self._cell_cell_repulsion_strength

    @cell_cell_repulsion_strength.setter
    def cell_cell_repulsion_strength(self, cell_cell_repulsion_strength: float) -> None:
        """Sets the cell-cell repulsion value, with validation"""
        if cell_cell_repulsion_strength < 0:
            raise NegativeValueError(cell_cell_repulsion_strength, "cell-cell repulsion")

        self._cell_cell_repulsion_strength = cell_cell_repulsion_strength

    @property
    def relative_maximum_adhesion_distance(self) -> float:
        """Returns the relative maximum distance value"""
        return self._relative_maximum_adhesion_distance

    @relative_maximum_adhesion_distance.setter
    def relative_maximum_adhesion_distance(self, relative_maximum_adhesion_distance: float) -> None:
        """Sets the relative maximum distance value, with validation"""
        if relative_maximum_adhesion_distance < 0:
            raise NegativeValueError(relative_maximum_adhesion_distance, "cell-cell repulsion")

        self._relative_maximum_adhesion_distance = relative_maximum_adhesion_distance


@dataclass
class MotilityParams:
    speed: str
    persistence_time: str
    bias: str


@dataclass
class CellParameters:
    cell_type: str
    mechanics: MechanicsParams
    motility: MotilityParams


class ConfigFileParser:
    """A class that acts as an interface between the user and the XML config file"""

    def __init__(self, config_path: Path = Path("../config/PhysiCell_settings.xml")) -> None:
        self.config_file = config_path
        self.tree = ElementTree.parse(config_path)

    @property
    def cell_definitions_list(self) -> List[str]:
        """Returns a list with the names of the cell definitions in the XML file"""
        root = self.tree.getroot()
        cell_definitions = root.find('cell_definitions').findall('cell_definition')

        return [definition.attrib['name'] for definition in cell_definitions]

    @property
    def me_substances_list(self) -> List[str]:
        """Returns a list with the names of the substances in the XML file"""
        root = self.tree.getroot()
        substances = root.find('microenvironment/domain/variables').findall('variable')

        return [substance.attrib['name'] for substance in substances]

    def read_mechanics_params(self, cell_definition_key: str) -> MechanicsParams:
        """Reads the mechanics parameters from the config file into a custom data structure"""
        # Build basic string stem to find mechanics cell data for cell definition
        mech_string = cell_definition_key + "/phenotype/mechanics"

        # Extract and save the basic mechanics data from the config file
        adhesion = float(self.tree.find(mech_string + "/cell_cell_adhesion_strength").text)
        repulsion = float(self.tree.find(mech_string + "/cell_cell_repulsion_strength").text)
        adhesion_distance = float(self.tree.find(mech_string + "/relative_maximum_adhesion_distance").text)
        mech = MechanicsParams(adhesion, repulsion, adhesion_distance)

        # Extract and save the optional mechanics data, if it exists
        if self.tree.find(mech_string + "/options/set_relative_equilibrium_distance").attrib["enabled"] == "true":
            equilibrium_distance = self.tree.find(mech_string + "/options/set_relative_equilibrium_distance").text
            mech.set_relative_equilibrium_distance = float(equilibrium_distance)

        if self.tree.find(mech_string + "/options/set_absolute_equilibrium_distance").attrib["enabled"] == "true":
            absolute_distance = self.tree.find(mech_string + "/options/set_absolute_equilibrium_distance").text
            mech.set_absolute_equilibrium_distance = float(absolute_distance)

        return mech

    def read_motility_params(self, cell_definition_key: str) -> MotilityParams:
        """Reads the motility parameters from the config file into a custom data structure"""
        # Build basic string stem to find motility cell data for cell definition
        motility_string = cell_definition_key + "/phenotype/motility"

        # Extract and save the motility data from the config file
        speed = self.tree.find(motility_string + "/speed").text
        persistence_time = self.tree.find(motility_string + "/persistence_time").text
        bias = self.tree.find(motility_string + "/migration_bias").text
        motility = MotilityParams(speed, persistence_time, bias)

        return motility

    def read_cell_data(self, cell_definition_name: str = "default") -> CellParameters:
        """Reads all the fields for a given cell definition into a custom data type"""
        try:
            if cell_definition_name not in self.cell_definitions_list:
                raise InvalidCellDefinition(cell_definition_name, self.cell_definitions_list)

            # Read and save the cell data
            cell_string = f"cell_definitions/cell_definition[@name='{cell_definition_name}']"
            mechanics = self.read_mechanics_params(cell_string)
            motility = self.read_motility_params(cell_string)

            params = CellParameters(cell_definition_name, mechanics, motility)

            return params

        except InvalidCellDefinition:
            print(InvalidCellDefinition)
