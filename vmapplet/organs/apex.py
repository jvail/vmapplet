from typing import List, Union, Tuple

from ..frame import Frame
from ..enums import Observation


class ApexData:
    """An apex class to be used in stocatree

    :Usage:

    First, you need to create an instance of the apex

    >>> a = ApexData()

    There are several default parameters described in the constructor
    documentation. You can now access to the attributes such as the
    **observation** using the getter :func:`get_observation`. There is
    also a setter for the observation :func:`set_observation`

    >>> a.get_observation()
    'trunk'

    :possible observations:

    ================ ======================================== ================================
    observation Code        Type of shoot from a bud                 Number of metamers
    ================ ======================================== ================================
    dormant          dormant bud (no shoot grow)
    large            long shoot                               16-70
    medium           medium shoot                             5-15
    small            short shoot                              4
    floral           inflorescence                            4 followed by a sylleptic shoot
    trunk            on the main trunk
    new_shoot        not yet determined
    ================ ======================================== ================================

    The other important attribute is the **radius**.

    >>> a.radius
    0.0

    There is a **maximum target radius** that is defined by the
    :func:`max_terminal_radius_target`.

    Each apex is associated to an HLU :class:`~openalea.stocatree.physics.Frame` to
    keep track of its orientation in the scene.


    Finally, an apex is part of a sequence.

    .. seealso:: :func:`generate_sequence`, :func:`terminal_fate`

    """

    sequence_position: int
    _observation: Union[None, Observation]
    parent_observation: Observation
    hlu: Frame
    sequence: Union[None, List[Tuple[int, int]]]
    radius: float
    target_radius: float
    expansion_period: int
    expansion_days_counter: int
    sequence_minimum_length: float
    sequence_maximum_length: float
    sequence_length_range: float

    # expansion rate of the radius
    terminal_expansion_rate: float

    # define the radius size
    maximum_size: float
    minimum_size: float
    radius_range: float

    # This is used to record the parent unit id
    # Added by Han
    parent_unit_id: int

    # This is used to record the parent branch id (first-order branch)
    # Added by Han on 02-05-2011
    parent_fbr_id: int

    # Since only one tree is investigated at this stage, there is no need to
    # update this parameter:
    parent_tree_id: int

    # Added by Han on 29-05-2012
    # The value will be set to be the same with the current year once a
    # growth unit (sequence) is fully generated
    # This is to avoid there are two growth units at the same year
    year: int

    # Added by Han on 06-07-2012
    # This is to avoid "1,2,3,4" growth units to be syllpetic at the first year
    sylleptic: bool

    # Flag to show that this apex was generated as a reaction to pruning
    from_pruning: bool

    # Information related to pruning reaction
    rank: int
    react_pos: int
    closest_apex: int
    farthest_apex: int

    # the cumulated sum of metamers sons
    sons_nb: int

    def __init__(self, hlu=Frame(), observation=Observation.TRUNK,
                 terminal_expansion_rate=0.00002, minimum_size=0.00075,
                 maximum_size=0.006, minimum_length=4, maximum_length=70,
                 expansion_period=300, target_radius=0.006, sylleptic=False, **kwargs):
        """
        The arguments "expansion_period" and "target_radius" were added by Han
        on 14-04-2011.
        """
        """**Constructor**

        The following attributes are set

        :param hlu: an instance of :class:`~openalea.stocatree.physics.Frame`
        :param observation: a string defining the apex's state (default is 'trunk')
        :param terminal_expansion_rate: default is 0.00002 meters per day
        :param minimum_size: default is 0.00075 meters
        :param maximum_size: default is 0.006 meters
        :param minimum_length: minimum length of the sequence (default 4)
        :param maximum_size: maximum length of the sequence (default is 70)

        :attributes:

        =========================== =============== ============
        type                        Default value   units
        =========================== =============== ============
        :attr:`radius`              0.              meters
        :attr:`target_radius`       0.              meters
        parent_observation          'NEW_SHOOT'
        trunk                       False
        sequence_position           0
        sequence                    None
        =========================== =============== ============


        """
        self.sequence_position = 0
        self._observation = None
        self.set_observation(observation)
        self.parent_observation = Observation.NEW_SHOOT
        self.trunk = observation == Observation.TRUNK
        self.hlu = hlu
        self.sequence = None

        self.radius = 0.
        self.target_radius = 0.
        self.expansion_period = expansion_period
        self.expansion_days_counter = 0
        self.sequence_minimum_length = minimum_length
        self.sequence_maximum_length = maximum_length
        assert self.sequence_maximum_length > self.sequence_minimum_length
        self.sequence_length_range = float(
            self.sequence_maximum_length -
            self.sequence_minimum_length
        )
        self.terminal_expansion_rate = terminal_expansion_rate
        self.maximum_size = maximum_size
        self.minimum_size = minimum_size
        self.radius_range = maximum_size - minimum_size
        self.parent_unit_id = 0
        self.parent_fbr_id = 0
        self.parent_tree_id = 0
        self.year = 1993
        self.sylleptic = sylleptic
        self.from_pruning = False
        self.rank = 0
        self.react_pos = 0
        self.closest_apex = 0
        self.farthest_apex = 0
        self.sons_nb = 0

    def set_observation(self, observation: Observation):
        """
        Set the apex observation. Observation values are defined in the enum 'Observation'
        """

        if observation in list(Observation):
            self._observation = observation
        else:
            raise ValueError("observation must be in %s , %s provided"
                             % (Observation, observation))

    def get_observation(self) -> Union[Observation, None]:
        """returns the current apex observation"""
        return self._observation

    def get_observation_from_sequence(self) -> Observation:
        """return observation corresponding to the current position"""

        index = self.sequence[self.sequence_position][1] if self.sequence is not None else -1

        if index == 0:
            return Observation.DORMANT
        elif index == 1:
            return Observation.LARGE
        elif index == 2:
            return Observation.MEDIUM
        elif index == 3:
            return Observation.SMALL
        elif index == 4:
            return Observation.FLORAL
        # The following indexes were added by Han on 30-04-2012
        elif index == 5:
            return Observation.SYLLEPTIC_SMALL
        elif index == 6:
            return Observation.SYLLEPTIC_MEDIUM
        elif index == 7:
            return Observation.SYLLEPTIC_LARGE
        else:
            # should never reach this line, however old sequences may contain 9s
            return Observation.DORMANT

    def max_terminal_radius_target(self):
        """Set the max terminal radius :attr:`target_radius`

        The radius range is defined by the minimum and maximum apex radius.

        .. math::

            r_{\\textrm{range}} = \\left(r_{\\textrm{max}} - r_{\\textrm{min}} \\right)

        The position is also defined within a valid range

        .. math::

            \\textrm{Position}_{\\textrm{range}} = \\left(\\textrm{Posistion}_{\\textrm{max}} - \\textrm{Position}_{\\textrm{min}} \\right)

        Therefore the maximum terminal apex range is defined by

        .. math::

            r_{\\textrm{target}} = r_{\\textrm{min}} + r_{\\textrm{range}} \\times (\\frac{ \\textrm{Position} - \\textrm{Position}_{\\textrm{min}})}{\\textrm{Position}_{\\textrm{range}}}

        :Hypothesis: a terminal apex expands to a maximum size based on the number
         of leaves in a shoot (i.e., position)

        """
        if self.sequence_position < self.sequence_minimum_length:
            print(self.sequence_position, self.sequence_minimum_length)
            print(self.sequence)
        assert self.sequence_position >= self.sequence_minimum_length
        self.target_radius = self.minimum_size + self.radius_range * (
            self.sequence_position - self.sequence_minimum_length
        ) / self.sequence_length_range

    def terminal_expansion(self, dt):
        self.radius = self.radius + self.terminal_expansion_rate * dt
        self.expansion_days_counter += dt

    # Added by Han on 11-07-2012, to be used as a condition to control the first-year sylleptic growth from trunk
    def trunk_sylleptic(self):
        index = self.sequence[self.sequence_position][1] if self.sequence is not None else -1
        if index == 0:
            return False
        elif index == 1:
            return False
        elif index == 2:
            return False
        elif index == 3:
            return False
        elif index == 4:
            return False
        # The following indexes were added by Han on 30-04-2012
        elif index == 5:
            return True
        elif index == 6:
            return True
        elif index == 7:
            return True

        raise ValueError("should never reach this line")
