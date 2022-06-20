# This module enables users to programmatically modify their PhysiCell XML config file
from pathlib import Path
from xml.etree import ElementTree
from dataclasses import dataclass, field
from typing import Callable, List, Union, Dict
from enum import Enum

from pydantic import BaseModel, confloat, conint


class BoolSettings(BaseModel):
    enabled: bool
    value: confloat(ge=0.0)

    class Config:
        validate_assignment = True


class Domain(BaseModel):
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    dx: conint(ge=0.0)
    dy: conint(ge=0.0)
    dz: conint(ge=0.0)
    use_2d: bool


class Overall(BaseModel):
    max_time: conint(ge=0.0)
    dt_diffusion: conint(ge=0.0)
    dt_mechanics: conint(ge=0.0)
    dt_phenotype: conint(ge=0.0)


class Volume(BaseModel):
    """
    A class that represents the cell volume parameters stored in the config file.

    Parameters
    ----------
    total
        The total cell volume value.
    fluid_fraction
        The cell fluid fraction value.
    nuclear
        The cell nuclear volume value.
    fluid_change_rate
        The cell fluid change rate value.
    cytoplasmic_biomass_change_rate
        The cytoplasmic biomass change rate value.
    nuclear_biomass_change_rate
        The nuclear biomass change rate value.
    calcified_fraction
        The cell calcified fraction value.
    calcification_rate
        The cell calcification rate value.
    relative_rupture_volume
        The cell relative rupture volume value.
    """

    total: confloat(ge=0.0)
    fluid_fraction: confloat(ge=0.0, le=1.0)
    nuclear: confloat(ge=0.0)
    fluid_change_rate: confloat(ge=0.0)
    cytoplasmic_biomass_change_rate: confloat(ge=0.0)
    nuclear_biomass_change_rate: confloat(ge=0.0)
    calcified_fraction: confloat(ge=0.0, le=1.0)
    calcification_rate: confloat(ge=0.0)
    relative_rupture_volume: confloat(ge=0.0)

    class Config:
        validate_assignment = True


class Mechanics(BaseModel):
    """
    A class that represents the cell mechanics parameters stored in the config file.
    """

    cell_cell_adhesion_strength: confloat(ge=0.0)
    cell_cell_repulsion_strength: confloat(ge=0.0)
    relative_maximum_adhesion_distance: confloat(ge=0.0)
    set_relative_equilibrium_distance: BoolSettings
    set_absolute_equilibrium_distance: BoolSettings

    class Config:
        validate_assignment = True


class Motility(BaseModel):
    """
    A class that represents the cell motility parameters stored in the config file.

    Parameters
    ----------
    speed
        The cell speed value.
    persistence
        The cell persistence time.
    bias
        The cell motility bias.
    motility_enabled
        If cells are able to move.
    use_2d
        If cells move in 2D.
    chemotaxis_enabled
        If chemotaxis is considered.
    chemotaxis_substrate
        The substance that induces chemotaxis.
    chemotaxis_direction
        The direction of the chemotaxis motility.
    """

    speed: confloat(ge=0.0)
    persistence: confloat(ge=0.0)
    bias: confloat(ge=0.0, le=1.0)
    motility_enabled: bool
    use_2d: bool
    chemotaxis_enabled: bool
    chemotaxis_substrate: str
    chemotaxis_direction: float

    class Config:
        validate_assignment = True


class Secretion(BaseModel):
    """
    A class that represents the cell secretion parameters stored in the config file
    for a single substance.

    Parameters
    ----------
    name
        The name of the secreted substance.
    secretion_rate
        The secretion rate of the substance.
    secretion_target
        The secretion target for the substance.
    uptake_rate
        The uptake rate of the substance.
    net_export_rate
        The net export rate of the substance.
    """

    name: str
    secretion_rate: confloat(ge=0.0)
    secretion_target: confloat(ge=0.0)
    uptake_rate: confloat(ge=0.0)
    net_export_rate: confloat(ge=0.0)

    class Config:
        validate_assignment = True


class CycleCode(Enum):
    LIVE = 0
    FLOW_CYTOMETRY_SEPARATED = 6


class Cycle:
    def __init__(self, code: CycleCode, transition_rates: List[float]):
        self.code = code
        self.rates = transition_rates


@dataclass
class Phenotype:
    cycle: Cycle


@dataclass
class CellParameters:
    """A class to store the cell data for a given cell definition of the config file."""

    name: str
    phenotype: Phenotype
    volume: Volume
    mechanics: Mechanics
    motility: Motility
    secretion: List[Secretion]


