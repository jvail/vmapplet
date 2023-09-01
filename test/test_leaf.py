import pytest

from vmapplet.organs import AppleLeaf
from vmapplet.enums import LeafState


def test_apple_leaf_state():
    # test set_state/get_state
    f = AppleLeaf(state=LeafState.GROWING)
    assert f.state == "GROWING"
    with pytest.raises(Exception):
        f.state = "dummy"

    assert f.state == LeafState.GROWING


class test_apple_leaf:
    leaf = AppleLeaf()
    assert leaf.max_area == 30 * 0.01 * 0.01
    leaf.age = 50
    leaf.compute_mass()


def test_apple_leaf_compute_area_from_func():
    import pathlib
    from vmapplet.tools.read_function import ReadFunction

    f = AppleLeaf()
    f.age = 50
    func_leaf_area = ReadFunction(
        pathlib.Path(__file__).parent.resolve() / "functions.fset", "leaf_area"
    )
    # first test the preformeed leaves
    f.compute_area_from_func(4, func_leaf_area)
    # and full leaves
    f.compute_area_from_func(14, func_leaf_area)
    # then maturity
    f.age = f.maturation + 1
    f.maturity = True
    f.compute_area_from_func(14, func_leaf_area)


def test_apple_leaf_compute_area():
    f = AppleLeaf()
    # before maturation
    f.age = 8
    f.compute_area(6)
    # after maturation
    f.age = 50
    f.compute_area(6)
    # number below and above 8
    f.compute_area(16)
