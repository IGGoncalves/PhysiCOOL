"""Script to test the config module of the PhysiCOOL package."""
import unittest
from pathlib import Path

from physicool import config

CONFIG_PATH = Path("PhysiCell/config/settings_read_only.xml")


class PhysiCellConfigTest(unittest.TestCase):
    def setUp(self):
        """Creates and stores a parser object to read data from the config file."""
        self.xml_data = config.ConfigFileParser(CONFIG_PATH)

    def test_get_cell_definition_list(self):
        """Asserts that the cell definitions extracted from the config file are correct."""
        cell_list = self.xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default"])

    def test_read_volume_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_values = [2494.0, 0.75, 540.0, 0.05, 0.0045, 0.0055, 0.0, 0.0, 2.0]

        volume_data = self.xml_data.read_volume_params("default")
        parsed_data = [
            volume_data.total_volume,
            volume_data.fluid_fraction,
            volume_data.nuclear,
            volume_data.fluid_change_rate,
            volume_data.cyto_bio_rate,
            volume_data.nuclear_bio_rate,
            volume_data.calcified_fraction,
            volume_data.calcification_rate,
            volume_data.rupture_volume,
        ]

        self.assertEqual(expected_values, parsed_data)

    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        expected_values = [0.4, 10.0, 1.25]
        mechanics_data = self.xml_data.read_mechanics_params("default")

        parsed_data = [
            mechanics_data.adhesion_strength,
            mechanics_data.repulsion_strength,
            mechanics_data.adhesion_distance,
        ]

        self.assertEqual(expected_values, parsed_data)

    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        expected_values = [1.0, 1.0, 0.5, False, True, False, "substrate", 1.0]
        motility_data = self.xml_data.read_motility_params("default")

        parsed_data = [
            motility_data.speed,
            motility_data.persistence,
            motility_data.bias,
            motility_data.motility_enabled,
            motility_data.use_2d,
            motility_data.chemo_enabled,
            motility_data.chemo_substrate,
            motility_data.chemo_direction,
        ]

        self.assertEqual(expected_values, parsed_data)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        expected_values = {"substrate": [0.0, 1.0, 0.0, 0.0],
        "oxygen": [0.0, 1.0, 0.0, 0.0]}
        secretion_data = self.xml_data.read_secretion_params("default")

        parsed_data = {
            substance.name: [
                substance.secretion_rate,
                substance.secretion_target,
                substance.uptake_rate,
                substance.net_export_rate,
            ]
            for substance in secretion_data
        }

        self.assertEqual(expected_values, parsed_data)


if __name__ == "__main__":
    unittest.main()
