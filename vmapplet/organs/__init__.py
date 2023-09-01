from .apex import ApexData
from .fruit import AppleFruit
from .growth_unit import GrowthUnitData
from .internode import Internode
from .leaf import AppleLeaf
from .metamer import MetamerData
from .tree import Tree
from .wood import Wood


_SCALE = {
    "TREE": 0,
    "GROWTH_UNIT": 1,
    "APEX": 2,
    "METAMER": 2,
}


def get_scale(organ: str):
    """Get scale of an organ/entity. Mainly used for MTG export"""
    return _SCALE[organ.upper()]


__all__ = [
    "ApexData",
    "AppleFruit",
    "GrowthUnitData",
    "Internode",
    "AppleLeaf",
    "MetamerData",
    "Tree",
    "Wood",
]
