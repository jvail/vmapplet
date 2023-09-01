from typing import Any, Union, Optional, Dict, List

import openalea.lpy as lpy
import openalea.plantgl.all as pgl

# a (optionaly nested) dict of paths to lsystem files
LsystemPaths = Dict[str, Union[str, "LsystemPaths"]]
Lstrings = Dict[str, Union[lpy.Lstring, "Lstrings"]]


class Lsystems:
    """
    A class handling multiple (nested) lpy files & lsystems
    """

    _lsystems: List[Union[lpy.Lsystem, "Lsystems"]]
    _name: str
    _config: Dict[str, Dict[str, Union[int, float, str]]]
    _lstrings: List[lpy.Lstring]
    _keys: List[str]
    _derivation_step: int
    _axiom: lpy.Lstring

    @property
    def derivation_step(self) -> int:
        return self._derivation_step

    @property
    def axiom(self) -> lpy.Lstring:
        return self._axiom

    @property
    def lstrings(self) -> Lstrings:
        lstrings = {}

        for (i, key), lstr in zip(enumerate(self._keys), self._lstrings):
            if type(self._lsystems[i]) is Lsystems:
                lstrings[key] = self._lsystems[i].lstrings
            else:
                lstrings[key] = lstr

        return lstrings

    def __init__(
        self,
        paths: LsystemPaths,
        context: Dict[str, Any] = {},
        config: Dict[str, Dict[str, Union[int, float, str]]] = {},
        name: str = "",
    ):
        """
        The config parameter is somewhat experimental. Currently just 'steps'
        is used to derive 'mechanics' 'steps' times
        """

        self._lsystems = []
        self._name = name
        self._config = config
        for name, path_or_paths in paths.items():
            if type(path_or_paths) is dict:
                self._lsystems.append(Lsystems(path_or_paths, context, config, name))
            else:
                self._lsystems.append(lpy.Lsystem(path_or_paths, context))

        self._axiom = self._lsystems[0].axiom
        self._lstrings = [self._axiom] * len(self._lsystems)
        self._keys = list(paths.keys())
        self._derivation_step = 0

    def derive(
        self,
        lstring: Optional[lpy.Lstring] = None,
        step: Optional[int] = None,
        steps: Optional[int] = None,
    ) -> lpy.Lstring:
        step = step or self._derivation_step
        steps = steps or 1
        lstring = lstring or self._lstrings[-1]

        if self._name in self._config and "steps" in self._config[self._name]:
            steps = int(self._config[self._name]["steps"])
            step = self._derivation_step

        for i, lsystem in enumerate(self._lsystems):
            lstring = lsystem.derive(lstring, step, steps)
            self._lstrings[i] = lstring

        self._derivation_step += steps

        return lstring

    def sceneInterpretation(self, lstring: Optional[lpy.Lstring] = None) -> pgl.Scene:
        """Create PlantGl scene from last lsystem/lstring in list"""
        return self._lsystems[-1].sceneInterpretation(self._lstrings[-1])
