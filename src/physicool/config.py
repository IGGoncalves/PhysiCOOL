# This module enables users to programmatically modify their PhysiCell XML config file
from pathlib import Path
from xml.etree import ElementTree
from dataclasses import dataclass, field
from typing import Callable, List, Union, Dict, Optional
from enum import Enum

from pydantic import BaseModel, confloat, conint


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


class Substance(BaseModel):
    name: str
    diffusion_coefficient: confloat(ge=0.0)
    decay_rate: confloat(ge=0.0)
    initial_conditions: confloat(ge=0.0)
    Dirichlet_boundary_condition: confloat(ge=0.0)


class Volume(BaseModel):
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
    cell_cell_adhesion_strength: confloat(ge=0.0)
    cell_cell_repulsion_strength: confloat(ge=0.0)
    relative_maximum_adhesion_distance: confloat(ge=0.0)
    set_relative_equilibrium_distance: confloat(ge=0.0)
    set_absolute_equilibrium_distance: confloat(ge=0.0)

    class Config:
        validate_assignment = True


class Motility(BaseModel):
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


class Cycle(BaseModel):
    code: CycleCode
    phase_durations: Optional[List[confloat(ge=0.0)]]
    phase_transition_rates: Optional[List[confloat(ge=0.0)]]

    class Config:
        validate_assignment = True


class DeathCode(Enum):
    APOPTOSIS = 100
    NECROSIS = 101


class Death(BaseModel):
    code: DeathCode
    phase_durations: Optional[List[confloat(ge=0.0)]]
    phase_transition_rates: Optional[List[confloat(ge=0.0)]]
    unlysed_fluid_change_rate: confloat(ge=0.0)
    lysed_fluid_change_rate: confloat(ge=0.0)
    cytoplasmic_biomass_change_rate: confloat(ge=0.0)
    nuclear_biomass_change_rate: confloat(ge=0.0)
    calcification_rate: confloat(ge=0.0)
    relative_rupture_volume: confloat(ge=0.0)

    class Config:
        validate_assignment = True


class CustomData(BaseModel):
    name: str
    value: float


@dataclass
class Phenotype:
    cycle: Cycle
    death: List[Death]


@dataclass
class CellParameters:
    """A class to store the cell data for a given cell definition of the config file."""

    name: str
    phenotype: Phenotype
    volume: Volume
    mechanics: Mechanics
    motility: Motility
    secretion: List[Secretion]


def parse_cycle(tree: ElementTree, path: str) -> Dict[str, Union[float, List[float]]]:
    cycle_node = tree.find(path)
    code = float(cycle_node.attrib["code"])
    data_type = list(cycle_node)[0].tag
    durations = None
    rates = None

    if data_type == "phase_durations":
        durations = [float(duration.text) for duration in cycle_node[0]]
    elif data_type == "phase_transition_rates":
        rates = [float(duration.text) for duration in cycle_node[0]]

    return {"code": code, "phase_durations": durations, "phase_transition_rates": rates}


def parse_death_model(
    tree: ElementTree, path: str, name: str
) -> Dict[str, Union[float, List[float]]]:
    model_stem = path + f"/model[@name='{name}']"

    death_node = tree.find(model_stem)
    code = float(death_node.attrib["code"])
    data_type = list(death_node)[1].tag
    durations = None
    rates = None

    if data_type == "phase_durations":
        durations = [float(duration.text) for duration in death_node[1]]
    elif data_type == "phase_transition_rates":
        rates = [float(duration.text) for duration in death_node[1]]

    model_stem += "/parameters"
    unlysed_fluid_change_rate = float(
        tree.find(model_stem + "/unlysed_fluid_change_rate").text
    )
    lysed_fluid_change_rate = float(tree.find(model_stem + "/lysed_fluid_change_rate").text)
    cytoplasmic_biomass_change_rate = float(
        tree.find(model_stem + "/cytoplasmic_biomass_change_rate").text
    )
    nuclear_biomass_change_rate = float(
        tree.find(model_stem + "/nuclear_biomass_change_rate").text
    )
    calcification_rate = float(tree.find(model_stem + "/calcification_rate").text)
    relative_rupture_volume = float(tree.find(model_stem + "/relative_rupture_volume").text)

    return {
        "code": code,
        "phase_durations": durations,
        "phase_transition_rates": rates,
        "unlysed_fluid_change_rate": unlysed_fluid_change_rate,
        "lysed_fluid_change_rate": lysed_fluid_change_rate,
        "cytoplasmic_biomass_change_rate": cytoplasmic_biomass_change_rate,
        "nuclear_biomass_change_rate": nuclear_biomass_change_rate,
        "calcification_rate": calcification_rate,
        "relative_rupture_volume": relative_rupture_volume,
    }


