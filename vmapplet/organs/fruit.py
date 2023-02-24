from math import log, exp

from ..enums import FruitState


class Fruit:
    """a base class interface for fruits

    A fruit is defined by an **age**, a **mass** and a **state** that may be
    in ['flower', 'no_flower', 'fruit_scar', 'fruit'].

    There is a setter/getter for the state.

    There is a compulsary method named :meth:`compute_mass`. Derived classes must
    implement this method.

    """

    _state: FruitState

    def __init__(self, state: FruitState = FruitState.FLOWER):
        """
        :param str state: a valid fruit state (default is flower)

        The :attr:`age` and :attr:`mass` attributes are set to zero when new
        instance is created.

        .. todo:: make age and  mass real attributes
        """

        self.age = 0
        self._state = state
        self.mass = 0.

    def _set_state(self, state: FruitState):
        if state in list(FruitState):
            self._state = state
        else:
            raise ValueError("state must be in %s , %s provided" % (FruitState, state))

    def _get_state(self) -> FruitState:
        return self._state

    state = property(
        fget=_get_state,
        fset=_set_state,
        doc="getter/setter of :attr:`state` of the component to be specified by the user"
    )

    def compute_mass(self):
        """a method that computes the mass of the fruit and returns its value"""
        raise NotImplementedError('please implements a compute_mass method in your fruit class.')


class AppleFruit(Fruit):
    """A specialised fruit class for apple trees


    This class inherits methods and attributes from
    :class:`~openalea.stocatree.fruit.Fruit` and specialises
    the :meth:`compute_mass` method.

    >>> fruit = AppleFruit(max_age=100., flower_duration=12.)
    >>> fruit.state
    'flower'
    >>> fruit.age
    0
    >>> fruit.mass
    0.0
    >>> fruit._flower_duration
    12.0
    >>> mass = fruit.compute_mass()

    """

    def __init__(self, flower_duration=10., max_relative_growth_rate=0.167, lost_time=28, max_age=147, probability=0.3, max_absolute_growth_rate=.0018):
        """
        Inherits :meth:`get_state`, :meth:`set_state` from :class:`Fruit` class.
        The method :meth:`compute_mass` is redefined.

        The following arguments may be provided and are specific to apple trees. There
        are mainly used to compute the mass of the fruit as a function of its age except for
        the :attr:`probbility` attribute that is the probability of fruitification.

        ==========================  =============== =============  ====================
        name                        notation        Default value  units
        ==========================  =============== =============  ====================
        flower_duration             :math:`T_{fl}`  10.0           day
        max_relative_growth_rate    :math:`R_m`     0.167          per day
        lost_time                   :math:`t_b`     28.0           day
        max_age                                     147.0          day
        probability                                 0.3
        max_absolute_growth_rate    :math:`C_m`     0.0018         kgrams per day
        ==========================  =============== =============  ====================
        """
        Fruit.__init__(self)

        self._flower_duration = flower_duration
        self._max_relative_growth_rate = max_relative_growth_rate
        self._lost_time = lost_time
        self._max_age = max_age
        self._probability = probability
        self._max_absolute_growth_rate = max_absolute_growth_rate
        # units in kg so r be dimensionless. r is used by compute_mass()
        self._r = self._max_absolute_growth_rate / self._max_relative_growth_rate

    def compute_mass(self):
        """Computes the fruit mass according to Lakso et al

        The fruit mass :math:`M_f` is computed with an expolinear model of fruit
        growth (Lakso et al., 1995) that is defined as follows:

        .. math::

            M_f(t) = \\frac{C_m}{R_m} \log (1.+ exp(R_m (t-t_b)))


        where :math:`M_f` is the mass of the fruit :math:`t` days after emergence, :math:`C_m` is the
        maximum absolute growth rate, :math:`R_m` is the maximum relative growth rate, and :math:`t_b`
        where the linear portion of the growth  would intercept the time-axis. This equation gives
        a curve that initialiy  has an exponential character but quickly becomes a linear curve.

        The parameters of the model are chosen to match the observations by Benzig [1], as
        analysed by Costes [2]. The particular observations used are representative of Fuji
        cultivars under a light fruit load, typical of young Fuji trees.

        .. note:: the flower duration is taken into account in the mode and substracted
            to the fruit age before any mass computation. The fruit mass is therefore
            independant of flower duration.

        :returns: fruit mass in gramms
        :references:
            1. Benzing S (1999) Patterns of vegetative and reproductive growth in apple
               (Malusdomestica Borkh.). Master thesis, Faculty de Wiesbaden,
               Geisenheim.
            2. Costes E, Lauri PE, R'egnard JL (2006) Tree architecture and production.
               Horticultural Reviews 32, 1-60.

        .. plot:: pyplots/fruit.py

        """
        #  // default mass unit = kg, time unit = second, ...
        fruit_age = min(self.age - self._flower_duration, self._max_age)

        i = log(1.0 + exp((self._max_relative_growth_rate * (fruit_age - self._lost_time))))
        self.mass = self._r * i
        return self.mass
