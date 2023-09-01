import pytest

from vmapplet.organs.apex import ApexData
from vmapplet.enums import Observation
from vmapplet.sequences import generate_sequence, Markov

markov = Markov()


class TestApexData:
    apex = ApexData()

    def test_observation(self):
        assert Observation.TRUNK == self.apex.get_observation()
        with pytest.raises(Exception):
            self.apex.set_observation("dummy")

    def test_sequence(self):
        self.apex.sequence = generate_sequence(
            self.apex.get_observation(), markov, 1995, False
        )
        for index, *_ in enumerate(self.apex.sequence):
            self.apex.sequence_position = index
            observation = self.apex.get_observation_from_sequence()
            assert observation in list(Observation)

    def test_radius_target(self):
        self.apex.sequence_position = 15
        self.apex.max_terminal_radius_target()

    def test_terminal_expansion(self):
        self.apex.terminal_expansion(10)
