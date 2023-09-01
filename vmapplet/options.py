from collections.abc import Mapping
from typing import Any, Dict, List
import dataclasses as dc
import pathlib
from datetime import date

import toml

from .tools.lsystems import LsystemPaths
from .enums import Observation


def _make_dataclass(cls, data_or_cls):
    return cls(**data_or_cls) if type(data_or_cls) is dict else data_or_cls


@dc.dataclass
class OptionsBase(Mapping):
    def __getitem__(self, key):
        return dc.asdict(self).__getitem__(key)

    def __iter__(self):
        return dc.asdict(self).__iter__()

    def __len__(self):
        return dc.asdict(self).__len__()


@dc.dataclass
class OptionsGeneral(OptionsBase):
    date_start: date = dc.field(default_factory=lambda: date(1994, 1, 1))
    date_end: date = dc.field(default_factory=lambda: date(1998, 6, 30))
    seed: int = 1163078255
    # the second year shoots
    second_year_draws: bool = True
    # Enable rupturing in branches
    ruptures: bool = False
    # Set the trunk on a stake - for all the trunk metamers to remain vertical
    stake: bool = True
    # Select a specific trunk among the 4 trunk sequences available (starts at 0)
    select_trunk: int = 0
    # Enable/Disable the rotation calculations (mechanics)
    mechanics: bool = True
    # render mode  may be bark, observations, zones, reaction_wood, year
    render_mode: str = "bark"
    # should be an integer. This is the number of elements of the shapes (e.g., leaf)
    stride_number: int = 5
    # Set to true to enalbe pruning# otherwise false (added by Liqi Han, 11-10-2011)
    pruning: bool = False
    # TODO
    convergence_steps: int = 2


@dc.dataclass
class OptionsOutput(OptionsBase):
    dates: List[Dict[str, int]] = dc.field(default_factory=lambda: list())
    attributes: Dict[str, List[str]] = dc.field(default_factory=lambda: dict())


@dc.dataclass
class OptionsInput(OptionsBase):
    lpy_files: LsystemPaths = dc.field(default_factory=lambda: dict())
    lpy_path: str = dc.field(
        default_factory=lambda: str(pathlib.Path(__file__).parent.joinpath("lpy"))
    )


@dc.dataclass
class OptionsEvents(OptionsBase):
    bud_break: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=15, month=5, duration=1)
    )
    new_cambial_layer: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=15, month=5, duration=1)
    )
    pre_harvest: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=29, month=10, duration=1)
    )
    harvest: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=30, month=10, duration=1)
    )
    autumn: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=1, month=11, duration=45)
    )
    leaf_fall: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=15, month=11, duration=45)
    )
    leaf_out: Dict[str, int] = dc.field(
        default_factory=lambda: dict(day=25, month=12, duration=1)
    )


@dc.dataclass
class OptionsTree(OptionsBase):
    phyllotactic_angle: float = -144.0
    branching_angle: float = 45.0
    floral_angle: float = -10.0
    tropism: float = 0.1
    preformed_leaves: float = 8
    spur_death_probability: float = 0.3
    inflorescence_death_probability: float = 0.2


@dc.dataclass
class OptionsWood(OptionsBase):
    wood_density: float = 1000  # [kg/m3]
    reaction_wood_rate: float = 0.5
    reaction_wood_inertia_coefficient: float = 0.1
    youngs_modulus: float = 1.1  # [GPa]
    modulus_of_rupture: float = 50e6  # [Pa]


@dc.dataclass
class OptionsInternode(OptionsBase):
    min_length: float = 0.0001  # [m]
    elongation_period: float = 10.0  # [D]
    plastochron: float = 3.0
    max_length: float = 0.03  # [m]


@dc.dataclass
class OptionsApex(OptionsBase):
    terminal_expansion_rate: float = 0.00002  # [m/D]
    minimum_size: float = 0.00075  # [m]
    maximum_size: float = 0.003  # [m]


@dc.dataclass
class OptionsMarkov(OptionsBase):
    maximum_length: int = 70  # < 100
    minimum_length: int = 4
    terminal_fate: Dict[Any, Any] = dc.field(default_factory=lambda: dict())

    def __post_init__(self):
        # create the expected structure/types from toml input
        # i.e. a list of dicts with observations as keys
        terminal_fate = {}
        if self.terminal_fate is not None:
            for i, item in enumerate(self.terminal_fate):
                for observation_str, probabilities in item.items():
                    # start with year_no = 1
                    terminal_fate[
                        (i + 1, Observation(observation_str.upper()))
                    ] = probabilities
        self.terminal_fate = terminal_fate


@dc.dataclass
class OptionsFruit(OptionsBase):
    flower_duration: float = 10.0
    max_relative_growth_rate: float = 0.167
    lost_time: float = 28
    max_age: float = 147
    probability: float = 0.3
    max_absolute_growth_rate: float = 0.0018


@dc.dataclass
class OptionsLeaf(OptionsBase):
    fall_probability: float = 0.1
    maturation: int = 12  # [D]
    mass_per_area: float = 0.220  # [kg/m**2]
    max_area: float = 0.003  # [m**2]
    min_final_area: float = 0.0020  # [m**2]
    petiole_radius: float = 0.0006  # [m]
    preformed_leaves: int = 8


@dc.dataclass
class Options(OptionsBase):
    general: OptionsGeneral = dc.field(default_factory=lambda: OptionsGeneral())
    input: OptionsInput = dc.field(default_factory=lambda: OptionsInput())
    output: OptionsOutput = dc.field(default_factory=lambda: OptionsOutput())
    events: OptionsEvents = dc.field(default_factory=lambda: OptionsEvents())
    tree: OptionsTree = dc.field(default_factory=lambda: OptionsTree())
    wood: OptionsWood = dc.field(default_factory=lambda: OptionsWood())
    internode: OptionsInternode = dc.field(default_factory=lambda: OptionsInternode())
    apex: OptionsApex = dc.field(default_factory=lambda: OptionsApex())
    markov: OptionsMarkov = dc.field(default_factory=lambda: OptionsMarkov())
    fruit: OptionsFruit = dc.field(default_factory=lambda: OptionsFruit())
    leaf: OptionsLeaf = dc.field(default_factory=lambda: OptionsLeaf())

    def __post_init__(self):
        self.general = _make_dataclass(OptionsGeneral, self.general)
        self.input = _make_dataclass(OptionsInput, self.input)
        self.output = _make_dataclass(OptionsOutput, self.output)
        self.events = _make_dataclass(OptionsEvents, self.events)
        self.tree = _make_dataclass(OptionsTree, self.tree)
        self.wood = _make_dataclass(OptionsWood, self.wood)
        self.internode = _make_dataclass(OptionsInternode, self.internode)
        self.apex = _make_dataclass(OptionsApex, self.apex)
        self.markov = _make_dataclass(OptionsMarkov, self.markov)
        self.fruit = _make_dataclass(OptionsFruit, self.fruit)
        self.leaf = _make_dataclass(OptionsLeaf, self.leaf)

    @staticmethod
    def loads(options: str) -> "Options":
        return Options(**toml.loads(options))

    def dumps(self) -> str:
        return toml.dumps(dc.asdict(self))
