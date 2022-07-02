# This module enables users to programmatically read and write to the PhysiCell XML config file.
# Data validation is not performed by this module. To safely write to the XML file, use the
# ConfigFileParser (from the config module) instead.
from xml.etree import ElementTree
from typing import List, Union, Dict


def parse_domain(tree: ElementTree, path: str) -> Dict[str, Union[bool, float]]:
    """
    Reads and returns the <domain> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the domain node (e.g., "domain").

    Returns
    -------
    Dict[str, Union[bool, float]]
        A dictionary with the domain data for a simulation (x_min, x_max,
        y_min, y_max, z_min, z_max, dx, dy, dz and use_2D).

    Raises
    ------
    ValueError
        When the passed path does not point to the domain node.
    """
    if tree.find(path).tag != "domain":
        raise ValueError("The passed path does not point to the correct node.")

    x_min = float(tree.find(path + "/x_min").text)
    x_max = float(tree.find(path + "/x_max").text)
    y_min = float(tree.find(path + "/y_min").text)
    y_max = float(tree.find(path + "/y_max").text)
    z_min = float(tree.find(path + "/z_min").text)
    z_max = float(tree.find(path + "/z_max").text)
    dx = float(tree.find(path + "/dx").text)
    dy = float(tree.find(path + "/dy").text)
    dz = float(tree.find(path + "/dz").text)
    use_2d = tree.find(path + "/use_2D").text == "true"

    return {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "z_min": z_min,
        "z_max": z_max,
        "dx": dx,
        "dy": dy,
        "dz": dz,
        "use_2d": use_2d,
    }


def parse_overall(tree: ElementTree, path: str) -> Dict[str, float]:
    """
    Reads and returns the <overall> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the overall node (e.g., "overall").

    Returns
    -------
    Dict[str, float]
        A dictionary with the overall data for a simulation (max_time,
        dt_diffusion, dt_mechanics, dt_phenotype).

    Raises
    ------
    ValueError
        When the passed path does not point to the overall node.
    """
    if tree.find(path).tag != "overall":
        raise ValueError("The passed path does not point to the correct node.")

    max_time = float(tree.find(path + "/max_time").text)
    dt_diffusion = float(tree.find(path + "/dt_diffusion").text)
    dt_mechanics = float(tree.find(path + "/dt_mechanics").text)
    dt_phenotype = float(tree.find(path + "/dt_phenotype").text)

    return {
        "max_time": max_time,
        "dt_diffusion": dt_diffusion,
        "dt_mechanics": dt_mechanics,
        "dt_phenotype": dt_phenotype,
    }


def parse_substance(
    tree: ElementTree, path: str, name: str
) -> Dict[str, Union[str, float]]:
    """
    Reads and returns the <variable> data for a microenvironment substance.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the microenvironment node
        (e.g., "microenvironment_setup").
    name:
        A string with the name of the microenvironment variable to be read.
    Returns
    -------
    Dict[str, Union[str, float]]
        A dictionary with the data for one of the substances in a simulation
        (name, diffusion_coefficient, decay_rate, initial_condition,
        Dirichlet_boundary_condition).

    Raises
    ------
    ValueError
        When the passed path does not point to the microenvironment node.
    ValueError
        When the passed name does not match any of the variables in the file.
    """
    if tree.find(path).tag != "microenvironment_setup":
        raise ValueError("The passed path does not point to the correct node.")

    substances = [
        substance.attrib["name"] for substance in tree.find(path).findall("variable")
    ]

    if name not in substances:
        raise ValueError("The passed substance name is not valid.")

    substance_stem = path + f"/variable[@name='{name}']"
    diffusion_coefficient = float(
        tree.find(substance_stem + "/physical_parameter_set/diffusion_coefficient").text
    )
    decay_rate = float(
        tree.find(substance_stem + "/physical_parameter_set/decay_rate").text
    )
    initial_condition = float(tree.find(substance_stem + "/initial_condition").text)
    dirichlet_boundary_condition = float(
        tree.find(substance_stem + "/Dirichlet_boundary_condition").text
    )

    return {
        "name": name,
        "diffusion_coefficient": diffusion_coefficient,
        "decay_rate": decay_rate,
        "initial_condition": initial_condition,
        "dirichlet_boundary_condition": dirichlet_boundary_condition,
    }


