from typing import Optional

from pgljupyter import SceneWidget

from ._cppyy import *  # noqa
from .simulation import Simulation
from .options import Options


def run(simulation: Simulation, scene_widget: Optional[SceneWidget] = None):
    """
    """

    date_start = simulation.options.general.date_start
    date_end = simulation.options.general.date_end

    for _ in range((date_end - date_start).days):

        simulation.advance()

        if scene_widget is not None:
            events = simulation.get_active_events()
            if 'growth_pause' not in events and 'leaf_out' not in events:
                # avoid displaying scenes when nothing changes visualy during a growth pause
                scene = simulation.get_scene()
                if scene is not None:
                    scene_widget.set_scenes(scene, scales=0.1)


__all__ = [
    'Simulation',
    'Options',
    'run'
]
