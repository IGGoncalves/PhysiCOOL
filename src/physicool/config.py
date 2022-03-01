# This module enables users to programmatically modify their PhysiCell XML config file
from pathlib import Path
from re import sub
from xml.etree import ElementTree
from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class VolumeParams:
    """A class that represents the cell volume parameters stored in the config file."""

    @property
    def total_volume(self) -> float:
        """
        Returns the total volume value.
        Raises a ValueError if the passed value is negative.
        """
        return self._total_volume

    @total_volume.setter
    def total_volume(self, total_volume: float) -> None:
        if total_volume < 0:
            raise ValueError("Total volume should be positve.")

        self._total_volume = total_volume

    @property
    def fluid_fraction(self) -> float:
        """
        Returns the fluid fraction value.
        Raises a ValueError if the passed value is not between 0 and 1.
        """
        return self._fluid_fraction

    @fluid_fraction.setter
    def fluid_fraction(self, fluid_fraction: float) -> None:
        if fluid_fraction < 0.0 or fluid_fraction > 1.0:
            raise ValueError("Fluid fraction should be between 0 and 1.")

        self._fluid_fraction = fluid_fraction

    @property
    def nuclear(self) -> float:
        """
        Returns the nuclear voulme value.
        Raises a ValueError if the passed value is negative.
        """
        return self._nuclear

    @nuclear.setter
    def nuclear(self, nuclear: float) -> None:
        if nuclear < 0:
            raise ValueError("Cell nuclear volume should be positive.")

        self._nuclear = nuclear

    @property
    def fluid_change_rate(self) -> float:
        """
        Returns the fluid change rate value.
        Raises a ValueError if the passed value is negative.
        """
        return self._fluid_change_rate

    @fluid_change_rate.setter
    def fluid_change_rate(self, fluid_change_rate: float) -> None:
        if fluid_change_rate < 0:
            raise ValueError("Fluid change rate should be positive.")

        self._fluid_change_rate = fluid_change_rate

    @property
    def cyto_bio_rate(self) -> float:
        """
        Returns the cytoplasmic biomass change rate value.
        Raises a ValueError if the passed value is negative.
        """
        return self._cyto_bio_rate

    @cyto_bio_rate.setter
    def cyto_bio_rate(self, cyto_bio_rate: float) -> None:
        if cyto_bio_rate < 0:
            raise ValueError("Cytoplasmic biomass change rate should be positive.")

        self._cyto_bio_rate = cyto_bio_rate

    @property
    def nuclear_bio_rate(self) -> float:
        """
        Returns the nuclear biomass change rate value.
        Raises a ValueError if the passed value is negative.
        """
        return self._nuclear_bio_rate

    @nuclear_bio_rate.setter
    def nuclear_bio_rate(self, nuclear_bio_rate: float) -> None:
        if nuclear_bio_rate < 0:
            raise ValueError("Nuclear biomass change rate should be positive.")

        self._nuclear_bio_rate = nuclear_bio_rate

    @property
    def calcified_fraction(self) -> float:
        """
        Returns the calcified fraction value.
        Raises a ValueError if the passed value is negative.
        """
        return self._calcified_fraction

    @calcified_fraction.setter
    def calcified_fraction(self, calcified_fraction: float) -> None:
        if calcified_fraction < 0.0 or calcified_fraction > 1.0:
            raise ValueError("Calcified fraction should be betwween 0 and 1.")

        self._calcified_fraction = calcified_fraction

    @property
    def calcification_rate(self) -> float:
        """
        Returns the calcification rate value.
        Raises a ValueError if the passed value is negative.
        """
        return self._calcification_rate

    @calcification_rate.setter
    def calcification_rate(self, calcification_rate: float) -> None:
        if calcification_rate < 0:
            raise ValueError("Calcification rate should be positive.")

        self._calcification_rate = calcification_rate

    @property
    def rupture_volume(self) -> float:
        """
        Returns the relative rupture voulme value.
        Raises a ValueError if the passed value is negative.
        """
        return self._rupture_volume

    @rupture_volume.setter
    def rupture_volume(self, rupture_volume: float) -> None:
        if rupture_volume < 0:
            raise ValueError("Relative rupture volume shoulde be positive.")

        self._rupture_volume = rupture_volume


