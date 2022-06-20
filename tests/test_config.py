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
        expected_data = config.Volume(
            total_volume=2494.0,
            fluid_fraction=0.75,
            nuclear=540.0,
            fluid_change_rate=0.05,
            cyto_bio_rate=0.0045,
            nuclear_bio_rate=0.0055,
            calcified_fraction=0.0,
            calcification_rate=0.0,
            rupture_volume=2.0,
        )

        volume_data = self.xml_data.read_volume_params("default")

        self.assertEqual(expected_data, volume_data)

    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        expected_data = config.Mechanics(
            adhesion_strength=0.4, repulsion_strength=10.0, adhesion_distance=1.25,
            relative_eq_distance=config.BoolSettings(enabled=False, value=1.8),
            absolute_eq_distance=config.BoolSettings(enabled=False, value=15.12)
        )
        mechanics_data = self.xml_data.read_mechanics_params("default")

        self.assertEqual(expected_data, mechanics_data)

    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        expected_data = config.Motility(
            speed=1.0,
            persistence=1.0,
            bias=0.5,
            motility_enabled=False,
            use_2d=True,
            chemo_enabled=False,
            chemo_substrate="substrate",
            chemo_direction=1.0,
        )
        motility_data = self.xml_data.read_motility_params("default")

        self.assertEqual(expected_data, motility_data)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        expected_data = [
            config.Secretion(
                name="substrate",
                secretion_rate=0.0,
                secretion_target=1.0,
                uptake_rate=0.0,
                net_export_rate=0.0,
            ),
            config.Secretion(
                name="oxygen",
                secretion_rate=0.0,
                secretion_target=1.0,
                uptake_rate=0.0,
                net_export_rate=0.0,
            ),
        ]

        secretion_data = self.xml_data.read_secretion_params("default")

        self.assertEqual(expected_data, secretion_data)


if __name__ == "__main__":
    unittest.main()
