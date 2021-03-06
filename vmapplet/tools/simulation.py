import datetime

from .read_function import ReadFunction


class Calendar(object):
    """A calendar class

    The Calendar class is a simple calendar that keeps track of the current date. It is
    fully based upon the datetime module.


    Calendar has five attributes with getter and setters: year, month, day, date and dt
    (see constructor for details).

    There is one main method, called :meth:`advance` that increments the :attr:`date` by :attr:`dt`
    and returns True is a new year has been passed through.


    .. doctest::

        >>> cal = Calendar(1994)
        >>> cal.year = 2000
        >>> cal.month = 1
        >>> cal.day = 1
        >>> cal.dt = 30     # in days
        >>> cal.advance()
        False

        >>> cal = Calendar(1994, month=12, day=31)
        >>> cal.advance()
        True
        >>> cal.year == 1995
        True

    """
    def __init__(self,  year=-1, month=1, day=1, delta_in_days=1):
        """**Constructor**

        :param year: valid year
        :param month: valid month in [1,12]
        :param day: valid day in [1, 31]
        :param delta_in_days: the time step in days


        :attributes:

            * :attr:`year`, the current year, an alias to date.year
            * :attr:`month`, the current year, an alias to date.month
            * :attr:`day`, the current year, an alias to date.day
            * :attr:`dt` the increment or time step (instance of :class:`datetime.timedelta`
            * :attr:`date` a :class:`datetime.datetime` object that contains the year, month and day

        """

        assert year != -1 , "you must provide a valid year"
        self._date = datetime.datetime(year=year, month=month, day=day)
        self._dt = datetime.timedelta(days=delta_in_days)
        self._year = year

    def _get_date(self):
        return self._date
    def _set_date(self, date):
        self._date = date
    date = property(fget=_get_date, fset=_set_date,
                    doc="Set date given a valid datetime.datetime() instance")

    def _get_month(self):
        return self._date.month
    def _set_month(self, month):
        self._date = datetime.datetime(self.year, month, self.day)
    month = property(fget=_get_month, fset=_set_month,
                    doc="Set month given a valid month (between 1 and 12)")

    def _get_day(self):
        return self._date.day
    def _set_day(self, day):
        self._date = datetime.datetime(self.year, self.month, day)
    day = property(fget=_get_day, fset=_set_day,
                    doc="Set day given a valid day (between 1 and 31)")

    def _get_year(self):
        return self._date.year
    def _set_year(self, year):
        self._date = datetime.datetime(year, self._date.month, self._date.day,
                                       self._date.hour, self.date.minute,
                                       self._date.second,
                                       self._date.microsecond)
        self._year = year
    year = property(fget=_get_year, fset=_set_year , doc="set current year.")

    def _get_dt(self):
        return self._dt
    def _set_dt(self, dt):
        self._dt = datetime.timedelta(days=dt)
    dt = property(fget=_get_dt, fset=_set_dt,
             doc="Set the delta time increment in days (may be non integer)")


    def __str__(self):
        res = 'current date and time= %s\n' % str(self._date)
        res += 'current increment= %s\n' % str(self._dt)
        return res


    def advance(self):
        """advance the **current_time** by the **increment**

        :return: True if cycle over a new year

        """
        self._date += self._dt
        if self.year > self._year:
            self._year = self.year
            return True
        else:
            return False