def parse_motility(tree: ElementTree, path: str) -> Dict[str, Union[float, str, bool]]:
    # Extract and save the motility data from the config file
    speed = float(tree.find(path + "/speed").text)
    persistence = float(tree.find(path + "/persistence_time").text)
    bias = float(tree.find(path + "/migration_bias").text)
    motility_enabled = tree.find(path + "/options/enabled").text == "true"
    use_2d = tree.find(path + "/options/use_2D").text == "true"
    chemotaxis_enabled = tree.find(path + "/options/chemotaxis/enabled").text == "true"
    chemotaxis_substrate = tree.find(path + "/options/chemotaxis/substrate").text
    chemotaxis_direction = float(tree.find(path + "/options/chemotaxis/direction").text)

    return {
        "speed": speed,
        "persistence": persistence,
        "bias": bias,
        "motility_enabled": motility_enabled,
        "use_2d": use_2d,
        "chemotaxis_enabled": chemotaxis_enabled,
        "chemotaxis_substrate": chemotaxis_substrate,
        "chemotaxis_direction": chemotaxis_direction,
    }


def parse_mechanics(tree: ElementTree, path: str) -> Dict[str, float]:
    # Extract and save the basic mechanics data from the config file
    cell_cell_adhesion_strength = float(
        tree.find(path + "/cell_cell_cell_cell_adhesion_strength").text
    )
    cell_cell_repulsion_strength = float(
        tree.find(path + "/cell_cell_cell_cell_repulsion_strength").text
    )
    relative_maximum_adhesion_distance = float(
        tree.find(path + "/relative_maximum_relative_maximum_adhesion_distance").text
    )

    relative_eq_dist_enabled = tree.find(
        path + "/options/set_relative_equilibrium_distance"
    ).attrib["enabled"]
    relative_eq_dist_value = tree.find(
        path + "/options/set_relative_equilibrium_distance"
    ).text

    absolute_eq_dist_enabled = tree.find(
        path + "/options/set_absolute_equilibrium_distance"
    ).attrib["enabled"]
    absolute_eq_dist_value = tree.find(
        path + "/options/set_absolute_equilibrium_distance"
    ).text

    return {
        "cell_cell_adhesion_strength": cell_cell_adhesion_strength,
        "cell_cell_repulsion_strength": cell_cell_repulsion_strength,
        "relative_maximum_adhesion_distance": relative_maximum_adhesion_distance,
        "set_relative_equilibrium_enabled": relative_eq_dist_enabled,
        "set_relative_equilibrium_value": relative_eq_dist_value,
        "set_absolute_equilibrium_enabled": absolute_eq_dist_enabled,
        "set_absolute_equilibrium_value": absolute_eq_dist_value,
    }


def parse_volume(tree: ElementTree, path: str) -> Dict[str, float]:
    total = float(tree.find(path + "/total").text)
    fluid_fraction = float(tree.find(path + "/fluid_fraction").text)
    nuclear = float(tree.find(path + "/nuclear").text)
    fluid_change_rate = float(tree.find(path + "/fluid_change_rate").text)
    cytoplasmic_biomass_change_rate = float(
        tree.find(path + "/cytoplasmic_biomass_change_rate").text
    )
    nuclear_biomass_change_rate = float(
        tree.find(path + "/nuclear_biomass_change_rate").text
    )
    calcified_fraction = float(tree.find(path + "/calcified_fraction").text)
    calcification_rate = float(tree.find(path + "/calcification_rate").text)
    relative_rupture_volume = float(
        tree.find(path + "/relative_relative_rupture_volume").text
    )

    return {
        "total": total,
        "fluid_fraction": fluid_fraction,
        "nuclear": nuclear,
        "fluid_change_rate": fluid_change_rate,
        "cytoplasmic_biomass_change_rate": cytoplasmic_biomass_change_rate,
        "nuclear_biomass_change_rate": nuclear_biomass_change_rate,
        "calcified_fraction": calcified_fraction,
        "calcification_rate": calcification_rate,
        "relative_rupture_volume": relative_rupture_volume,
    }


