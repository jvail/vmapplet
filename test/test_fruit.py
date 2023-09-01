import pytest

from vmapplet.organs.fruit import Fruit, AppleFruit
from vmapplet.enums import FruitState


def test_fruit_state():
    # test set_state/get_state
    f = Fruit()
    f.state = FruitState.FLOWER
    assert f._state == FruitState.FLOWER
    with pytest.raises(Exception):
        f.state = "dummy"

    assert f.state == FruitState.FLOWER


def test_fruit_compute_mass():
    f = Fruit()
    with pytest.raises(Exception):
        f.compute_mass()


def test_apple_fruit_state():
    # test set_state/get_state
    f = AppleFruit()
    f.state = FruitState.FLOWER
    assert f._state == FruitState.FLOWER
    with pytest.raises(Exception):
        f.state = "dummy"


def test_apple_fruit_attributes():
    f = AppleFruit()
    assert f._flower_duration == 10
    assert f._probability == 0.3
    assert f._lost_time == 28
    assert f._max_relative_growth_rate == 0.167


def test_apple_fruit_compute_mass():
    f = AppleFruit()
    f.age = 50
    f.compute_mass()