class Event(object):
    """create an event

    An event is defined by a name, a starting date, a duration.

    In addition, it may be periodic (over years) or not.

    An event is active if the current date (from a Calendar) is
    between the starting date and the starting_date plus the event duration.

    .. doctest::

        >>> event = Event('test', datetime.datetime(2000,4,15), datetime.timedelta(10))
        >>> event = Event('test', datetime.datetime(2000,4,15), datetime.timedelta(10), periodic=False)
        >>> assert event.duration.days == 10


    """

    def __init__(self, name, starting_date, duration=datetime.timedelta(1),
                 periodic = True):
        """

        :param name: set a label to an event
        :param date: a starting date (:class:`datetime.datetime` instance)
        :param duration: a duration in days (:class:`datetime.timedelta`),
            default is 1 day
        :param periodic: a boolean to specify if the event is a singl event or
          is periodic over years

        :attributes:
            * :attr:`name` same as input name
            * :attr:`starting_date` same as input starting_date
            * :attr:`ending_date` is the starting date plus duration
            * :attr:`active` is set by the :meth:`isactive` to True of False
            * :attr:`duration` is the event duration
            * :attr:`periodic` is a flag to set if the event occurs every year

        """
        # some assertions
        assert type(starting_date) == datetime.datetime, \
            'date must be of type datetime.datetime()'
        assert type(name) == str, 'name must be of type str'
        assert type(duration) == datetime.timedelta, \
            'duration must be of type datetime.timedelta'
        assert periodic in [True, False], 'duration must be of type boolean'
        assert duration.days < 365, \
            'Duration of an event must be less than a year'


        self._name = name
        self._starting_date = starting_date
        self._ending_date = starting_date + duration
        self._active = False
        self._duration = duration
        self._periodic = periodic

    def __str__(self):
        res = self.name + " "
        res += str(self.starting_date) + "\n"
        res += " duration=" + str(self.duration) + "\n"
        res += " active=" + str(self.active)
        return res

    def isactive(self, date):
        """Check whether the event staring and ending time are spanning a
        given date.

        :param date: a :class:`datetime.datetime` instance

        :returns: True if the event span the current date, e.g, if
            event.starting_date < date < event.ending_date

        >>> date = datetime.datetime(2000, 4, 15)
        >>> duration = datetime.timedelta(30)
        >>> event = Event('test', date, duration, periodic=False)
        >>> event.isactive(datetime.datetime(2000, 4, 19))
        True

        """

        assert type(date) == datetime.datetime

        # 2 cases: either the event is periodic and therefore occurs every year,
        # or it happens only once.

        # non periodic case is simple:
        if self.periodic is False:
            if self.ending_date >= date and self.starting_date <= date:
                self._active = True
            else:
                self._active = False
        else:

            # If periodic, we do not want to use the date as such, but we want
            # to switch to the same year as the event itself. One problem arise
            # when the original year is bissextil.
            try:
                newdate = datetime.datetime(self.starting_date.year,
                                            date.month, date.day)
            except:
                if date.month == 2 and date.day == 29:
                    newdate = datetime.datetime(self.starting_date.year,
                                                date.month, date.day-1)

            if self.ending_date >= newdate and self.starting_date <= newdate:
                self._active = True
            else:
                self._active = False
        return self._active

    def _set_duration(self, duration):
        self._duration = datetime.timedelta(days=duration)
    def _get_duration(self):
        return self._duration
    duration = property(fget=_get_duration,fset=_set_duration,
                        doc="getter/setter for duration. duration is in days.")

    def _get_periodic(self):
        return self._periodic
    periodic = property(fget=_get_periodic, doc="getter of periodic attribute.")

    def _get_active(self):
        return self._active
    active = property(fget=_get_active, doc="getter of active attribute.")

    def _get_name(self):
        return self._name
    name = property(fget=_get_name, doc="returns name of this event.")

    def _get_starting_date(self):
        return self._starting_date
    starting_date = property(fget=_get_starting_date,
                             doc="returns starting date of this event.")

    def _get_ending_date(self):
        return self._ending_date
    ending_date = property(fget=_get_ending_date,
                           doc="returns ending date of this event.")


class Events(object):
    """Define a list of events.

    Events is a list of :class:`~openalea.plantik.simulation.calendar.Event`. This class is
    used by  a :class:`~openalea.plantik.simulation.simulation.SimulationInterface` class.

    You can add or remove Event from the list using the two methods :meth:`add_event` and
    :meth:`remove_event`.

    .. doctest::

        >>> eventsList = Events()
        >>> eventsList.add_event('test', datetime.datetime(2000,4,15), datetime.timedelta(10))
        >>> eventsList.add_event('test2', datetime.datetime(2000,4,15), datetime.timedelta(10))
        >>> eventsList.remove_event('test')
        >>> len(eventsList.events)
        1

    .. note:: events are accessible in 3 different ways:

        * as attribute (with their name) (recommended)
        * from the events attributes list
        * using an index on the objec directly

        The first method is recommended since indices are tricky to manipulate especially if an event is removed.

    The following example shows three ways to acces to an event, given that only one event is added to the event list.

    .. doctest::

        >>> e = Events()
        >>> e.add_event('test', datetime.datetime(2000,4,15), datetime.timedelta(10))
        >>> assert e.test.duration == e.events[0].duration == e[0].duration


    """
    def __init__(self):
        """Empty constructor of Events

        :attributes:

            * :attr:`events` a list of :class:`~openalea.plantik.simulation.calendar.Event` instances
            * :attr:`names` a list of event names
        """
        self._events = []

    def __str__(self):
        res = ""
        for event in self.events:
            res +=  event.__str__() + '\n'
        return res

    def __len__(self):
        return len(self.events)

    def __getitem__(self, i):
        return self.events[i]

    def add_event(self, name, starting_date, duration, periodic=True):
        """add a new event in the pool of events

        :param name: set a label to an event
        :param date: a starting date (:class:`datetime.datetime` instance)
        :param duration: a duration in days (:class:`datetime.timedelta`)
        :param periodic: a boolean to specify if the event is a singl event or is periodic over years

        """
        e = Event(name, starting_date, duration, periodic=periodic)
        if e.name in self.names:
            import warnings
            warnings.warn("Event name already chosen. Conisder changing it or rename your event")
        else:
            self.events.append(e)
            self.__setattr__(name, e)

    def remove_event(self, name):
        """remove an event from the list of events

        :param name: the event's name
        """
        self.__delattr__(name)
        for i, event in enumerate(self.events):
            if event.name == name:
                index = i
                break
        del self.events[index]


    def _get_names(self):
        return [x.name for x in self.events]
    names = property(fget=_get_names,
                     doc="return list of event names stored in :attr:`events`.")


    def _get_events(self):
        return self._events
    events = property(fget=_get_events, doc="returns the list of events")




