import pytest

from vmapplet.sequences import (
    Markov,
    terminal_fate,
    generate_trunk,
    _generate_random_draw_sequence,
    generate_floral_sequence,
    generate_short_sequence,
    _non_parametric_distribution,
)
from vmapplet.enums import Observation


def test_terminal_fate():
    for year in range(0, 7):
        for code in [
            Observation.LARGE,
            Observation.MEDIUM,
            Observation.SMALL,
            Observation.FLORAL,
        ]:
            index = terminal_fate(year, code)
            assert index in list(Observation)


def test_generate_trunk():
    for i in range(1, 10):
        seq = generate_trunk()
        assert len(seq) == 4


def test_generate_random_draw_sequence():
    seq = _generate_random_draw_sequence()
    assert len(seq) in [46, 20, 49, 57, 39, 51, 48, 53, 62]


def test_floral():
    seq = generate_floral_sequence()
    assert len(seq) == 4


def test_short():
    seq = generate_short_sequence()
    assert len(seq) == 4


def test_non_parametric_distribution():
    pdf = [0.25, 0.25, 0.25, 0.25]
    for i in range(100):
        index = _non_parametric_distribution(pdf)
        assert index >= 1
        assert index <= 4

    pdf = [1, 1, 1, 1]
    with pytest.raises(Exception):
        index = _non_parametric_distribution(pdf)


def test_markov():
    markov = Markov()
    assert markov.maximum_length == 70
