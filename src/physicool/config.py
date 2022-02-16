# This module enables users to programmatically modify their PhysiCell XML config file
from pathlib import Path
from re import sub
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
    """
    A class that represents the cell mechanics parameters stored in the config file.
    """
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
    _speed: float = field(init=False, repr=False)
    _persistence_time: float = field(init=False, repr=False)
    _bias: float = field(init=False, repr=False)
    _motility_enabled: bool = field(init=False, repr=False)
    _use_2d: bool = field(init=False, repr=False)
    _chemotaxis_enabled: bool = field(init=False, repr=False)
    _chemotaxis_substrate: str = field(init=False, repr=False)
    _chemotaxis_direction: float = field(init=False, repr=False)

    @property
    def speed(self) -> float:
        """Returns the cell speed value."""
        return self._speed

    @speed.setter
    def speed(self, speed: float) -> None:
        """Sets the cell speed value, with validation."""
        if speed < 0.0:
            raise NegativeValueError(speed, "cell speed")

        self._speed = speed

    @property
    def persistence_time(self) -> float:
        """Returns the cell persistence time value."""
        return self._persistence_time

    @persistence_time.setter
    def persistence_time(self, persistence_time: float) -> None:
        """Sets the cell persistence time value, with validation."""
        if persistence_time < 0.0:
            raise NegativeValueError(persistence_time, "cell persistence time")

        self._persistence_time = persistence_time

    @property
    def bias(self) -> float:
        """Returns the cell motility bias value."""
        return self._bias

    @bias.setter
    def bias(self, bias: float) -> None:
        """Sets the cell motility bias value, with validation."""
        if bias < 0.0:
            raise RangeValueError(bias, "cell motility bias")

        self._bias = bias

    @property
    def motility_enabled(self) -> bool:
        """Returns the cell motility status."""
        return self._motility_enabled

    @motility_enabled.setter
    def motility_enabled(self, motility_enabled: bool) -> None:
        """Sets the cell motility status."""
        self._motility_enabled = motility_enabled

    @property
    def use_2d(self) -> bool:
        """Returns the cell motility 2D status."""
        return self._use_2d

    @use_2d.setter
    def use_2d(self, use_2d: bool) -> None:
        """Sets the cell motility 2D status."""
        self._use_2d = use_2d

    @property
    def chemotaxis_enabled(self) -> bool:
        """Returns the chemotaxis status."""
        return self._chemotaxis_enabled

    @chemotaxis_enabled.setter
    def chemotaxis_enabled(self, chemotaxis_enabled: bool) -> None:
        """Sets the chemotaxis status."""
        self._chemotaxis_enabled = chemotaxis_enabled

    @property
    def chemotaxis_substrate(self) -> str:
        """Returns the chemotaxis substance."""
        return self._chemotaxis_substrate

    @chemotaxis_substrate.setter
    def chemotaxis_substrate(self, chemotaxis_substrate: str) -> None:
        """Sets the chemotaxis substance."""
        self._chemotaxis_substrate = chemotaxis_substrate

    @property
    def chemotaxis_direction(self) -> float:
        """Returns the chemotaxis direction."""
        return self._chemotaxis_direction

    @chemotaxis_direction.setter
    def chemotaxis_direction(self, chemotaxis_direction: float) -> None:
        """Sets the chemotaxis direction."""
        self._chemotaxis_direction = chemotaxis_direction


