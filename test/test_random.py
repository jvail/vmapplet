import pytest

from vmapplet import srandom

N = 100


def test_uniform_random():
    for i in range(1, N):
        a = srandom.random(-1, 1)
        assert a >= -1
        assert a <= 1

    with pytest.raises(Exception):
        srandom.random(-1, 1, 1, 1, 1, 1)

    with pytest.raises(Exception):
        srandom.random("rubbish")


def test_uniform_random_scaled():
    for i in range(1, N):
        a = srandom.random(5.0)
        assert a >= 0
        assert a <= 5


def test_uniform_random_int():
    for i in range(1, N):
        a = srandom.random(5)
        assert a >= 0
        assert a <= 5


def test_boolean_event():
    for i in range(1, 10):
        i * 0.1, " ", srandom.boolean_event(0.5)
