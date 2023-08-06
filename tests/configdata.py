"""Data to be used in the unit tests for the ConfigFileParser and the pcxml module."""
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "data/settings_read_only.xml"
WRITE_PATH = Path("test.xml")

EXPECTED_DOMAIN_READ = {
    "x_min": -500.0,
    "x_max": 500.0,
    "y_min": -500.0,
    "y_max": 500.0,
    "z_min": -10.0,
    "z_max": 10.0,
    "dx": 20.0,
    "dy": 20.0,
    "dz": 20.0,
    "use_2d": True,
}

EXPECTED_DOMAIN_WRITE = {
    "x_min": -200.0,
    "x_max": 200.0,
    "y_min": -500.0,
    "y_max": 500.0,
    "z_min": -10.0,
    "z_max": 10.0,
    "dx": 20.0,
    "dy": 20.0,
    "dz": 20.0,
    "use_2d": False,
}

EXPECTED_OVERALL_READ = {
    "max_time": 620.0,
    "dt_diffusion": 0.01,
    "dt_mechanics": 0.1,
    "dt_phenotype": 6.0,
}

EXPECTED_OVERALL_WRITE = {
    "max_time": 120.0,
    "dt_diffusion": 0.01,
    "dt_mechanics": 0.1,
    "dt_phenotype": 6.0,
}

EXPECTED_SUBSTANCE_READ = {
    "name": "substrate",
    "diffusion_coefficient": 100000.0,
    "decay_rate": 10.0,
    "initial_condition": 0.0,
    "dirichlet_boundary_condition": 0.0,
}

EXPECTED_SUBSTANCE_WRITE = {
    "name": "substrate",
    "diffusion_coefficient": 400.0,
    "decay_rate": 1.0,
    "initial_condition": 0.0,
    "dirichlet_boundary_condition": 0.0,
}

EXPECTED_CYCLE_DURATIONS_READ = {
    "code": 6.0,
    "phase_durations": [300.0, 480.0, 240.0, 60.0],
    "phase_transition_rates": None,
}

EXPECTED_CYCLE_DURATIONS_WRITE = {
    "code": 6.0,
    "phase_durations": [100.0, 10.0, 240.0, 60.0],
    "phase_transition_rates": None,
}

EXPECTED_CYCLE_RATES_READ = {
    "code": 6.0,
    "phase_durations": None,
    "phase_transition_rates": [0.00334672, 0.00208333, 0.00416667, 0.0166667],
}

EXPECTED_CYCLE_RATES_WRITE = {
    "code": 6.0,
    "phase_durations": None,
    "phase_transition_rates": [0.001, 0.001, 0.00416667, 0.0166667],
}

WRONG_CYCLE_RATES_WRITE = {
    "code": 6.0,
    "phase_durations": None,
    "phase_transition_rates": [0.001, 0.00416667, 0.0166667],
}

EXPECTED_DEATH_APOPTOSIS_READ = {
    "name": "apoptosis",
    "code": 100.0,
    "death_rate": 5.31667e-05,
    "phase_durations": [516],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_DEATH_APOPTOSIS_WRITE = {
    "name": "apoptosis",
    "code": 100.0,
    "death_rate": 5.31667e-05,
    "phase_durations": [518],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.5,
    "relative_rupture_volume": 2.0,
}

EXPECTED_DEATH_NECROSIS_READ = {
    "name": "necrosis",
    "code": 101.0,
    "death_rate": 0.0,
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

EXPECTED_VOLUME_WRITE = {
    "total": 2494.0,
    "fluid_fraction": 0.75,
    "nuclear": 100.0,
    "fluid_change_rate": 0.05,
    "cytoplasmic_biomass_change_rate": 0.0045,
    "nuclear_biomass_change_rate": 0.0055,
    "calcified_fraction": 0.5,
    "calcification_rate": 1.0,
    "relative_rupture_volume": 3.0,
}

EXPECTED_MOTILITY_READ = {
    "speed": 1.0,
    "persistence_time": 1.0,
    "migration_bias": 0.5,
    "motility_enabled": False,
    "use_2d": True,
    "chemotaxis_enabled": False,
    "chemotaxis_substrate": "substrate",
    "chemotaxis_direction": 1.0,
}

EXPECTED_MOTILITY_WRITE = {
    "speed": 12.0,
    "persistence_time": 60.0,
    "migration_bias": 0.5,
    "motility_enabled": True,
    "use_2d": True,
    "chemotaxis_enabled": False,
    "chemotaxis_substrate": "substrate",
    "chemotaxis_direction": 1.0,
}

EXPECTED_MECHANICS_READ = {
    "cell_cell_adhesion_strength": 0.4,
    "cell_cell_repulsion_strength": 10.0,
    "cell_BM_adhesion_strength": 4.0,
    "cell_BM_repulsion_strength": 10.0,
    "cell_adhesion_affinities": {"cell_duration": 1, "cell_transrate": 1.0},
    "attachment_elastic_constant": 0.01,
    "attachment_rate": 0.0,
    "detachment_rate": 0.0,
    "relative_maximum_adhesion_distance": 1.25,
    "set_relative_equilibrium_distance": 1.8,
    "set_absolute_equilibrium_distance": 15.12,
}

EXPECTED_MECHANICS_WRITE = {
    "cell_cell_adhesion_strength": 4.0,
    "cell_cell_repulsion_strength": 100.0,
    "cell_BM_adhesion_strength": 4.0,
    "cell_BM_repulsion_strength": 10.0,
    "cell_adhesion_affinities": {"cell_duration": 1, "cell_transrate": 1.0},
    "attachment_elastic_constant": 0.01,
    "attachment_rate": 0.0,
    "detachment_rate": 0.0,
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

EXPECTED_SECRETION_WRITE_SUBSTRATE = {
    "name": "substrate",
    "secretion_rate": 1.0,
    "secretion_target": 1.0,
    "uptake_rate": 0.0,
    "net_export_rate": 0.0,
}

EXPECTED_CUSTOM_READ = [{"name": "sample", "value": 1.0}]
EXPECTED_CUSTOM_WRITE = [{"name": "sample", "value": 5.0}]

EXPECTED_USER_PARAMETERS_READ = [
    {"name": "random_seed", "value": 0.0},
    {"name": "number_of_cells", "value": 5.0},
]

EXPECTED_USER_PARAMETERS_WRITE = [
    {"name": "random_seed", "value": 1.0},
    {"name": "number_of_cells", "value": 5.0},
]

EXPECTED_CELL_DATA_WRITE = {
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
        "total": 100.0,
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
        "cell_cell_adhesion_strength": 4.0,
        "cell_cell_repulsion_strength": 10.0,
        "cell_BM_adhesion_strength": 4.0,
        "cell_BM_repulsion_strength": 10.0,
        "cell_adhesion_affinities": {"cell_duration": 1, "cell_transrate": 1.0},
        "attachment_elastic_constant": 0.01,
        "attachment_rate": 0.0,
        "detachment_rate": 0.0,
        "relative_maximum_adhesion_distance": 1.25,
        "set_relative_equilibrium_distance": 1.8,
        "set_absolute_equilibrium_distance": 15.12,
    },
    "motility": {
        "speed": 5.0,
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

EXPECTED_CELL_DATA_READ = {
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
        "cell_BM_adhesion_strength": 4.0,
        "cell_BM_repulsion_strength": 10.0,
        "cell_adhesion_affinities": {"cell_duration": 1, "cell_transrate": 1.0},
        "attachment_elastic_constant": 0.01,
        "attachment_rate": 0.0,
        "detachment_rate": 0.0,
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
