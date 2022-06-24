"""Script to test the config module of the PhysiCOOL package."""
import unittest
from pathlib import Path
from xml.etree import ElementTree

from physicool import config

CONFIG_PATH = Path("PhysiCell/config/settings_read_only.xml")

EXPECTED_OVERALL_READ = {
    "max_time": 620.0,
    "dt_diffusion": 0.01,
    "dt_mechanics": 0.1,
    "dt_phenotype": 6,
}

EXPECTED_SUBSTANCE_READ = {
    "name": "substrate",
    "diffusion_coefficient": 100000.0,
    "decay_rate": 10.0,
    "initial_condition": 0.0,
    "dirichlet_boundary_condition": 0.0,
}

EXPECTED_CYCLE_DURATIONS_READ = {
    "code": 6,
    "phase_durations": [300.0, 480.0, 240.0, 60.0],
    "phase_transition_rates": None,
}
EXPECTED_CYCLE_RATES_READ = {
    "code": 6,
    "phase_durations": None,
    "phase_transition_rates": [0.00334672, 0.00208333, 0.00416667, 0.0166667],
}

EXPECTED_DEATH_APOPTOSIS_READ = {
    "code": 100,
    "phase_durations": [516],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_DEATH_NECROSIS_READ = {
    "code": 101,
    "phase_durations": [0.0, 86400],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_VOLUME_READ = {
    "total": 2494.0,
    "fluid_fraction": 0.75,
    "nuclear": 540.0,
    "fluid_change_rate": 0.05,
    "cytoplasmic_biomass_change_rate": 0.0045,
    "nuclear_biomass_change_rate": 0.0055,
    "calcified_fraction": 0.0,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_MOTILITY_READ = {
    "speed": 1.0,
    "persistence": 1.0,
    "bias": 0.5,
    "motility_enabled": False,
    "use_2d": True,
    "chemotaxis_enabled": False,
    "chemotaxis_substrate": "substrate",
    "chemotaxis_direction": 1.0,
}

EXPECTED_MECHANICS_READ = {
    "cell_cell_adhesion_strength": 0.4,
    "cell_cell_repulsion_strength": 10.0,
    "relative_maximum_adhesion_distance": 1.25,
    "set_relative_equilibrium_distance": 1.8,
    "set_absolute_equilibrium_distance": 15.12,
}

EXPECTED_SECRETION_READ_SUBSTRATE = {
    "name": "substrate",
    "secretion_rate": 0.0,
    "secretion_target": 1.0,
    "uptake_rate": 0.0,
    "net_export_rate": 0.0,
}

EXPECTED_SECRETION_READ_OXYGEN = {
    "name": "oxygen",
    "secretion_rate": 0.0,
    "secretion_target": 1.0,
    "uptake_rate": 0.0,
    "net_export_rate": 0.0,
}

EXPECTED_SECRETION_READ = [
    EXPECTED_SECRETION_READ_SUBSTRATE,
    EXPECTED_SECRETION_READ_OXYGEN,
]

EXPECTED_CUSTOM_READ = [{"name": "sample", "value": 1.0}]

EXPECTED_USER_PARAMETERS_READ = [
    {"name": "random_seed", "value": 0.0},
    {"name": "number_of_cells", "value": 5.0},
]


class ReadDataTest(unittest.TestCase):
    def setUp(self):
        self.tree = ElementTree.parse(CONFIG_PATH)

    def test_parse_overall(self):
        data = config.parse_overall(tree=self.tree, path="overall")
        self.assertEqual(EXPECTED_OVERALL_READ, data)

    def test_parse_substance(self):
        data = config.parse_substance(tree=self.tree, path="microenvironment_setup", name="substrate")
        self.assertEqual(EXPECTED_SUBSTANCE_READ, data)

    def test_parse_me(self):
        data = config.parse_microenvironment(tree=self.tree, path="microenvironment_setup")
        self.assertEqual([EXPECTED_SUBSTANCE_READ], data)


class PhysiCellConfigTest(unittest.TestCase):
    def setUp(self):
        """Creates and stores a parser object to read data from the config file."""
        self.xml_data = config.ConfigFileParser(CONFIG_PATH)

    def test_get_cell_definition_list(self):
        """Asserts that the cell definitions extracted from the config file are correct."""
        cell_list = self.xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default", "cancer"])

    def test_read_overall_data(self):
        expected_data = config.Overall(**EXPECTED_OVERALL_READ)
        overall_data = self.xml_data.read_overall_data()
        self.assertEqual(expected_data, overall_data)

    def test_read_me_data(self):
        expected_data = [config.Substance(**EXPECTED_SUBSTANCE_READ)]
        me_data = self.xml_data.read_me_data()
        self.assertEqual(expected_data, me_data)

    def test_read_cycle_durations_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = config.Cycle(**EXPECTED_CYCLE_DURATIONS_READ)
        cycle_data = self.xml_data.read_cycle_params("default")
        self.assertEqual(expected_data, cycle_data)

    def test_read_cycle_rates_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = config.Cycle(**EXPECTED_CYCLE_RATES_READ)
        cycle_data = self.xml_data.read_cycle_params("cancer")
        self.assertEqual(expected_data, cycle_data)

    def test_read_death(self):
        expected_data = [
            config.Death(**EXPECTED_DEATH_APOPTOSIS_READ),
            config.Death(**EXPECTED_DEATH_NECROSIS_READ),
        ]
        death_data = self.xml_data.read_death_params("default")
        self.assertEqual(expected_data, death_data)

    def test_read_volume_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = config.Volume(**EXPECTED_VOLUME_READ)
        volume_data = self.xml_data.read_volume_params("default")
        self.assertEqual(expected_data, volume_data)

    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        expected_data = config.Mechanics(**EXPECTED_MECHANICS_READ)
        mechanics_data = self.xml_data.read_mechanics_params("default")
        self.assertEqual(expected_data, mechanics_data)

    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        expected_data = config.Motility(**EXPECTED_MOTILITY_READ)
        motility_data = self.xml_data.read_motility_params("default")
        self.assertEqual(expected_data, motility_data)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        expected_data = [
            config.Secretion(**EXPECTED_SECRETION_READ_SUBSTRATE),
            config.Secretion(**EXPECTED_SECRETION_READ_OXYGEN),
        ]
        secretion_data = self.xml_data.read_secretion_params("default")
        self.assertEqual(expected_data, secretion_data)

    def test_read_custom_params(self):
        expected_data = [config.CustomData(**custom) for custom in EXPECTED_CUSTOM_READ]
        custom_data = self.xml_data.read_custom_data("default")
        self.assertEqual(expected_data, custom_data)

    def test_read_user_parameters(self):
        expected_data = [
            config.CustomData(**custom) for custom in EXPECTED_USER_PARAMETERS_READ
        ]
        user_data = self.xml_data.read_user_parameters()
        self.assertEqual(expected_data, user_data)


if __name__ == "__main__":
    unittest.main()