class SimulationInterface(object):
    """An abstract base class to design simulations.

    This class put together a :class:`~vplants.plantik.simulation.calendar.Calendar`
    class and a list of events :class:`~vplants.plantik.simulation.calendar.Events`
    to ease management of simulations.

    :param dt: the time step in days (default is 1
    :param starting_date: the starting date (default is year 2000)
    :param ending_date: the ending date (default is year 2010)

    :type starting_date: float or integer
    :type ending_date: float or integer

    :attributes:
        * :attr:`calendar` is an instance of :class:`~vplants.plantik.simulation.calendar.Calendar`
        * :attr:`events` is an instance of :class:`~vplants.plantik.simulation.calendar.Events`
        * :attr:`date` is an instance of :class:`datetime.datetime` (alias
          to calendar.date) and is read-only.
        * :attr:`time_elapsed` is an instance of :class:`datetime.timedelta` and is
          read-only.
        * :attr:`ending_year` read-only.
        * :attr:`dt` read-only. use `calendar.dt` to set another value

    ::

        >>> from vplants.plantik.simulation.simulation import SimulationInterface
        >>> sim = SimulationInterface(dt=10)
        >>> sim.calendar.date.year
        2000
        >>> sim.date
        datetime.datetime(2000, 1, 1, 0, 0)
        >>> import datetime
        >>> sim.events.add_event('test', datetime.datetime(2000,4,15), datetime.timedelta(1))
        >>> sim.advance()
        False
        >>> sim.time_elapsed
        datetime.timedelta(10)

    """
    def __init__(self, dt=1., starting_date=2000., ending_date=2010):

        self._ending_date = self.convert_input_date(ending_date)

        # set up the calendar, must convert the floating year to a date before
        date = self.convert_input_date(starting_date)
        self._starting_date = date
        self.calendar = Calendar(year=date.year, month=date.month, day=date.day,
                                delta_in_days=dt)


        # setup a event list with an example, the starting date
        self.events = Events()
        # we store the beginnin of the simulation as an event.
        self.events.add_event('starting_date', date, datetime.timedelta(1), periodic=False)

        #: read-only attribute (in days using datetime.timedelta)
        self._time_elapsed = datetime.timedelta(0.)

        #: read-only attribute, alias to calendar.date
        #self._date = self.calendar.date

    def convert_input_date(self, date):
        if type(date) in [float, int]:
            return self.convert_fractional_year_to_date(date)
        elif type(date) == str:
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
            except:
                raise ValueError("input date does not seem to be in the format year-month-day e.g., 2000-12-30")
            return date
        else:
            raise TypeError("date must be int, float (fractional year) or string format such as 2000-12-30")


    @staticmethod
    def convert_fractional_year_to_date(year):
        """returns a timedelta object given a fractional year

        .. note:: this is a static method

        ::

            Simulation.convert_fractional_year_to_date(2000.5)
            datetime.datetime(2000, 7, 1, 12, 0)

        """
        assert year>=1, "year cannot be less than 1"
        date = datetime.datetime(int(year), 1, 1)
        fraction = (year % 1) *365
        date += datetime.timedelta(fraction)
        return date

    def __str__(self):
        res = "Current time is %s" % str(self._get_date())
        return res

    def _get_starting_date(self):
        return self._starting_date
    starting_date = property(fget=_get_starting_date, doc="getter to starting date")

    def _get_ending_date(self):
        return self._ending_date
    ending_date = property(fget=_get_ending_date, doc="getter to ending date")

    def _get_date(self):
        return self.calendar.date
    date = property(fget=_get_date, doc="returns date from calendar instance")

    def _get_time_elapsed(self):
        return self._time_elapsed
    time_elapsed = property(fget=_get_time_elapsed,
                            doc="returns time elapsed since simulation began in datetime format")

    def _get_dt(self):
        return self.calendar.dt
    def _set_dt(self, dt):
        self.calendar.dt = dt
    dt = property(fget=_get_dt, fset=_set_dt,
                            doc="returns time step datetime format ")


    def advance(self):
        """increment the calendar time by `dt` and check for events activation

        All events have a starting date and a duration. When the calendar advance,
        we must check whether any events englobe the current time. If so, its `active`
        status is set to True. See :class:`~vplants.plantik.simulation.calendar.Event`
        class for details.

        :returns: True if we switched to a new year while advancing current time by `dt`.
        """
        new_year = self.calendar.advance()
        self._time_elapsed += self.dt

        for event in self.events.events:
            event.isactive(self.date)

        return new_year


