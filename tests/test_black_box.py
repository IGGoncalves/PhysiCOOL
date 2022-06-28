import unittest

from physicool.datatypes import *
from physicool import updaters

CELL_DATA = {
    "name": "default",
    "cycle": {
        "code": 6.0,
        "phase_durations": [300.0, 480.0, 240.0, 60.0],
        "phase_transition_rates": None,
    },
    "death": [
        {
            "code": 100.0,
            "name": "apoptosis",
            "death_rate": 5.31667e-05,
            "phase_durations": [516.0],
            "phase_transition_rates": None,
            "unlysed_fluid_change_rate": 0.05,
            "lysed_fluid_change_rate": 0.0,
            "cytoplasmic_biomass_change_rate": 0.0166667,
            "nuclear_biomass_change_rate": 0.00583333,
            "calcification_rate": 0.0,
            "relative_rupture_volume": 2.0,
        },
        {
            "code": 101.0,
            "name": "necrosis",
            "death_rate": 0.0,
            "phase_durations": [0.0, 86400.0],
            "phase_transition_rates": None,
            "unlysed_fluid_change_rate": 0.05,
            "lysed_fluid_change_rate": 0.0,
            "cytoplasmic_biomass_change_rate": 0.0166667,
            "nuclear_biomass_change_rate": 0.00583333,
            "calcification_rate": 0.0,
            "relative_rupture_volume": 2.0,
        },
    ],
    "volume": {
        "total": 2494.0,
        "fluid_fraction": 0.75,
        "nuclear": 540.0,
        "fluid_change_rate": 0.05,
        "cytoplasmic_biomass_change_rate": 0.0045,
        "nuclear_biomass_change_rate": 0.0055,
        "calcified_fraction": 0.0,
        "calcification_rate": 0.0,
        "relative_rupture_volume": 2.0,
    },
    "mechanics": {
        "cell_cell_adhesion_strength": 0.4,
        "cell_cell_repulsion_strength": 10.0,
        "relative_maximum_adhesion_distance": 1.25,
        "set_relative_equilibrium_distance": 1.8,
        "set_absolute_equilibrium_distance": 15.12,
    },
    "motility": {
        "speed": 1.0,
        "persistence_time": 1.0,
        "migration_bias": 0.5,
        "motility_enabled": False,
        "use_2d": True,
        "chemotaxis_enabled": False,
        "chemotaxis_substrate": "substrate",
        "chemotaxis_direction": 1.0,
    },
    "secretion": [
        {
            "name": "substrate",
            "secretion_rate": 0.0,
            "secretion_target": 1.0,
            "uptake_rate": 0.0,
            "net_export_rate": 0.0,
        },
        {
            "name": "oxygen",
            "secretion_rate": 0.0,
            "secretion_target": 1.0,
            "uptake_rate": 0.0,
            "net_export_rate": 0.0,
        },
    ],
    "custom": [{"name": "sample", "value": 1.0}],
}


EXPECTED_MOTILITY_WRITE = Motility(
    speed=5.0,
    persistence_time=10.0,
    migration_bias=1.0,
    motility_enabled=False,
    use_2d=True,
    chemotaxis_enabled=False,
    chemotaxis_substrate="substrate",
    chemotaxis_direction=1.0,
)

EXPECTED_MOTILITY_WRITE_2 = EXPECTED_MOTILITY_WRITE.copy(deep=True)
EXPECTED_MOTILITY_WRITE_2.migration_bias = 0.5


class UpdaterFunctionsTest(unittest.TestCase):
    def test_motility_updater_function(self):
        """Asserts that the motility parameters are correctly updated."""
        data = CellParameters(**CELL_DATA)
        new_motility_values = {
            "speed": 5.0,
            "persistence_time": 10.0,
            "migration_bias": 1.0,
        }
        updaters.update_motility_values(cell_data=data, new_values=new_motility_values)
        self.assertEqual(EXPECTED_MOTILITY_WRITE, data.motility)

    def test_motility_updater_function_incomplete(self):
        """Asserts that the motility parameters are correctly updated when not all parameters are defined."""
        data = CellParameters(**CELL_DATA)
        new_motility_values = {"speed": 5.0, "persistence_time": 10.0}
        updaters.update_motility_values(cell_data=data, new_values=new_motility_values)
        self.assertEqual(EXPECTED_MOTILITY_WRITE_2, data.motility)


class SimpleBlackBoxTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == "__main__":
    unittest.main()
