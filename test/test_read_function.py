import pytest
import pathlib

from vmapplet.tools.read_function import ReadFunction, _FSet


def test_read_function():
    func_leaf_area = ReadFunction(
        pathlib.Path(__file__).parent.resolve() / "functions.fset", "leaf_area"
    )
    func_leaf_area.gety(0.5)

    with pytest.raises(Exception):
        func_leaf_area = ReadFunction("dummy.fset", "leaf_area")


def test_fset():
    x = [0, 1, 2, 3]
    y = [0, 0.25, 0.5, 1]
    fset = _FSet(flip="on", x=x, y=y)
    print(fset)
    fset = _FSet(flip="off", x=x, y=y)
    print(fset)

    with pytest.raises(Exception):
        fset = _FSet(flip="dummy", x=x, y=y)