def parse_microenvironment(
    tree: ElementTree, path: str
) -> List[Dict[str, Union[float, str]]]:
    """
    Reads and returns the <microenvironment> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the microenvironment node
        (e.g., "microenvironment_setup").

    Returns
    -------
    List[Dict[str, Union[float, str]]]
        A list of dictionaries with the data for all the substances in a simulation
        (name, diffusion_coefficient, decay_rate, initial_condition,
        Dirichlet_boundary_condition).

    Raises
    ------
    ValueError
        When the passed path does not point to the microenvironment node.
    """
    if tree.find(path).tag != "microenvironment_setup":
        raise ValueError("The passed path does not point to the correct node.")

    substances = [
        substance.attrib["name"] for substance in tree.find(path).findall("variable")
    ]
    substance_data = []

    for substance in substances:
        data = parse_substance(tree=tree, path=path, name=substance)
        substance_data.append(data)

    return substance_data


def parse_cycle(tree: ElementTree, path: str) -> Dict[str, Union[float, List[float]]]:
    """
    Reads and returns the <cycle> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the cycle node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/cycle").

    Returns
    -------
    Dict[str, Union[float, List[float]]]
        A dictionary with the cycle data for a cell definition in a simulation
        (code, phase_durations or phase_transition_rates).

    Raises
    ------
    ValueError
        When the passed path does not point to a valid cycle node.
    """
    if tree.find(path).tag != "cycle":
        raise ValueError("The passed path does not point to the correct node.")

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
    """
    Reads and returns the <death> data for a death model.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the death node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/death").
    name:
        A string with the name of the death model to be read.
    Returns
    -------
    Dict[str, Union[float, List[float]]]
        A dictionary with the data for one of the death models for a cell definition
         in a simulation (code, death_rate, phase_duration_rates or phase_transition_rates,
         unlysed_fluid_change_rate, unlysed_fluid_change_rate, cytoplasmic_biomass_change_rate,
         nuclear_biomass_change_rate, calcification_rate, relative_rupture_volume).

    Raises
    ------
    ValueError
        When the passed path does not point to the death node.
    ValueError
        When the passed name does not match any of the death models for the cell definition.
    """
    if tree.find(path).tag != "death":
        raise ValueError("The passed path does not point to the correct node.")

    models = [model.attrib["name"] for model in tree.find(path).findall("model")]
    if name not in models:
        raise ValueError("The passed name does not match a valid death model.")

    model_stem = path + f"/model[@name='{name}']"
    death_node = tree.find(model_stem)
    code = float(death_node.attrib["code"])
    data_type = list(death_node)[1].tag
    durations = None
    rates = None

    death_rate = float(tree.find(model_stem + "/death_rate").text)

    if data_type == "phase_durations":
        durations = [float(duration.text) for duration in death_node[1]]
    elif data_type == "phase_transition_rates":
        rates = [float(duration.text) for duration in death_node[1]]

    model_stem += "/parameters"
    unlysed_fluid_change_rate = float(
        tree.find(model_stem + "/unlysed_fluid_change_rate").text
    )
    lysed_fluid_change_rate = float(
        tree.find(model_stem + "/lysed_fluid_change_rate").text
    )
    cytoplasmic_biomass_change_rate = float(
        tree.find(model_stem + "/cytoplasmic_biomass_change_rate").text
    )
    nuclear_biomass_change_rate = float(
        tree.find(model_stem + "/nuclear_biomass_change_rate").text
    )
    calcification_rate = float(tree.find(model_stem + "/calcification_rate").text)
    relative_rupture_volume = float(
        tree.find(model_stem + "/relative_rupture_volume").text
    )

    return {
        "name": name,
        "code": code,
        "death_rate": death_rate,
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
    """
    Reads and returns the <death> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the death node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/death").

    Returns
    -------
    List[Dict[str, Union[float, List[float]]]]
        A list of dictionaries with the data for all the death models for a cell definition
         in a simulation (code, death_rate, phase_duration_rates or phase_transition_rates,
         unlysed_fluid_change_rate, unlysed_fluid_change_rate, cytoplasmic_biomass_change_rate,
         nuclear_biomass_change_rate, calcification_rate, relative_rupture_volume).

    Raises
    ------
    ValueError
        When the passed path does not point to the death node.
    """
    if tree.find(path).tag != "death":
        raise ValueError("The passed path does not point to the correct node.")

    models = [model.attrib["name"] for model in tree.find(path).findall("model")]
    death_data = []

    for model in models:
        data = parse_death_model(tree=tree, path=path, name=model)
        death_data.append(data)

    return death_data


def parse_volume(tree: ElementTree, path: str) -> Dict[str, float]:
    """
    Reads and returns the <volume> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the volume node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/volume").

    Returns
    -------
    Dict[str, float]
        A dictionary with the volume data for a cell definition in a simulation
        (total, fluid_fraction, nuclear, fluid_change_rate, cytoplasmic_biomass_change_rate,
        nuclear_biomass_change_rate, calcified_fraction, calcification_rat,
        relative_rupture_volume).

    Raises
    ------
    ValueError
        When the passed path does not point to a valid volume node.
    """
    if tree.find(path).tag != "volume":
        raise ValueError("The passed path does not point to the correct node.")

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


def parse_mechanics(tree: ElementTree, path: str) -> Dict[str, float]:
    """
    Reads and returns the <mechanics> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the mechanics node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/mechanics").

    Returns
    -------
    Dict[str, float]
        A dictionary with the mechanics data for a cell definition in a simulation
        (cell_cell_adhesion_strength, cell_cell_repulsion_strength,
        set_relative_maximum_adhesion_distance, set_relative_equilibrium_distance,
        set_absolute_equilibrium_distance).

    Raises
    ------
    ValueError
        When the passed path does not point to a valid mechanics node.
    """
    if tree.find(path).tag != "mechanics":
        raise ValueError("The passed path does not point to the correct node.")

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


def parse_motility(tree: ElementTree, path: str) -> Dict[str, Union[float, str, bool]]:
    """
    Reads and returns the <motility> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the motility node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/motility").

    Returns
    -------
    Dict[str, Union[float, str, bool]]
        A dictionary with the motility data for a cell definition in a simulation
        (code, phase_durations or phase_transition_rates).

    Raises
    ------
    ValueError
        When the passed path does not point to a valid motility node.
    """
    if tree.find(path).tag != "motility":
        raise ValueError("The passed path does not point to the correct node.")

    speed = float(tree.find(path + "/speed").text)
    persistence_time = float(tree.find(path + "/persistence_time").text)
    migration_bias = float(tree.find(path + "/migration_bias").text)
    motility_enabled = tree.find(path + "/options/enabled").text == "true"
    use_2d = tree.find(path + "/options/use_2D").text == "true"
    chemotaxis_enabled = tree.find(path + "/options/chemotaxis/enabled").text == "true"
    chemotaxis_substrate = tree.find(path + "/options/chemotaxis/substrate").text
    chemotaxis_direction = float(tree.find(path + "/options/chemotaxis/direction").text)

    return {
        "speed": speed,
        "persistence_time": persistence_time,
        "migration_bias": migration_bias,
        "motility_enabled": motility_enabled,
        "use_2d": use_2d,
        "chemotaxis_enabled": chemotaxis_enabled,
        "chemotaxis_substrate": chemotaxis_substrate,
        "chemotaxis_direction": chemotaxis_direction,
    }


def parse_secretion_substance(
    tree: ElementTree, path: str, name: str
) -> Dict[str, Union[str, float]]:
    """
    Reads and returns the data for a secretion <substrate>.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the secretion node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/secretion").
    name:
        A string with the name of the secretion substance to be read.
    Returns
    -------
    Dict[str, Union[str, float]]
        A dictionary with the data for one of the substances in a simulation
        (name, secretion_rate, secretion_target, uptake_rate, net_export_rate).

    Raises
    ------
    ValueError
        When the passed path does not point to the secretion node.
    ValueError
        When the passed name does not match any of the substances in the secretion data.
    """
    if tree.find(path).tag != "secretion":
        raise ValueError("The passed path does not point to the correct node.")

    substrates = [
        substrate.attrib["name"] for substrate in tree.find(path).findall("substrate")
    ]

    if name not in substrates:
        raise ValueError("The passed name does not match a valid death model.")

    substrate_stem = path + f"/substrate[@name='{name}']"
    secretion_rate = float(tree.find(substrate_stem + "/secretion_rate").text)
    secretion_target = float(tree.find(substrate_stem + "/secretion_target").text)
    uptake_rate = float(tree.find(substrate_stem + "/uptake_rate").text)
    net_export_rate = float(tree.find(substrate_stem + "/net_export_rate").text)

    return {
        "name": name,
        "secretion_rate": secretion_rate,
        "secretion_target": secretion_target,
        "uptake_rate": uptake_rate,
        "net_export_rate": net_export_rate,
    }


def parse_secretion(tree: ElementTree, path: str) -> List[Dict[str, Union[str, float]]]:
    """
    Reads and returns the <secretion> data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the secretion node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/secretion").

    Returns
    -------
    List[Dict[str, Union[str, float]]]
        A list of dictionaries with the data for all the secretion models for a cell definition
         in a simulation (name, secretion_rate, secretion_target, uptake_rate, net_export_rate).

    Raises
    ------
    ValueError
        When the passed path does not point to the secretion node.
    """
    if tree.find(path).tag != "secretion":
        raise ValueError("The passed path does not point to the correct node.")

    substrates = [
        substrate.attrib["name"] for substrate in tree.find(path).findall("substrate")
    ]
    secretion_data = []

    for substrate in substrates:
        data = parse_secretion_substance(tree=tree, path=path, name=substrate)
        secretion_data.append(data)

    return secretion_data


def parse_custom(tree: ElementTree, path: str) -> List[Dict[str, Union[float, str]]]:
    """
    Reads and returns the custom data.

    Parameters
    ----------
    tree:
        A ElementTree object of the XML config file to be read.
    path:
        A string with the path to the motility node
        (e.g., "cell_definitions/cell_definition[@name='default']/custom_data", "user_parameters").

    Returns
    -------
    List[Dict[str, Union[float, str]]]
        A list of dictionaries with data for the custom variables (custom cell data and
        user parameters). Dictionaries have the format {"name": ..., "value": ...}.

    Raises
    ------
    ValueError
        When the passed path does not point to a valid custom node.
    """
    if (tree.find(path).tag != "custom_data") & (
        tree.find(path).tag != "user_parameters"
    ):
        raise ValueError("The passed path does not point to the correct node.")

    return [
        {"name": variable.tag, "value": float(variable.text)}
        for variable in list(tree.find(path))
        if variable.text
    ]


def write_domain(
    new_values: Dict[str, Union[float, bool]], tree: ElementTree, path: str
) -> None:
    """
    Writes new values for the <domain> data in the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the domain variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the domain node (e.g., "domain").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid domain node.
    """
    if tree.find(path).tag != "domain":
        raise ValueError("The passed path does not point to the correct node.")

    try:
        tree.find(path + "/x_min").text = str(new_values["x_min"])
        tree.find(path + "/x_max").text = str(new_values["x_max"])
        tree.find(path + "/y_min").text = str(new_values["y_min"])
        tree.find(path + "/y_max").text = str(new_values["y_max"])
        tree.find(path + "/z_min").text = str(new_values["z_min"])
        tree.find(path + "/z_max").text = str(new_values["z_max"])
        tree.find(path + "/dx").text = str(new_values["dx"])
        tree.find(path + "/dy").text = str(new_values["dy"])
        tree.find(path + "/dz").text = str(new_values["dz"])
        if new_values["use_2d"]:
            tree.find(path + "/use_2D").text = "true"
        else:
            tree.find(path + "/use_2D").text = "false"

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_overall(new_values: Dict[str, float], tree: ElementTree, path: str) -> None:
    """
    Writes new values for the <overall> data in the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the overall variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the overall node (e.g., "overall").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid overall node.
    """
    if tree.find(path).tag != "overall":
        raise ValueError("The passed path does not point to the correct node.")

    try:
        tree.find(path + "/max_time").text = str(new_values["max_time"])
        tree.find(path + "/dt_diffusion").text = str(new_values["dt_diffusion"])
        tree.find(path + "/dt_mechanics").text = str(new_values["dt_mechanics"])
        tree.find(path + "/dt_phenotype").text = str(new_values["dt_phenotype"])

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_substance(new_values, tree: ElementTree, path: str, name: str) -> None:
    """
    Writes new values for a microenvironment substance the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the substance variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the microenvironment node (e.g., "microenvironment_setup").
    name:
        A string with the name of the substance to be written.

    Raises
    ------
    ValueError
        When the passed path does not point to the valid microenvironment node.
    ValueError
        When the passed name does not match any of the substances in the file.
    """
    if tree.find(path).tag != "microenvironment_setup":
        raise ValueError("The passed path does not point to the correct node.")

    substances = [
        substance.attrib["name"] for substance in tree.find(path).findall("variable")
    ]

    if name not in substances:
        raise ValueError("The passed substance name is not valid.")

    try:
        substance_stem = path + f"/variable[@name='{name}']"
        tree.find(
            substance_stem + "/physical_parameter_set/diffusion_coefficient"
        ).text = str(new_values["diffusion_coefficient"])
        tree.find(substance_stem + "/physical_parameter_set/decay_rate").text = str(
            new_values["decay_rate"]
        )
        tree.find(substance_stem + "/initial_condition").text = str(
            new_values["initial_condition"]
        )
        tree.find(substance_stem + "/Dirichlet_boundary_condition").text = str(
            new_values["dirichlet_boundary_condition"]
        )

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_cycle(
    new_values: Dict[str, Union[float, List[float]]], tree: ElementTree, path: str
) -> None:
    """
    Writes new values for the <cycle> data in the XML tree.
    The phase durations or rates should have the same length as the XML file.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the cycle variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the cycle node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/cycle").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid cycle node.
    ValueError
        When the number of transition rates/durations does not match the values
        in the XML file.
    """
    if tree.find(path).tag != "cycle":
        raise ValueError("The passed path does not point to the correct node.")

    try:
        if tree.find(path + "/phase_durations"):
            durations = list(tree.find(path + "/phase_durations"))
            new_durations = new_values["phase_durations"]

            if len(durations) != len(new_durations):
                raise ValueError(
                    "The length of the durations list does not match the XML file."
                )

            for new_value, element in zip(new_durations, durations):
                element.text = str(new_value)
        else:
            rates = list(tree.find(path + "/phase_transition_rates"))
            new_rates = new_values["phase_transition_rates"]

            if len(rates) != len(new_rates):
                raise ValueError(
                    "The length of the rates list does not match the XML file."
                )

            for new_value, element in zip(new_rates, rates):
                element.text = str(new_value)

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_death_model(
    new_values: Dict[str, Union[float, List[float]]], tree: ElementTree, path: str
) -> None:
    """
    Writes new values for a <death> model in the XML tree.
    The phase durations or rates should have the same length as the XML file.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the death variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the death node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/death").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid death node.
    ValueError
        When the passed name does not match any of the death models in the XML file.
    ValueError
        When the number of transition rates/durations does not match the values
        in the XML file.
    """
    if tree.find(path).tag != "death":
        raise ValueError("The passed path does not point to the correct node.")

    name = new_values["name"]
    models = [model.attrib["name"] for model in tree.find(path).findall("model")]
    if name not in models:
        raise ValueError("The passed name does not match a valid death model.")

    try:
        model_stem = path + f"/model[@name='{name}']"
        tree.find(model_stem + "/death_rate").text = str(new_values["death_rate"])

        if tree.find(model_stem + "/phase_durations"):
            durations = list(tree.find(model_stem + "/phase_durations"))
            new_durations = new_values["phase_durations"]

            if len(durations) != len(new_durations):
                raise ValueError(
                    "The length of the durations list does not match the XML file."
                )

            for new_value, element in zip(new_durations, durations):
                element.text = str(new_value)

        else:
            rates = list(tree.find(model_stem + "/phase_transition_rates"))
            new_rates = new_values["phase_transition_rates"]

            if len(rates) != len(new_rates):
                raise ValueError(
                    "The length of the rates list does not match the XML file."
                )

            for new_value, element in zip(new_rates, rates):
                element.text = str(new_value)

        tree.find(model_stem + "/parameters/unlysed_fluid_change_rate").text = str(
            new_values["unlysed_fluid_change_rate"]
        )
        tree.find(model_stem + "/parameters/lysed_fluid_change_rate").text = str(
            new_values["lysed_fluid_change_rate"]
        )
        tree.find(
            model_stem + "/parameters/cytoplasmic_biomass_change_rate"
        ).text = str(new_values["cytoplasmic_biomass_change_rate"])
        tree.find(model_stem + "/parameters/nuclear_biomass_change_rate").text = str(
            new_values["nuclear_biomass_change_rate"]
        )
        tree.find(model_stem + "/parameters/calcification_rate").text = str(
            new_values["calcification_rate"]
        )
        tree.find(model_stem + "/parameters/relative_rupture_volume").text = str(
            new_values["relative_rupture_volume"]
        )

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_volume(new_values: Dict[str, float], tree: ElementTree, path: str) -> None:
    """
    Writes new values for the <volume> data in the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the volume variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the volume node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/volume").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid volume node.
    """
    if tree.find(path).tag != "volume":
        raise ValueError("The passed path does not point to the correct node.")

    try:
        tree.find(path + "/total").text = str(new_values["total"])
        tree.find(path + "/fluid_fraction").text = str(new_values["fluid_fraction"])
        tree.find(path + "/nuclear").text = str(new_values["nuclear"])
        tree.find(path + "/fluid_change_rate").text = str(
            new_values["fluid_change_rate"]
        )
        tree.find(path + "/cytoplasmic_biomass_change_rate").text = str(
            new_values["cytoplasmic_biomass_change_rate"]
        )
        tree.find(path + "/nuclear_biomass_change_rate").text = str(
            new_values["nuclear_biomass_change_rate"]
        )
        tree.find(path + "/calcified_fraction").text = str(
            new_values["calcified_fraction"]
        )
        tree.find(path + "/calcification_rate").text = str(
            new_values["calcification_rate"]
        )
        tree.find(path + "/relative_rupture_volume").text = str(
            new_values["relative_rupture_volume"]
        )

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_mechanics(new_values: Dict[str, float], tree: ElementTree, path: str) -> None:
    """
    Writes new values for the <mechanics> data in the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the mechanics variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the mechanics node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/mechanics").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid mechanics node.
    """
    if tree.find(path).tag != "mechanics":
        raise ValueError("The passed path does not point to the correct node.")

    try:
        tree.find(path + "/cell_cell_adhesion_strength").text = str(
            new_values["cell_cell_adhesion_strength"]
        )
        tree.find(path + "/cell_cell_repulsion_strength").text = str(
            new_values["cell_cell_repulsion_strength"]
        )
        tree.find(path + "/relative_maximum_adhesion_distance").text = str(
            new_values["relative_maximum_adhesion_distance"]
        )
        tree.find(path + "/options/set_relative_equilibrium_distance").text = str(
            new_values["set_relative_equilibrium_distance"]
        )
        tree.find(path + "/options/set_absolute_equilibrium_distance").text = str(
            new_values["set_absolute_equilibrium_distance"]
        )

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_motility(
    new_values: Dict[str, Union[float, bool, str]], tree: ElementTree, path: str
) -> None:
    """
    Writes new values for the <motility> data in the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the motility variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the motility node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/motility").

    Raises
    ------
    ValueError
        When the passed path does not point to the valid motility node.
    """
    if tree.find(path).tag != "motility":
        raise ValueError("The passed path does not point to the correct node.")

    try:
        tree.find(path + "/speed").text = str(new_values["speed"])
        tree.find(path + "/persistence_time").text = str(new_values["persistence_time"])
        tree.find(path + "/migration_bias").text = str(new_values["migration_bias"])

        if new_values["motility_enabled"]:
            tree.find(path + "/options/enabled").text = "true"
        else:
            tree.find(path + "/options/enabled").text = "false"

        if new_values["use_2d"]:
            tree.find(path + "/options/use_2D").text = "true"
        else:
            tree.find(path + "/options/use_2D").text = "false"

        chemo_str = path + "/options/chemotaxis"

        if new_values["chemotaxis_enabled"]:
            tree.find(chemo_str + "/enabled").text = "true"
        else:
            tree.find(chemo_str + "/enabled").text = "false"

        tree.find(chemo_str + "/substrate").text = new_values["chemotaxis_substrate"]
        tree.find(chemo_str + "/direction").text = str(
            new_values["chemotaxis_direction"]
        )

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_secretion_substance(
    new_values, tree: ElementTree, path: str, name: str
) -> None:
    """
    Writes new values for a secretion substance the XML tree.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A dictionary with the name of the substance variables and their
        values (must include all the variables).
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the microenvironment node
        (e.g., "cell_definitions/cell_definition[@name='default']/phenotype/secretion").
    name:
        A string with the name of the substance to be written.

    Raises
    ------
    ValueError
        When the passed path does not point to the valid microenvironment node.
    ValueError
        When the passed name does not match any of the substances in the file.
    """
    if tree.find(path).tag != "secretion":
        raise ValueError("The passed path does not point to the correct node.")

    substances = [
        substance.attrib["name"] for substance in tree.find(path).findall("substrate")
    ]

    if name not in substances:
        raise ValueError("The passed substance name is not valid.")

    try:
        stem = path + f"/substrate[@name='{name}']"
        tree.find(stem + "/secretion_rate").text = str(new_values["secretion_rate"])
        tree.find(stem + "/secretion_target").text = str(new_values["secretion_target"])
        tree.find(stem + "/uptake_rate").text = str(new_values["uptake_rate"])
        tree.find(stem + "/net_export_rate").text = str(new_values["net_export_rate"])

    except KeyError:
        print("The passed dictionary does not have all the domain variables.")


def write_custom_data(
    new_values: List[Dict[str, float]], tree: ElementTree, path: str
) -> None:
    """
    Writes new values to the custom user variables in the XML tree.
    The list must match the custom variables in the XML file.
    Values will not be saved to the XML file, only to the ElementTree.

    Parameters
    ----------
    new_values:
        A list of dictionaries with the custom variables to be written.
    tree:
        A ElementTree object of the XML config file to be written.
    path:
        A string with the path to the motility node
        (e.g., "cell_definitions/cell_definition[@name='default']/custom_data", "user_parameters").

    Raises
    ------
    ValueError
        When the passed path does not point to a valid custom node.
    ValueError
        When the passed list does not match the variables in the config file.
    """
    if (tree.find(path).tag != "custom_data") & (
        tree.find(path).tag != "user_parameters"
    ):
        raise ValueError("The passed path does not point to the correct node.")

    variables_names = [var.tag for var in list(tree.find(path)) if var.text]
    new_variables_names = [var["name"] for var in new_values]

    if variables_names != new_variables_names:
        raise ValueError("The custom variables do not match those in the XML file.")

    for variable in new_values:
        tree.find(path + f"/{variable['name']}").text = str(variable["value"])
