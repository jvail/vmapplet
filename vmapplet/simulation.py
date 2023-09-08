from typing import Dict, Tuple, Optional, Union
import pathlib
import dataclasses as dc
from datetime import datetime, timedelta
import random
import io
import os
import pickle

from openalea.mtg.io import (
    axialtree2mtg,
    # TODO: Try lpy2mtg
)
import toml
import numpy as np

from .organs.tree import Tree
from .organs import get_scale
from .tools.lsystems import LsystemPaths, Lsystems
from .tools.simulation import SimulationInterface, RotationConvergence
from .tools.read_function import ReadFunction
from .tools.file_tools import get_shared_data_path
from .options import Options
from .markov import Markov, MarkovModel


def _to_full_path(root: pathlib.Path, paths: LsystemPaths) -> LsystemPaths:
    return {
        name: str(pathlib.Path(root).joinpath(path))
        if type(path) is str
        else _to_full_path(root, path)
        for name, path in paths.items()
    }


class Simulation(SimulationInterface):
    """Instantiate a VMAppleT Simulation

    :param options: a string (toml) or an Options instance
    :param output_path: a string/path were output files will be created
    """

    options: Options
    rotation_convergence: RotationConvergence

    _lsystems: Lsystems
    _markov: Markov
    _markov_models: Dict[Tuple[str, int], MarkovModel]
    _output_path: pathlib.Path
    _rng: np.random.Generator

    # calculated from events: between leaf_out and bud_break
    _growth_pause: bool = False

    def __init__(self, options: Union[str, Options], output_path: Optional[str] = None):
        if isinstance(options, Options):
            self.options = options
        else:
            self.options = Options(**toml.loads(options))

        self._output_path = pathlib.Path(output_path or os.getcwd() + "/output")

        start_date = self.options.general.date_start
        end_date = self.options.general.date_end

        super().__init__(starting_date=start_date, ending_date=end_date)
        random.seed(self.options.general.seed)
        self._rng = np.random.default_rng(self.options.general.seed)

        for name, event in dc.asdict(self.options.events).items():
            self.events.add_event(
                name,
                datetime(
                    self.options.general.date_start.year, event["month"], event["day"]
                ),
                duration=timedelta(event["duration"]),
            )

        self._markov = Markov(
            generator=self._rng,
            minimum_length=self.options.markov.minimum_length,
            maximum_length=self.options.markov.maximum_length,
        )

        self._markov_models = {}
        for path in os.listdir(get_shared_data_path("markov")):
            path = pathlib.Path(get_shared_data_path("markov")) / path
            if path.is_file() and path.suffix == ".toml":
                with io.open(path) as file:
                    model = MarkovModel(**toml.loads(file.read()))
                    self._markov_models[(model.length, model.year)] = model

        tree = Tree(**self.options.tree)

        lpy_path = self.options.input.lpy_path
        lpy_files = self.options.input.lpy_files
        # namspace available in L-Py files
        lpy_options = dict(
            options=self.options, simulation=self, markov=self._markov, tree_data=tree
        )

        self._lsystems = Lsystems(
            _to_full_path(pathlib.Path(lpy_path), lpy_files),
            lpy_options,
            dict(mechanics=dict(steps=self.options.general.convergence_steps)),
        )

        self._func_leaf_area_init(get_shared_data_path("lpy/functions.fset"))
        self.rotation_convergence = RotationConvergence(
            steps=self.options.general.convergence_steps
        )

    def _func_leaf_area_init(
        self, filename="lpy/functions.fset", func_name="leaf_area"
    ):
        """read the functions.fset once for all the metamers"""
        self.func_leaf_area = ReadFunction(filename, func_name)

    def _write_output(self, lstring):
        file_name = f"{datetime.date(self.calendar.date).isoformat()}.bmtg"

        if not os.path.exists(self._output_path):
            os.mkdir(self._output_path)

        with io.open(self._output_path / file_name, "xb") as file:
            mtg = axialtree2mtg(
                lstring,
                scale={
                    organ: get_scale(organ)
                    for organ in self.options.output.attributes.keys()
                },
                scene=None,
                parameters=self.options.output.attributes,
            )
            pickle.dump(mtg, file)

    def _set_markov_model(self):
        if self.year_no == 0:
            self._markov.set_models(
                medium=self._markov_models[("MEDIUM", 3)],
                long=self._markov_models[("LONG", 1)],
            )
            # self._markov.hsm_medium = self._markov_model['fuji_medium_year_3']
            # self._markov.hsm_long = self._markov_model['fuji_long_year_1']
        if self.year_no == 1:
            self._markov.set_models(
                medium=self._markov_models[("MEDIUM", 3)],
                long=self._markov_models[("LONG", 1)],
            )
            # self._markov.hsm_medium = self._markov_model['fuji_medium_year_3']
            # self._markov.hsm_long = self._markov_model['fuji_long_year_2']
        elif self.year_no == 2:
            self._markov.set_models(
                medium=self._markov_models[("MEDIUM", 3)],
                long=self._markov_models[("LONG", 3)],
            )
            # self._markov.hsm_medium = self._markov_model['fuji_medium_year_3']
            # self._markov.hsm_long = self._markov_model['fuji_long_year_3']
        elif self.year_no == 3:
            self._markov.set_models(
                medium=self._markov_models[("MEDIUM", 4)],
                long=self._markov_models[("LONG", 4)],
            )
            # self._markov.hsm_medium = self._markov_model['fuji_medium_year_4']
            # self._markov.hsm_long = self._markov_model['fuji_long_year_4']
        else:
            self._markov.set_models(
                medium=self._markov_models[("MEDIUM", 5)],
                long=self._markov_models[("LONG", 5)],
            )
            # self._markov.hsm_medium = self._markov_model['fuji_medium_year_5']
            # self._markov.hsm_long = self._markov_model['fuji_long_year_5']

    def get_active_events(self) -> Tuple[str, ...]:
        active_events = tuple([event.name for event in self.events if event.active])
        if "leaf_out" in active_events:
            self._growth_pause = True
        elif "bud_break" in active_events:
            self._growth_pause = False
        if self._growth_pause is True:
            active_events = ("growth_pause",) + active_events
        return active_events

    def advance(self):
        """
        Advance simulation by one day and derive all lsystems
        """
        super().advance()
        self._set_markov_model()
        lstring = self._lsystems.derive()
        for day_month in self.options.output.dates:
            if (
                day_month["day"] == self.calendar.day
                and day_month["month"] == self.calendar.month
            ):
                self._write_output(lstring)

    def get_scene(self):
        return self._lsystems.sceneInterpretation()