@dataclass
class SecretionParams:
    """
    A class that represents the cell secretion parameters stored in the config file.
    """
    _secretion_rate: float = field(init=False, repr=False)
    _secretion_target: float = field(init=False, repr=False)
    _uptake_rate: float = field(init=False, repr=False)
    _net_export_rate: float = field(init=False, repr=False)

    @property
    def secretion_rate(self) -> float:
        """Returns the cell motility 2D status."""
        return self._secretion_rate

    @secretion_rate.setter
    def secretion_rate(self, secretion_rate: float) -> None:
        """Sets the cell motility 2D status."""
        if secretion_rate < 0.0:
            raise NegativeValueError(secretion_rate, "secretion rate")

        self._secretion_rate = secretion_rate

    @property
    def secretion_target(self) -> float:
        """Returns the cell motility 2D status."""
        return self._secretion_target

    @secretion_target.setter
    def secretion_target(self, secretion_target: float) -> None:
        """Sets the cell motility 2D status."""
        if secretion_target < 0.0:
            raise NegativeValueError(secretion_target, "secretion target")

        self._secretion_target = secretion_target

    @property
    def uptake_rate(self) -> float:
        """Returns the cell motility 2D status."""
        return self._uptake_rate

    @uptake_rate.setter
    def uptake_rate(self, uptake_rate: float) -> None:
        """Sets the cell motility 2D status."""
        if uptake_rate < 0.0:
            raise NegativeValueError(uptake_rate, "net export rate")

        self._uptake_rate = uptake_rate

    @property
    def net_export_rate(self) -> float:
        """Returns the cell motility 2D status."""
        return self._net_export_rate

    @net_export_rate.setter
    def net_export_rate(self, net_export_rate: float) -> None:
        """Sets the cell motility 2D status."""
        if net_export_rate < 0.0:
            raise NegativeValueError(net_export_rate, "net export rate")

        self._net_export_rate = net_export_rate


@dataclass
class CellParameters:
    cell_definition_name: str
    mechanics: Optional[MechanicsParams]
    motility: Optional[MechanicsParams]
    secretion: Optional[MechanicsParams]