class Simulation(SimulationInterface):
    """ a simple simulation protocol.

    Simulation is a specialised form of :class:`SimulationInterface`. See
    :class:`SimulationInterface` for the basic usage.

    Constructor is the same constructor as :class:`~vplants.plantik.simulation.simulation.SimulationInterface` for the time being.
    """
    def __init__(self, dt=1, starting_date=2000., ending_date=2010):
        SimulationInterface.__init__(self, dt=dt, starting_date=starting_date,
            ending_date=ending_date)



class RotationConvergence():
    steps = 2  # // Runge-Kutta order 2
    step  = 1.0 / steps



class SimulationStocatree(SimulationInterface):
    def __init__(self, dt=1, starting_date=2000, ending_date=2010,seed=1163078257):
        SimulationInterface.__init__(self, dt=dt, starting_date=starting_date, ending_date=ending_date)


        mydt = datetime.timedelta(dt)
        self.events.add_event('bud_break',
                              datetime.datetime(starting_date, 4, 15),
                              duration=datetime.timedelta(0))
        self.events.add_event('new_cambial_layer',
                              datetime.datetime(starting_date, 5, 15),
                              duration=mydt)
        self.events.add_event('pre_harvest',
                              datetime.datetime(starting_date, 10, 29),
                              duration=mydt)
        self.events.add_event('harvest',
                              datetime.datetime(starting_date, 10, 30),
                              duration=mydt)
        self.events.add_event('autumn',
                              datetime.datetime(starting_date, 11, 1),
                              duration=datetime.timedelta(45))
        self.events.add_event('leaf_fall',
                              datetime.datetime(starting_date, 11, 15),
                              duration=datetime.timedelta(45))
        #to make sure there are no remaining leaves for next year
        self.events.add_event('leaf_out',
                              datetime.datetime(starting_date, 12, 25),
                              duration=mydt)
        self.phase            = 0 #initialisation
        self.error            = False # purpose of that attribut is not clear, seems not used
        self.seed             = seed
        self.base_dt          = dt
        self.number           = 0
        self.rotation_convergence = RotationConvergence()
        self.harvested = False    # purpose of that attribut is not clear, seems not used

        #---------------------------------------------------------------------#
        # Here comes element that should be saved in order to be able to      #
        # restart the simulation from a saved point                           #
        #---------------------------------------------------------------------#

        # the tree representation as a lstring should be set just before saving to avoid duplication
        # and be deleted after loading to continue simulation
        self.lstring          = None

        # Data structure that store output
        # should probably replaced and/or cleaned
        self.data             = None

        # Tree is the unique instance that represent the tree and store tree status
        self.tree             = None

        # Budbreak date is also saved in case the simulation is saved and reloaded
        # between 01/01 when budbreak date is calculated and the calculated date
        self.bud_break        = None


    def load_save(self, lstr, dat, tr, bbreak):
        """
        Gather all simulation element that are necessary to be able to reload it
        before being serialized
        """
        self.lstring = lstr
        self.data = dat
        self.tree = tr
        self.bud_break = bbreak

    def unload_save(self):
        """
        Free some memory by setting some attributs back to None
        """
        self.lstring          = None
        self.data             = None
        self.tree             = None


    def func_leaf_area_init(self, filename='functions.fset', func_name='leaf_area'):
        """read the functions.fset once for all the metamers"""
        self.func_leaf_area = ReadFunction(filename, func_name)
