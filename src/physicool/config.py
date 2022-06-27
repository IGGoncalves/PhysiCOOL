# This module enables users to programmatically modify their PhysiCell XML config file
from pathlib import Path
from xml.etree import ElementTree
from typing import List, Union

import physicool.datatypes as dt
from physicool import pcxml


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

    def read_domain_params(self) -> dt.Domain:
        return dt.Domain(**pcxml.parse_domain(tree=self.tree, path="domain"))

    def read_overall_params(self) -> dt.Overall:
        return dt.Overall(**pcxml.parse_overall(tree=self.tree, path="overall"))

    def read_me_params(self) -> List[dt.Substance]:
        return [
            dt.Substance(**substance)
            for substance in pcxml.parse_microenvironment(
                tree=self.tree, path="microenvironment_setup"
            )
        ]

    def read_cycle_params(self, name: str) -> dt.Cycle:
        # Build basic string stem to find motility cell data for cell definition
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/cycle"
        return dt.Cycle(**pcxml.parse_cycle(self.tree, path=stem))

    def read_death_params(self, name: str) -> List[dt.Death]:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/death"
        return [dt.Death(**model) for model in pcxml.parse_death(self.tree, path=stem)]

    def read_volume_params(self, name: str) -> dt.Volume:
        """Reads the motility parameters from the config file into a custom data structure"""
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/volume"
        return dt.Volume(**pcxml.parse_volume(tree=self.tree, path=stem))

    def read_mechanics_params(self, name: str) -> dt.Mechanics:
        """Reads the mechanics parameters from the config file into a custom data structure"""
        # Build basic string stem to find mechanics cell data for cell definition
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/mechanics"
        return dt.Mechanics(**pcxml.parse_mechanics(tree=self.tree, path=stem))

    def read_motility_params(self, name: str) -> dt.Motility:
        """Reads the motility parameters from the config file into a custom data structure"""
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/motility"
        return dt.Motility(**pcxml.parse_motility(tree=self.tree, path=stem))

    def read_secretion_params(self, name: str) -> List[dt.Secretion]:
        """Reads the secretion parameters from the config file into a custom data structure"""
        # Build basic string stem to find secretion cell data for cell definition
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/secretion"
        return [
            dt.Secretion(**substance)
            for substance in pcxml.parse_secretion(tree=self.tree, path=stem)
        ]

    def read_custom_data(self, name: str) -> List[dt.CustomData]:
        stem = f"cell_definitions/cell_definition[@name='{name}']/custom_data"
        return [dt.CustomData(**custom) for custom in pcxml.parse_custom(self.tree, stem)]

    def read_cell_data(self, name: str = "default") -> dt.CellParameters:
        """
        Reads all the fields for a given cell definition into a custom cell data type.

        Parameters
        ----------
        name: str, default "default"
            The name of the cell definition to be read

        Returns
        -------
        dt.CellParameters
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
            cycle = self.read_cycle_params(name)
            death = self.read_death_params(name)
            volume = self.read_volume_params(name)
            mechanics = self.read_mechanics_params(name)
            motility = self.read_motility_params(name)
            secretion = self.read_secretion_params(name)

            return dt.CellParameters(
                name, cycle, death, volume, mechanics, motility, secretion
            )

        except ValueError as ve:
            print(ve)

    def read_user_params(self):
        return [
            dt.CustomData(**custom)
            for custom in pcxml.parse_custom(self.tree, "user_parameters")
        ]

    def write_domain_params(self, domain: dt.Domain, update_file: bool = True) -> None:
        pcxml.write_domain(new_values=domain.dict(), tree=self.tree, path="domain")
        if update_file:
            self.tree.write(self.config_file)

    def write_overall_params(self, overall: dt.Overall, update_file: bool = True) -> None:
        pcxml.write_overall(new_values=overall.dict(), tree=self.tree, path="overall")
        if update_file:
            self.tree.write(self.config_file)

    def write_substance_params(
            self, substance: dt.Substance, update_file: bool = True
    ) -> None:
        pcxml.write_substance(
            new_values=substance.dict(),
            tree=self.tree,
            path="microenvironment_setup",
            name=substance.name,
        )
        if update_file:
            self.tree.write(self.config_file)

    def write_cycle_params(
            self, name: str, cycle: dt.Cycle, update_file: bool = True
    ) -> None:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/cycle"
        pcxml.write_cycle(new_values=cycle.dict(), tree=self.tree, path=stem)
        if update_file:
            self.tree.write(self.config_file)

    def write_death_model_params(self, name: str, death: dt.Death, model_name: str, update_file: bool = True) -> None:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/death"
        pcxml.write_death_model(new_values=death.dict(), tree=self.tree, path=stem, name=model_name)
        if update_file:
            self.tree.write(self.config_file)

    def write_motility_params(self, name: str, motility: dt.Motility, update_file: bool = True) -> None:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/motility"
        pcxml.write_motility(new_values=motility.dict(), tree=self.tree, path=stem)
        if update_file:
            self.tree.write(self.config_file)

    def write_mechanics_params(self, name: str, mechanics: dt.Mechanics, update_file: bool = True) -> None:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/mechanics"
        pcxml.write_mechanics(new_values=mechanics.dict(), tree=self.tree, path=stem)
        self.tree.write(self.config_file)
        if update_file:
            self.tree.write(self.config_file)

    def write_volume_params(self, name: str, volume: dt.Volume, update_file: bool = True) -> None:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/volume"
        pcxml.write_volume(new_values=volume.dict(), tree=self.tree, path=stem)
        self.tree.write(self.config_file)
        if update_file:
            self.tree.write(self.config_file)

    def write_secretion_params(self, name: str, death: dt.Death, substance: str, update_file: bool = True) -> None:
        stem = f"cell_definitions/cell_definition[@name='{name}']/phenotype/secretion"
        pcxml.write_secretion_substance(new_values=death.dict(), tree=self.tree, path=stem, name=substance)
        if update_file:
            self.tree.write(self.config_file)

    def write_custom_params(self, name: str, custom_data: List[dt.CustomData], update_file: bool = True):
        stem = f"cell_definitions/cell_definition[@name='{name}']/custom_data"
        data = [variable.dict() for variable in custom_data]
        pcxml.write_custom_data(new_values=data, tree=self.tree, path=stem)
        if update_file:
            self.tree.write(self.config_file)

    def write_user_params(self, custom_data: List[dt.CustomData], update_file: bool = True):
        data = [variable.dict() for variable in custom_data]
        pcxml.write_custom_data(new_values=data, tree=self.tree, path="user_parameters")
        if update_file:
            self.tree.write(self.config_file)

    def update_params(self, cell_data: dt.CellParameters) -> None:
        """
        Writes the new parameters to the XML tree object and also updates the XML file.

        Parameters
        ----------
        new_parameters: dt.CellParameters
            The new cell parameters to be writeen to the XML file.
        """
        self.write_motility_params(cell_data.name, cell_data.motility)
        self.write_cycle_params(cell_data.name, cell_data.phenotype.cycle)