class ConfigFileParser:
    """A class that acts as an interface between the user and the XML config file"""

    def __init__(self, config_path: Path = Path("config/PhysiCell_settings.xml")) -> None:
        self.config_file = config_path
        self.tree = ElementTree.parse(config_path)

    @property
    def cell_definitions_list(self) -> List[str]:
        """Returns a list with the names of the cell definitions in the XML file"""
        root = self.tree.getroot()
        cell_definitions = root.find('cell_definitions').findall('cell_definition')

        return [definition.attrib['name'] for definition in cell_definitions]

    @property
    def me_substance_list(self) -> List[str]:
        """Returns a list with the names of the substances in the XML file"""
        root = self.tree.getroot()
        substances = root.find('microenvironment/domain/variables').findall('variable')

        return [substance.attrib['name'] for substance in substances]

    def read_mechanics_params(self, cell_definition_name: str) -> MechanicsParams:
        """Reads the mechanics parameters from the config file into a custom data structure"""
        # Build basic string stem to find mechanics cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{cell_definition_name}']"
        mech_string = cell_string + "/phenotype/mechanics"

        mech = MechanicsParams()

        # Extract and save the basic mechanics data from the config file
        mech.cell_cell_adhesion_strength = float(self.tree.find(mech_string + "/cell_cell_adhesion_strength").text)
        mech.cell_cell_repulsion_strength = float(self.tree.find(mech_string + "/cell_cell_repulsion_strength").text)
        mech.relative_maximum_adhesion_distance = float(self.tree.find(mech_string + "/relative_maximum_adhesion_distance").text)

        # TODO: Extract and save the optional mechanics data, if it exists
        # if self.tree.find(mech_string + "/options/set_relative_equilibrium_distance").attrib["enabled"] == "true":
        #    equilibrium_distance = self.tree.find(mech_string + "/options/set_relative_equilibrium_distance").text
        #    mech.set_relative_equilibrium_distance = float(equilibrium_distance)

        # if self.tree.find(mech_string + "/options/set_absolute_equilibrium_distance").attrib["enabled"] == "true":
        #    absolute_distance = self.tree.find(mech_string + "/options/set_absolute_equilibrium_distance").text
        #    mech.set_absolute_equilibrium_distance = float(absolute_distance)

        return mech

    def read_motility_params(self, cell_definition_name: str) -> MotilityParams:
        """Reads the motility parameters from the config file into a custom data structure"""
        # Build basic string stem to find motility cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{cell_definition_name}']"
        motility_string = cell_string + "/phenotype/motility"

        motility = MotilityParams()

        # Extract and save the motility data from the config file
        motility.speed = float(self.tree.find(motility_string + "/speed").text)
        motility.persistence_time = float(self.tree.find(motility_string + "/persistence_time").text)
        motility.bias = float(self.tree.find(motility_string + "/migration_bias").text)

        motility.motility_enabled = self.tree.find(motility_string + "/options/enabled").text == "true"
        motility.use_2d = self.tree.find(motility_string + "/options/use_2D").text == "true"

        motility.chemotaxis_enabled = self.tree.find(motility_string + "/options/chemotaxis/enabled").text == "true"
        motility.chemotaxis_substrate = self.tree.find(motility_string + "/options/chemotaxis/substrate").text
        motility.chemotaxis_direction = float(self.tree.find(motility_string + "/options/chemotaxis/direction").text)

        return motility

    def read_secretion_params(self, cell_definition_name: str, substrate_name: str) -> SecretionParams:
        """Reads the motility parameters from the config file into a custom data structure"""
        # Build basic string stem to find secretion cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{cell_definition_name}']"
        secretion_string = cell_string + f"/phenotype/secretion/substrate[@name='{substrate_name}']"

        secretion = SecretionParams()

        # Extract and save the motility data from the config file
        secretion.secretion_rate = float(self.tree.find(secretion_string + "/secretion_rate").text)
        secretion.secretion_target = float(self.tree.find(secretion_string + "/secretion_target").text)
        secretion.uptake_rate = float(self.tree.find(secretion_string + "/uptake_rate").text)
        secretion.net_export_rate = float(self.tree.find(secretion_string + "/net_export_rate").text)

        return secretion

    def read_cell_data(self, cell_definition_name: str = "default", substrate_name: str = "substrate") -> CellParameters:
        """Reads all the fields for a given cell definition into a custom data type"""
        try:
            if cell_definition_name not in self.cell_definitions_list:
                raise InvalidCellDefinition(cell_definition_name, self.cell_definitions_list)

            # Read and save the cell data
            mechanics = self.read_mechanics_params(cell_definition_name)
            motility = self.read_motility_params(cell_definition_name)
            secretion = self.read_secretion_params(cell_definition_name, substrate_name)

            return CellParameters(cell_definition_name, mechanics, motility, secretion)

        except InvalidCellDefinition:
            print(InvalidCellDefinition)

    def read_user_params_data(self):
        params = self.tree.find("user_parameters").getchildren()
        user_params = {}

        for parameter in params:
            value = parameter.text
            name = parameter.tag

            user_params[name] = value

        return user_params

    def write_motility_params(self, cell_definition_name: str, motility: MotilityParams) -> None:
        cell_string = f"cell_definitions/cell_definition[@name='{cell_definition_name}']"
        motility_string = cell_string + "/phenotype/motility"

        # Extract and save the motility data from the config file
        self.tree.find(motility_string + "/speed").text = str(motility.speed)
        self.tree.find(motility_string + "/persistence_time").text = str(motility.persistence_time)
        self.tree.find(motility_string + "/migration_bias").text = str(motility.bias)

        self.tree.find(motility_string + "/options/enabled").text = "true" if motility.motility_enabled else "false"
        self.tree.find(motility_string + "/options/use_2D").text = "true" if motility.use_2d else "false"

        self.tree.find(motility_string + "/options/chemotaxis/enabled").text = "true" if motility.chemotaxis_enabled else "false"
        self.tree.find(motility_string + "/options/chemotaxis/substrate").text = motility.chemotaxis_substrate
        self.tree.find(motility_string + "/options/chemotaxis/direction").text = str(motility.chemotaxis_direction)

    def update_params(self, cell_definition_name, new_parameters: CellParameters) -> None:
        self.write_motility_params(cell_definition_name, new_parameters.motility)
        
        self.tree.write(self.config_file)
