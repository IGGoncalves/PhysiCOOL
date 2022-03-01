"""Script to test the config module of the PhysiCOOL package."""
import unittest
from pathlib import Path

from physicool import config

CONFIG_PATH = Path("PhysiCell/config/settings_read_only.xml")

class PhysiCellConfigTest(unittest.TestCase):
    def test_get_cell_definition_list(self):
        """Asserts that the cell definitions extracted from the config file are correct."""
        xml_data = config.ConfigFileParser(CONFIG_PATH)
        cell_list = xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default"])

    def test_read_volume_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        volume_data = config.ConfigFileParser(CONFIG_PATH).read_volume_params("default")
        self.assertEqual(volume_data.total_volume, 2494.0)
        self.assertEqual(volume_data.fluid_fraction, 0.75)
        self.assertEqual(volume_data.nuclear, 540.0)
        self.assertEqual(volume_data.fluid_change_rate, 0.05)
        self.assertEqual(volume_data.cyto_bio_rate, 0.0045)
        self.assertEqual(volume_data.nuclear_bio_rate, 0.0055)
        self.assertEqual(volume_data.calcified_fraction, 0.0)
        self.assertEqual(volume_data.calcification_rate, 0.0)
        self.assertEqual(volume_data.rupture_volume, 2.0)


    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        mechanics_data = config.ConfigFileParser(CONFIG_PATH).read_mechanics_params("default")
        self.assertEqual(mechanics_data.adhesion_strength, 0.4)
        self.assertEqual(mechanics_data.repulsion_strength, 10.0)
        self.assertEqual(mechanics_data.adhesion_distance, 1.25)

    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        motility_data = config.ConfigFileParser(CONFIG_PATH).read_motility_params("default")
        self.assertEqual(motility_data.speed, 1.0)
        self.assertEqual(motility_data.persistence, 1.0)
        self.assertEqual(motility_data.bias, 0.5)
        self.assertEqual(motility_data.motility_enabled, False)
        self.assertEqual(motility_data.use_2d, True)
        self.assertEqual(motility_data.chemo_enabled, False)
        self.assertEqual(motility_data.chemo_substrate, "substrate")
        self.assertEqual(motility_data.chemo_direction, 1.0)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        secretion_data = config.ConfigFileParser(CONFIG_PATH).read_secretion_params("default")
        self.assertEqual(secretion_data.secretion_rate, 0.0)
        self.assertEqual(secretion_data.secretion_target, 1.0)
        self.assertEqual(secretion_data.uptake_rate, 0.0)
        self.assertEqual(secretion_data.net_export_rate, 0.0)


if __name__ == '__main__':
    unittest.main()
