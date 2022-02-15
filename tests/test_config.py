"""Script to test the config module of the PhysiCOOL package."""
import unittest

from physicool import config


class PhysiCellConfigTest(unittest.TestCase):
    def test_get_cell_definition_list(self):
        """Asserts that the cell definitions extracted from the config file are correct."""
        xml_data = config.ConfigFileParser()
        cell_list = xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default"])

    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        mechanics_data = config.ConfigFileParser().read_mechanics_params("default")
        self.assertEqual(mechanics_data.cell_cell_adhesion_strength, 0.4)
        self.assertEqual(mechanics_data.cell_cell_repulsion_strength, 10.0)
        self.assertEqual(mechanics_data.relative_maximum_adhesion_distance, 1.25)


    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        motility_data = config.ConfigFileParser().read_motility_params("default")
        self.assertEqual(motility_data.speed, 1.0)
        self.assertEqual(motility_data.persistence_time, 1.0)
        self.assertEqual(motility_data.bias, 0.5)
        self.assertEqual(motility_data.motility_enabled, False)
        self.assertEqual(motility_data.use_2d, True)
        self.assertEqual(motility_data.chemotaxis_enabled, False)
        self.assertEqual(motility_data.chemotaxis_substrate, "substrate")
        self.assertEqual(motility_data.chemotaxis_direction, 1.0)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        secretion_data = config.ConfigFileParser().read_secretion_params("default", "substrate")
        self.assertEqual(secretion_data.secretion_rate, 0.0)
        self.assertEqual(secretion_data.secretion_target, 1.0)
        self.assertEqual(secretion_data.uptake_rate, 0.0)
        self.assertEqual(secretion_data.net_export_rate, 0.0)


if __name__ == '__main__':
    unittest.main()