def parse_death(
    tree: ElementTree, path: str
) -> List[Dict[str, Union[float, List[float]]]]:
    models = [model.attrib["name"] for model in tree.find(path).findall("model")]
    death_data = []

    for model in models:
        data = parse_death_model(tree=tree, path=path, name=model)
        death_data.append(data)

    return death_data


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
        tree.find(path + "/cell_cell_adhesion_strength").text
    )
    cell_cell_repulsion_strength = float(
        tree.find(path + "/cell_cell_repulsion_strength").text
    )
    relative_maximum_adhesion_distance = float(
        tree.find(path + "/relative_maximum_adhesion_distance").text
    )

    relative_equilibrium_distance = float(
        tree.find(path + "/options/set_relative_equilibrium_distance").text
    )

    absolute_equilibrium_distance = float(
        tree.find(path + "/options/set_absolute_equilibrium_distance").text
    )

    return {
        "cell_cell_adhesion_strength": cell_cell_adhesion_strength,
        "cell_cell_repulsion_strength": cell_cell_repulsion_strength,
        "relative_maximum_adhesion_distance": relative_maximum_adhesion_distance,
        "set_relative_equilibrium_distance": relative_equilibrium_distance,
        "set_absolute_equilibrium_distance": absolute_equilibrium_distance,
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
    relative_rupture_volume = float(tree.find(path + "/relative_rupture_volume").text)

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


def parse_secretion_substance(
    tree: ElementTree, path: str, substrate: str
) -> Dict[str, float]:
    # Extract and save the motility data from the config file
    substrate_stem = path + f"/substrate[@name='{substrate}']"

    secretion_rate = float(tree.find(substrate_stem + "/secretion_rate").text)
    secretion_target = float(tree.find(substrate_stem + "/secretion_target").text)
    uptake_rate = float(tree.find(substrate_stem + "/uptake_rate").text)
    net_export_rate = float(tree.find(substrate_stem + "/net_export_rate").text)

    return {
        "name": substrate,
        "secretion_rate": secretion_rate,
        "secretion_target": secretion_target,
        "uptake_rate": uptake_rate,
        "net_export_rate": net_export_rate,
    }


def parse_secretion(tree: ElementTree, path: str) -> List[Dict[str, float]]:
    substrates = [
        substrate.attrib["name"] for substrate in tree.find(path).findall("substrate")
    ]
    secretion_data = []

    for substrate in substrates:
        data = parse_secretion_substance(tree=tree, path=path, substrate=substrate)
        secretion_data.append(data)

    return secretion_data


def parse_custom(tree: ElementTree, path: str) -> List[Dict[str, Union[float, str]]]:
    return [{"name": variable.tag, "value": float(variable.text)}
            for variable in list(tree.find(path)) if variable.text]


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
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/cycle"
        return Cycle(**parse_cycle(self.tree, path=stem))

    def read_death_params(self, name: str) -> List[Death]:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/death"
        return [Death(**model) for model in parse_death(self.tree, path=stem)]

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
        return Mechanics(**parse_mechanics(tree=self.tree, path=stem))

    def read_motility_params(self, name: str) -> Motility:
        """Reads the motility parameters from the config file into a custom data structure"""
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/motility"
        return Motility(**parse_motility(tree=self.tree, path=stem))

    def read_secretion_params(self, name: str) -> List[Secretion]:
        """Reads the secretion parameters from the config file into a custom data structure"""
        # Build basic string stem to find secretion cell data for cell definition
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/secretion"
        return [
            Secretion(**substance)
            for substance in parse_secretion(tree=self.tree, path=stem)
        ]

    def read_custom_data(self, name: str) -> List[CustomData]:
        stem = f"cell_definitions/cell_definition[@name='{name}']/custom_data"
        return [CustomData(**custom) for custom in parse_custom(self.tree, stem)]

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

    def read_user_parameters(self):
        return [CustomData(**custom) for custom in parse_custom(self.tree, "user_parameters")]

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
