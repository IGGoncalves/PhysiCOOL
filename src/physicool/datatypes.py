# This module offers data objects with the expected data types for PhysiCell objects.
# Type and value validation is performed through Pydantic when writing to these objects.
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, confloat, conint


class Domain(BaseModel):
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    dx: conint(ge=0)
    dy: conint(ge=0)
    dz: conint(ge=0)
    use_2d: bool


class Overall(BaseModel):
    max_time: conint(ge=0)
    dt_diffusion: confloat(ge=0)
    dt_mechanics: confloat(ge=0)
    dt_phenotype: confloat(ge=0)


class Substance(BaseModel):
    name: str
    diffusion_coefficient: confloat(ge=0.0)
    decay_rate: confloat(ge=0.0)
    initial_condition: confloat(ge=0.0)
    dirichlet_boundary_condition: confloat(ge=0.0)


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
    persistence_time: confloat(ge=0.0)
    migration_bias: confloat(ge=0.0, le=1.0)
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
    code: float
    phase_durations: Optional[List[confloat(ge=0.0)]]
    phase_transition_rates: Optional[List[confloat(ge=0.0)]]

    class Config:
        validate_assignment = True


class DeathCode(Enum):
    APOPTOSIS = 100
    NECROSIS = 101


class Death(BaseModel):
    code: float
    name: str
    death_rate: confloat(ge=0.0)
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


class CellParameters(BaseModel):
    name: str
    cycle: Cycle
    death: List[Death]
    volume: Volume
    mechanics: Mechanics
    motility: Motility
    secretion: List[Secretion]
    custom: List[CustomData]
