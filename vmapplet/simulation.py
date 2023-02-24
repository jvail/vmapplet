from typing import (
    Dict,
    Tuple,
    Optional
)
import pathlib
import dataclasses as dc
from datetime import (
    datetime,
    timedelta
)
import random

import toml
from pgljupyter import SceneWidget

from .organs.tree import Tree
from .tools.lsystems import (
    LsystemPaths,
    Lsystems
)
from .tools.simulation import (
    SimulationInterface,
    RotationConvergence
)
from .tools.read_function import ReadFunction
from .tools.structure_analysis import (
    HiddenSemiMarkov,
    StatError
)
from .options import Options
from .sequences import Markov


def get_shared_data(path: str):
    return str(pathlib.Path(__file__).joinpath(f'../data/{path}').resolve())


def _to_full_path(root: pathlib.Path, paths: LsystemPaths) -> LsystemPaths:
    return {
        name: str(pathlib.Path(root).joinpath(path)) if type(path) is str else _to_full_path(root, path)
        for name, path in paths.items()
    }


class Simulation(SimulationInterface):

    options: Options
    rotation_convergence: RotationConvergence

    _lsystems: Lsystems
    _markov: Markov
    _markov_model: Dict[str, HiddenSemiMarkov]

    # calculated from events: between leaf_out and bud_break
    _growth_pause: bool = False

    def __init__(self, options: str):

        self.options = Options(**toml.loads(options))

        year_start = self.options.general.date_start.year
        year_end = self.options.general.date_start.year

        super().__init__(dt=1, starting_date=year_start, ending_date=year_end)
        random.seed(self.options.general.seed)

        for name, event in dc.asdict(self.options.events).items():
            self.events.add_event(
                name,
                datetime(year_start, event['month'], event['day']),
                duration=timedelta(event['duration'])
            )

        self._markov = Markov(**self.options.markov)

        self._markov_model = dict(
            fuji_medium_year_3=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_medium_year_3.txt')
            ),
            fuji_medium_year_4=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_medium_year_4.txt')
            ),
            fuji_medium_year_5=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_medium_year_5.txt')
            ),
            fuji_long_year_1=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_long_year_1.txt')
            ),
            fuji_long_year_2=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_long_year_2.txt')
            ),
            fuji_long_year_3=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_long_year_3.txt')
            ),
            fuji_long_year_4=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_long_year_4.txt')
            ),
            fuji_long_year_5=HiddenSemiMarkov.ascii_read(
                StatError(), get_shared_data('markov/fuji_long_year_5.txt')
            )
        )

        tree = Tree(**self.options.tree)

        lpy_path = self.options.input.lpy_path
        lpy_files = self.options.input.lpy_files
        # namspace available in L-Py files
        lpy_options = dict(
            options=self.options,
            simulation=self,
            markov=self._markov,
            tree=tree
        )
        self._lsystems = Lsystems(
            _to_full_path(pathlib.Path(lpy_path), lpy_files),
            lpy_options,
            dict(mechanics=dict(steps=self.options.general.convergence_steps))
        )

        self._func_leaf_area_init(get_shared_data('lpy/functions.fset'))
        self.rotation_convergence = RotationConvergence(steps=self.options.general.convergence_steps)

    def _func_leaf_area_init(self, filename='lpy/functions.fset', func_name='leaf_area'):
        """read the functions.fset once for all the metamers"""
        self.func_leaf_area = ReadFunction(filename, func_name)

    def _set_markov_model(self):

        if self.year_no == 0:
            self._markov.hsm_medium = self._markov_model['fuji_medium_year_3']
            self._markov.hsm_long = self._markov_model['fuji_long_year_1']
        if self.year_no == 1:
            self._markov.hsm_medium = self._markov_model['fuji_medium_year_3']
            self._markov.hsm_long = self._markov_model['fuji_long_year_2']
        elif self.year_no == 2:
            self._markov.hsm_medium = self._markov_model['fuji_medium_year_3']
            self._markov.hsm_long = self._markov_model['fuji_long_year_3']
        elif self.year_no == 3:
            self._markov.hsm_medium = self._markov_model['fuji_medium_year_4']
            self._markov.hsm_long = self._markov_model['fuji_long_year_4']
        else:
            self._markov.hsm_medium = self._markov_model['fuji_medium_year_5']
            self._markov.hsm_long = self._markov_model['fuji_long_year_5']

    def active_events(self) -> Tuple[str, ...]:
        active_events = tuple([event.name for event in self.events if event.active])
        if 'leaf_out' in active_events:
            self._growth_pause = True
        elif 'bud_break' in active_events:
            self._growth_pause = False
        if self._growth_pause is True:
            active_events = ('growth_pause',) + active_events
        return active_events

    def run(self, scene_widget: Optional[SceneWidget] = None) -> None:

        date_start = self.options.general.date_start
        date_end = self.options.general.date_end

        for step in range((date_end - date_start).days):

            self.advance()
            self._set_markov_model()
            self._lsystems.derive()

            if scene_widget is not None:
                events = self.active_events()
                if 'growth_pause' not in events and 'leaf_out' not in events:
                    # avoid displaying scenes when nothing changes visualy during a growth pause
                    scene = self._lsystems.sceneInterpretation()
                    if scene is not None:
                        scene_widget.set_scenes(scene, scales=0.1)
