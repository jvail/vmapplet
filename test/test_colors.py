import pytest

from vmapplet.colors import (
    Colors,
    Year,
    Zone,
    ReactionWood,
    ObservationColors,
    ColorInterface,
)
from vmapplet.enums import Observation, Zone as ZoneEnum


def test_colors():
    colors = Colors()
    assert colors.red == 2
    colors.observation.get_color(Observation.DORMANT) == 2


def test_year():
    y = Year()
    y.set_colors()
    y.get_color(1994, starting_year=1994)


def test_zone():
    y = Zone()
    y.set_colors()
    y.get_color(ZoneEnum.SMALL)

    with pytest.raises(Exception):
        y.get_color("dummy")


def test_reaction_wood():
    y = ReactionWood()
    y.set_colors()
    y.get_color(1.0)


def test_observation():
    y = ObservationColors()
    y.set_colors()
    y.get_color(Observation.LARGE)
    with pytest.raises(Exception):
        y.get_color("dummy")


def test_colorInterface():
    c = ColorInterface()
    with pytest.raises(Exception):
        c.set_colors()
    with pytest.raises(Exception):
        c.get_color()
