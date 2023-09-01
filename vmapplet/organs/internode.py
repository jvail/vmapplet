from typing import Optional

from ..enums import Zone


class Internode:
    """Internode class to be used within a metamer"""

    def __init__(
        self,
        min_length=0.0001,
        elongation_period=10.0,
        plastochron=3.0,
        max_length=0.03,
    ):
        self._min_length = min_length  # m/day
        self._plastochron = plastochron  # days
        self._elongation_period = elongation_period  # days
        self._max_length = max_length

        self._final_none = self._max_length / 1.5
        self._final_dormant_start = 0.25 * self._max_length / 1.5
        self._final_small = 0.5 * self._max_length / 1.5
        self._final_diffuse = self._max_length / 1.5
        self._final_medium = 0.75 * self._max_length / 1.5
        self._final_floral = 0.5 * self._max_length / 1.5
        self._final_dormant_end = 0.25 * self._max_length / 1.5
        self._final_else = 0.25 * self._max_length / 1.5

    def growth_rate(self, zone: Optional[Zone] = None):
        """compute te growth rate of the internode as a function of its zone

        :Hypothesis:

        The elongation rate of an internode depends on the zone in which it appears

        :param float uzone: zone in which is situated the internode

        :returns: a velocity in m/day
        """

        if zone is None:
            res = self._final_none / self._elongation_period
        elif zone == Zone.DORMANT_START:
            res = self._final_dormant_start / self._elongation_period
        elif zone == Zone.SMALL:
            res = self._final_small / self._elongation_period
        elif zone == Zone.DIFFUSE:
            res = self._final_diffuse / self._elongation_period
        elif zone == Zone.MEDIUM:
            res = self._final_medium / self._elongation_period
        elif zone == Zone.FLORAL:
            res = self._final_floral / self._elongation_period
        elif zone == Zone.DORMANT_END:
            res = self._final_dormant_end / self._elongation_period
        else:
            res = self._final_else / self._elongation_period

        return res