@dataclass
class MechanicsParams:
    """A class that represents the cell mechanics parameters stored in the config file."""

    @property
    def adhesion_strength(self) -> float:
        """
        Returns the cell-cell adhesion value.
        """
        return self._adhesion_strength

    @adhesion_strength.setter
    def adhesion_strength(self, adhesion_strength: float) -> None:
        if adhesion_strength < 0:
            raise ValueError("Cell-cell adhesion should be positive.")

        self._adhesion_strength = adhesion_strength

    @property
    def repulsion_strength(self) -> float:
        """Returns the cell-cell repulsion value"""
        return self._repulsion_strength

    @repulsion_strength.setter
    def repulsion_strength(self, repulsion_strength: float) -> None:
        """Sets the cell-cell repulsion value, with validation"""
        if repulsion_strength < 0:
            raise ValueError("Cell-cell repulsion should be positive.")

        self._repulsion_strength = repulsion_strength

    @property
    def adhesion_distance(self) -> float:
        """Returns the relative maximum distance value"""
        return self._adhesion_distance

    @adhesion_distance.setter
    def adhesion_distance(self, adhesion_distance: float) -> None:
        """Sets the relative maximum distance value, with validation"""
        if adhesion_distance < 0:
            raise ValueError("Adhesion distance should be positive.")

        self._adhesion_distance = adhesion_distance


@dataclass
class MotilityParams:
    """A class that represents the cell motility parameters stored in the config file."""
    
    @property
    def speed(self) -> float:
        """Returns the cell speed value."""
        return self._speed

    @speed.setter
    def speed(self, speed: float) -> None:
        """Sets the cell speed value, with validation."""
        if speed < 0.0:
            raise ValueError("Speed should be positive.")

        self._speed = speed

    @property
    def persistence(self) -> float:
        """Returns the cell persistence time value."""
        return self._persistence

    @persistence.setter
    def persistence(self, persistence: float) -> None:
        """Sets the cell persistence time value, with validation."""
        if persistence < 0.0:
            raise ValueError("Persistence time should be positive.")

        self._persistence = persistence

    @property
    def bias(self) -> float:
        """Returns the cell motility bias value."""
        return self._bias

    @bias.setter
    def bias(self, bias: float) -> None:
        """Sets the cell motility bias value, with validation."""
        if bias < 0.0 or bias > 1.0:
            raise ValueError("Motility bias should be between 0 and 1.")

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
    def chemo_enabled(self) -> bool:
        """Returns the chemotaxis status."""
        return self._chemo_enabled

    @chemo_enabled.setter
    def chemo_enabled(self, chemo_enabled: bool) -> None:
        """Sets the chemotaxis status."""
        self._chemo_enabled = chemo_enabled

    @property
    def chemo_substrate(self) -> str:
        """Returns the chemotaxis substance."""
        return self._chemo_substrate

    @chemo_substrate.setter
    def chemo_substrate(self, chemo_substrate: str) -> None:
        """Sets the chemotaxis substance."""
        self._chemo_substrate = chemo_substrate

    @property
    def chemo_direction(self) -> float:
        """Returns the chemotaxis direction."""
        return self._chemo_direction

    @chemo_direction.setter
    def chemo_direction(self, chemo_direction: float) -> None:
        """Sets the chemotaxis direction."""
        self._chemo_direction = chemo_direction

    def print(self):
        print(f"Speed: {self.speed}")
        print(f"Persistence time: {self.persistence}")
        print(f"Motility bias: {self.bias}")
        print(f"Motility enabled: {self.motility_enabled}")
        print(f"2D motility: {self.use_2d}")
        print(f"Chemotaxis enabled: {self.chemo_enabled}")
        print(f"Chemotaxis substance: {self.chemo_substrate}")
        print(f"Chemotaxis direction: {self.chemo_direction}")

@dataclass
class SecretionParams:
    """A class that represents the cell secretion parameters stored in the config file."""
    # TODO: Add a substance name parameter

    @property
    def secretion_rate(self) -> float:
        """
        Returns the value of the secretion rate. Setting a new value will raise a
        ValueError if a negative number is passed.
        """
        return self._secretion_rate

    @secretion_rate.setter
    def secretion_rate(self, secretion_rate: float) -> None:
        if secretion_rate < 0.0:
            raise ValueError(secretion_rate, "secretion rate")

        self._secretion_rate = secretion_rate

    @property
    def secretion_target(self) -> float:
        """
        Returns the value of the secretion target Setting a new value will raise a
        ValueError if a negative number is passed.
        """
        return self._secretion_target

    @secretion_target.setter
    def secretion_target(self, secretion_target: float) -> None:
        if secretion_target < 0.0:
            raise ValueError(secretion_target, "secretion target")

        self._secretion_target = secretion_target

    @property
    def uptake_rate(self) -> float:
        """
        Returns the value of the uptake rate. Setting a new value will raise a
        ValueError if a negative number is passed.
        """
        return self._uptake_rate

    @uptake_rate.setter
    def uptake_rate(self, uptake_rate: float) -> None:
        if uptake_rate < 0.0:
            raise ValueError(uptake_rate, "net export rate")

        self._uptake_rate = uptake_rate

    @property
    def net_export_rate(self) -> float:
        """
        Returns the value of the net export rate. Setting a new value will raise a
        ValueError if a negative number is passed.
        """
        return self._net_export_rate

    @net_export_rate.setter
    def net_export_rate(self, net_export_rate: float) -> None:
        if net_export_rate < 0.0:
            raise ValueError(net_export_rate, "net export rate")

        self._net_export_rate = net_export_rate


