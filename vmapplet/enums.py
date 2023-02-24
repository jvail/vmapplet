from enum import Enum


class Observation(str, Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'
    SYLLEPTIC_SMALL = 'SYLLEPTIC_SMALL'
    SYLLEPTIC_MEDIUM = 'SYLLEPTIC_MEDIUM'
    SYLLEPTIC_LARGE = 'SYLLEPTIC_LARGE'
    DORMANT = 'DORMANT'
    FLORAL = 'FLORAL'
    TRUNK = 'TRUNK'
    NEW_SHOOT = 'NEW_SHOOT'


class FruitState(str, Enum):
    FLOWER = 'FLOWER'
    NO_FLOWER = 'NO_FLOWER'
    FRUIT_SCAR = 'FRUIT_SCAR'
    FRUIT = 'FRUIT'


class LeafState(str, Enum):
    SCAR = 'SCAR'
    GROWING = 'GROWING'