class ConfigFileParser:
    """A class that acts as an interface between the user and the XML config file"""

    def __init__(
        self, path: Union[str, Path] = Path("config/PhysiCell_settings.xml")
    ) -> None:
        if isinstance(path, str):
            path = Path(path)

        self.config_file = path
        self.tree = ElementTree.parse(path)

    @property
    def cell_definitions_list(self) -> List[str]:
        """Returns a list with the names of the cell definitions in the XML file"""
        root = self.tree.getroot()
        cell_definitions = root.find("cell_definitions").findall("cell_definition")

        return [definition.attrib["name"] for definition in cell_definitions]

    @property
    def me_substance_list(self) -> List[str]:
        """Returns a list with the names of the substances in the XML file"""
        root = self.tree.getroot()
        substances = root.find("microenvironment/domain/variables").findall("variable")

        return [substance.attrib["name"] for substance in substances]

    def read_cycle_params(self, name: str) -> Cycle:
        # Build basic string stem to find motility cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + "/phenotype/cycle"

        cycle_node = self.tree.find(stem)
        code = CycleCode(int(cycle_node.items()[0][1]))
        rates = [float(duration.text) for duration in cycle_node[0]]

        return Cycle(code=code, transition_rates=rates)

    def read_phenotype_params(self, name: str) -> Phenotype:
        cycle = self.read_cycle_params(name)

        return Phenotype(cycle=cycle)

    def read_volume_params(self, name: str) -> Volume:
        """Reads the motility parameters from the config file into a custom data structure"""
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/volume"

        return Volume(**parse_volume(tree=self.tree, path=stem))

    def read_mechanics_params(self, name: str) -> Mechanics:
        """Reads the mechanics parameters from the config file into a custom data structure"""
        # Build basic string stem to find mechanics cell data for cell definition
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/mechanics"
        mechanics_data = parse_mechanics(tree=self.tree, path=stem)

        return Mechanics(
            cell_cell_adhesion_strength=mechanics_data["cell_cell_adhesion_strength"],
            cell_cell_repulsion_strength=mechanics_data["cell_cell_repulsion_strength"],
            relative_maximum_adhesion_distance=mechanics_data[
                "relative_maximum_adhesion_distance"
            ],
            set_relative_equilibrium_distance=BoolSettings(
                enabled=mechanics_data["set_relative_equilibrium_enabled"],
                value=mechanics_data["set_relative_equilibrium_value"],
            ),
            set_absolute_equilibrium_distance=BoolSettings(
                enabled=mechanics_data["set_absolute_equilibrium_enabled"],
                value=mechanics_data["set_absolute_equilibrium_value"],
            ),
        )

    def read_motility_params(self, name: str) -> Motility:
        """Reads the motility parameters from the config file into a custom data structure"""
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/motility"

        return Motility(**parse_motility(tree=self.tree, path=stem))

    def read_secretion_params(self, name: str) -> List[Secretion]:
        """Reads the secretion parameters from the config file into a custom data structure"""
        # Build basic string stem to find secretion cell data for cell definition
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + f"/phenotype/secretion"

        substrates = [
            substrate.attrib["name"]
            for substrate in self.tree.find(stem).findall("substrate")
        ]

        secretion_data = []

        for substrate in substrates:
            substrate_stem = stem + f"/substrate[@name='{substrate}']"

            # Extract and save the motility data from the config file
            secretion_rate = float(
                self.tree.find(substrate_stem + "/secretion_rate").text
            )
            secretion_target = float(
                self.tree.find(substrate_stem + "/secretion_target").text
            )
            uptake_rate = float(self.tree.find(substrate_stem + "/uptake_rate").text)
            net_export_rate = float(
                self.tree.find(substrate_stem + "/net_export_rate").text
            )

            secretion_data.append(
                Secretion(
                    name=substrate,
                    secretion_rate=secretion_rate,
                    secretion_target=secretion_target,
                    uptake_rate=uptake_rate,
                    net_export_rate=net_export_rate,
                )
            )

        return secretion_data

    def read_cell_data(self, name: str = "default") -> CellParameters:
        """
        Reads all the fields for a given cell definition into a custom cell data type.

        Parameters
        ----------
        name: str, default "default"
            The name of the cell definition to be read

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
            phenotype = self.read_phenotype_params(name)
            volume = self.read_volume_params(name)
            mechanics = self.read_mechanics_params(name)
            motility = self.read_motility_params(name)
            secretion = self.read_secretion_params(name)

            return CellParameters(
                name, phenotype, volume, mechanics, motility, secretion
            )

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

    def write_cycle_params(self, name: str, cycle: Cycle) -> None:
        cell_string = f"cell_definitions/cell_definition[@name='{name}']"
        stem = cell_string + "/phenotype/cycle"

        for i, rate in enumerate(cycle.rates):
            self.tree.find(
                stem + f"/phase_durations/duration[@index='{i}']"
            ).text = str(rate)

    def write_motility_params(self, name: str, motility: Motility) -> None:
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

        if motility.chemotaxis_enabled:
            self.tree.find(chmo_str + "/enabled").text = "true"
        else:
            self.tree.find(chmo_str + "/enabled").text = "false"

        self.tree.find(chmo_str + "/substrate").text = motility.chemotaxis_substrate
        self.tree.find(chmo_str + "/direction").text = str(
            motility.chemotaxis_direction
        )

    def update_params(self, cell_data: CellParameters) -> None:
        """
        Writes the new parameters to the XML tree object and also updates the XML file.

        Parameters
        ----------
        new_parameters: CellParameters
            The new cell parameters to be writeen to the XML file.
        """
        self.write_motility_params(cell_data.name, cell_data.motility)
        self.write_cycle_params(cell_data.name, cell_data.phenotype.cycle)

        self.tree.write(self.config_file)


UpdaterFunction = Callable[[CellParameters, List[float]], None]


def update_motility_values(cell_data: CellParameters, new_values=List[float]):
    cell_data.motility.speed = new_values[0]
    cell_data.motility.persistence = new_values[1]
    cell_data.motility.bias = new_values[2]


def update_mechanics_values(cell_data: CellParameters, new_values=List[float]):
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