@dataclass
class CellParameters:
    """A class to store the cell data for a given cell definition of the config file."""
    name: str
    volume: Optional[VolumeParams] = None
    mechanics: Optional[MechanicsParams] = None
    motility: Optional[MotilityParams] = None
    # TODO: turn the secretion params into a list of objects for multiple susbtrates
    secretion: Optional[SecretionParams] = None

    def print(self):
        print(f"Cell definition name: {self.name}")
        print("-----------------------------")
        print("Motility data:")
        self.motility.print()


class ConfigFileParser:
    """A class that acts as an interface between the user and the XML config file"""

    def __init__(self, path: Path = Path("config/PhysiCell_settings.xml")) -> None:
        self.config_file = path
        self.tree = ElementTree.parse(path)

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

    def read_volume_params(self, name: str) -> VolumeParams:
        """Reads the motility parameters from the config file into a custom data structure"""
        # Build basic string stem to find motility cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + "/phenotype/volume"

        volume = VolumeParams()

        # Extract and save the volume data from the config file
        volume.total_volume = float(self.tree.find(stem + "/total").text)
        volume.fluid_fraction = float(self.tree.find(stem + "/fluid_fraction").text)
        volume.nuclear = float(self.tree.find(stem + "/nuclear").text)
        volume.fluid_change_rate = float(self.tree.find(stem + "/fluid_change_rate").text)
        volume.cyto_bio_rate = float(self.tree.find(stem + "/cytoplasmic_biomass_change_rate").text)
        volume.nuclear_bio_rate = float(self.tree.find(stem + "/nuclear_biomass_change_rate").text)
        volume.calcified_fraction = float(self.tree.find(stem + "/calcified_fraction").text)
        volume.calcification_rate = float(self.tree.find(stem + "/calcification_rate").text)
        volume.rupture_volume = float(self.tree.find(stem + "/relative_rupture_volume").text)

        return volume

    def read_mechanics_params(self, name: str) -> MechanicsParams:
        """Reads the mechanics parameters from the config file into a custom data structure"""
        # Build basic string stem to find mechanics cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + "/phenotype/mechanics"

        mech = MechanicsParams()

        # Extract and save the basic mechanics data from the config file
        mech.adhesion_strength = float(self.tree.find(stem + "/cell_cell_adhesion_strength").text)
        mech.repulsion_strength = float(self.tree.find(stem + "/cell_cell_repulsion_strength").text)
        mech.adhesion_distance = float(self.tree.find(stem + "/relative_maximum_adhesion_distance").text)

        # TODO: Extract and save the optional mechanics data, if it exists
        # if self.tree.find(stem + "/options/set_relative_equilibrium_distance").attrib["enabled"] == "true":
        #    equilibrium_distance = self.tree.find(stem + "/options/set_relative_equilibrium_distance").text
        #    mech.set_relative_equilibrium_distance = float(equilibrium_distance)

        # if self.tree.find(stem + "/options/set_absolute_equilibrium_distance").attrib["enabled"] == "true":
        #    absolute_distance = self.tree.find(stem + "/options/set_absolute_equilibrium_distance").text
        #    mech.set_absolute_equilibrium_distance = float(absolute_distance)

        return mech

    def read_motility_params(self, name: str) -> MotilityParams:
        """Reads the motility parameters from the config file into a custom data structure"""
        # Build basic string stem to find motility cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + "/phenotype/motility"

        motility = MotilityParams()

        # Extract and save the motility data from the config file
        motility.speed = float(self.tree.find(stem + "/speed").text)
        motility.persistence = float(self.tree.find(stem + "/persistence_time").text)
        motility.bias = float(self.tree.find(stem + "/migration_bias").text)

        motility.motility_enabled = self.tree.find(stem + "/options/enabled").text == "true"
        motility.use_2d = self.tree.find(stem + "/options/use_2D").text == "true"

        motility.chemo_enabled = self.tree.find(stem + "/options/chemotaxis/enabled").text == "true"
        motility.chemo_substrate = self.tree.find(stem + "/options/chemotaxis/substrate").text
        motility.chemo_direction = float(self.tree.find(stem + "/options/chemotaxis/direction").text)

        return motility

    def read_secretion_params(self, name: str) -> SecretionParams:
        """Reads the secretion parameters from the config file into a custom data structure"""
        # Build basic string stem to find secretion cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + f"/phenotype/secretion"

        substrates = [substrate.attrib["name"]
                      for substrate in self.tree.find(stem).findall("substrate")]

        for substrate in substrates:
            secretion = SecretionParams()
            substrate_stem = stem + f"/substrate[@name='{substrate}']"

            # Extract and save the motility data from the config file
            secretion.secretion_rate = float(self.tree.find(substrate_stem + "/secretion_rate").text)
            secretion.secretion_target = float(self.tree.find(substrate_stem + "/secretion_target").text)
            secretion.uptake_rate = float(self.tree.find(substrate_stem + "/uptake_rate").text)
            secretion.net_export_rate = float(self.tree.find(substrate_stem + "/net_export_rate").text)

        return secretion

    def read_cell_data(self, name: str = "default") -> CellParameters:
        """
        Reads all the fields for a given cell definition into a custom cell data type.
        
        Parameters
        ----------
        name: str, default "default"
            The name of the cell definition to be read
        substrate: str, default "substrate"
            The name of the substrate to be read.

        Returns
        -------
        CellParameters
            A custom cell data type that contains all the parameters of a cell definiton

        Raises
        ------
        ValueError
            If the input cell definition is not defined in the config file.
        """
        try:
            if name not in self.cell_definitions_list:
                raise ValueError("Invalid cell definition")

            # Read and save the cell data
            volume = self.read_volume_params(name)
            mechanics = self.read_mechanics_params(name)
            motility = self.read_motility_params(name)
            secretion = self.read_secretion_params(name)

            return CellParameters(name, volume, mechanics, motility, secretion)

        except ValueError as ve:
            print(ve)

    def read_user_params_data(self):
        params = self.tree.find("user_parameters").getchildren()
        user_params = {}

        for parameter in params:
            value = parameter.text
            name = parameter.tag

            user_params[name] = value

        return user_params

    def write_motility_params(self, name: str, motility: MotilityParams) -> None:
        """
        Writes the new motility parameter values to the XML tree object, for a given cell definition.
        Values will not be updated in the XML file.

        Parameters
        ----------
        name: str
            The name of the cell definition to be updated.
        motility: MotilityParams
            The new parameter values to be written to the XML object.
        """
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + "/phenotype/motility"

        # Extract and save the motility data from the config file
        self.tree.find(stem + "/speed").text = str(motility.speed)
        self.tree.find(stem + "/persistence_time").text = str(motility.persistence)
        self.tree.find(stem + "/migration_bias").text = str(motility.bias)

        if motility.motility_enabled:
            self.tree.find(stem + "/options/enabled").text = "true" 
        else:
            self.tree.find(stem + "/options/enabled").text = "false" 

        if motility.use_2d:
            self.tree.find(stem + "/options/use_2D").text = "true" 
        else:
            self.tree.find(stem + "/options/use_2D").text = "false" 

        chmo_str = stem + "/options/chemotaxis"

        if motility.chemo_enabled:
            self.tree.find(chmo_str + "/enabled").text = "true"
        else:
            self.tree.find(chmo_str + "/enabled").text = "false"

        self.tree.find(chmo_str + "/substrate").text = motility.chemo_substrate
        self.tree.find(chmo_str + "/direction").text = str(motility.chemo_direction)

    def update_params(self, name, new_parameters: CellParameters) -> None:
        """
        Writes the new parameters to the XML tree object and also updates the XML file.

        Parameters
        ----------
        name: str
            The name of the cell definition to be updated.
        new_parameters: CellParameters
            The new cell parameters to be writeen to the XML file.
        """
        self.write_motility_params(name, new_parameters.motility)
        
        self.tree.write(self.config_file)


ParamsUpdater = Callable[[List[float]], None]


def update_motility_params(self, new_values: List[float]) -> None:
    cell_definition_name = "default"

    # Read the data from the file
    xml_parser = ConfigFileParser()
    cell_data = xml_parser.read_cell_data(cell_definition_name)

    # Update the data
    cell_data.motility.speed = new_values[0]
    cell_data.motility.persistence = new_values[1]
    cell_data.motility.bias = new_values[2]

    xml_parser.update_params(cell_data)


def update_mechanics_params(self, new_values: List[float]) -> None:
    cell_definition_name = "default"

    # Read the data from the file
    xml_parser = ConfigFileParser()
    cell_data = xml_parser.read_cell_data(cell_definition_name)

    # Update the data
    cell_data.mechanics.adhesion_strength = new_values[0]
    cell_data.mechanics.repulsion_strength = new_values[1]
    cell_data.mechanics.adhesion_distance = new_values[2]

    xml_parser.update_params(cell_data)
