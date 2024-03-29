from typing import Union

from math import acos

from openalea.plantgl.all import Vector3, dot

from .. import constants
from ..physics import (
    rotate_frame_at_branch,
    second_moment_of_area_annular_section,
    reaction_wood_target,
    second_moment_of_area_circle,
)
from ..srandom import boolean_event
from ..enums import Zone, FruitState, LeafState


class CambialLayer:
    """A simple layer class to manage cambial layers

    :param float thickness:  the thickness of the layer (default 0)
    :param float radius: position of the layer in the cross section (default 0)

    contains also a reaction wood attribute that will be used to store information

    This class is used by :class:`metamer_data` class.
    """

    def __init__(self, thickness=0, radius=0):
        self.thickness = thickness
        self.radius = radius
        self.reaction_wood = 0.0
        self.second_moment_of_area = 0.0


class MetamerData:
    r"""Class to define metamer data structure


    :Some definition:

    The torque, also called moment or moment of force is the
    tendency of a force to rotate an object about an axis.
    The symbol for torque is :math:`\tau`. The magnitude of torque depends
    on the force applied, the length of the lever arm connecting the axis
    to the point of force application, and the angle between the two.

    .. math::

        \boldsymbol \tau = \mathbf{r}\times \mathbf{F}\,\!= rF\sin \theta\,\!

    """

    def __init__(
        self,
        floral=False,
        number=0,
        hlu=None,
        zone: Union[None, Zone] = None,
        observation=None,
        parent_observation=None,
        parent_unit_id=None,
        parent_fbr_id=None,
        parent_tree_id=0,
        p_angle=0.0,
        b_angle=0.0,
        wood=None,
        internode=None,
        fruit=None,
        leaf=None,
    ):
        """**Constructor**


        Leaf, internode, fruit and wood must be provided

        :param bool floral:
        :param int number: rank of the metamer in the GU
        :param Frame hlu:
        :param int zone:
        :param int observation:
        :param float p_angle: phyllotactic angle in degrees
        :param float b_angle: branching angle in degrees
        :param wood: a :class:`~openalea.stocatree.wood.Wood` instance
        :param internode: a :class:`~openalea.stocatree.internode.Internode` instance
        :param fruit: a :class:`~openalea.stocatree.fruit.Fruit` instance
        :param leaf: a :class:`~openalea.stocatree.leaf.Leaf` instance

        """
        """
        Parameters added by Han, commented on 02-05-2011:
        parent_unit_id: the id of the parent unit (the unit where the metamer is located)
        parent_fbr_id: the id of the parent branch (the branch where the metamer is located)
        # If the parent_fbr_id is 0, it represents "trunk".
        """
        if leaf is None:
            raise ValueError("leaf must be provided as a Leaf class")
        else:
            self.leaf = leaf

        if fruit is None:
            raise ValueError("fruit must be provided as a Fruit class")
        else:
            self.fruit = fruit

        if wood is None:
            raise ValueError("wood must be provided as a Wood class")
        else:
            self.wood = wood

        if internode is None:
            raise ValueError("internode must be provided as a Internode class")
        else:
            self.internode = internode

        self.number = number  # Yield the rank of the metamer
        self.closest_apex = 0  # Distance to the closest apex
        self.farthest_apex = 0  # Distance to the farthest apex
        self.sons_nb = 0  # Cumulated sum of metamer sons
        self.pruning_react = True  # wether the metamer could react to pruning
        self.pruned_data = None  # If metamer was below the pruning point, this will contain the data required to determine pruning reaction that will be passed on previous metamers (rankwise), i.e. reacting position from cutting point [0,2], closest_apex, farthest_apex, sons_nb

        self.observation = observation
        self.parent_observation = (
            parent_observation  # Yield the shoot type of that metamer
        )
        self.parent_unit_id = parent_unit_id
        self.parent_fbr_id = parent_fbr_id
        self.parent_tree_id = parent_tree_id

        try:
            self.zone = zone
        except Exception:
            pass

        self.hlu = hlu
        self.cumulated_mass = 0.0  # [kg]
        self.radius = self.leaf.petiole_radius  # petiole_radius is in m
        self.offset = 0  # used to shift first branching node to keep it from disapearing into cambial growth
        self.cumulated_torque = Vector3(0.0, 0.0, 0.0)
        self.developped = False  # to avoid more than 1 lateral shoot
        self.phyllotactic_angle = (
            p_angle  # azimuth / parent metamer (around h) #TODO must be in [0,2pi]
        )
        self.branching_angle = b_angle  # TODO must be in [0,2pi]
        self.rigidity = 0.0  # in Pa * m**4
        self.age = 0  # in days
        self.year = 0
        self.length = self.internode._min_length  # internode units is in m
        if floral:
            self.fruit.state = FruitState.FLOWER
        else:
            self.fruit.state = FruitState.NO_FLOWER

        self.trunk = False

        # Vector3D are initilised to 0,0,0 but could have been anything.
        self.rotation_memory = Vector3(
            0.0, 0.0, 0.0
        )  # remaining rotation after harvest
        self.rotation_velocity = Vector3(
            0.0, 0.0, 0.0
        )  # acting_rotation + rotation_memory
        self.acting_rotation = Vector3(0.0, 0.0, 0.0)  # due to mass and tropism actions
        self.position = Vector3(0.0, 0.0, 0.0)  # absolute

        # Rotation velocity is normalized and its norm is saved in rv_norm
        self.rv_norm = self.rotation_velocity.normalize()
        self.season_initial_heading = self.hlu.heading  # used to compute reaction wood
        self.external_layer = 0  # index in vector cambial::pool

        # TEST
        self.layers = []
        self.nlayers = 0
        self.total_second_moment_of_area = 0.0

        self.pre_harvest_mass = 0.0  # in g # used to compute rotation_memory
        self.pre_harvest_radius = 0  # in meters
        self.pre_harvest_rotation = Vector3(0.0, 0.0, 0.0)

        """
        The conditional on 'number' is to get around a bug in LPFG.
        LPFG creates lots of temporary instances of objects that are
        never used.  We only want the constructor to have an effect
        when the object is one that is actually used in the structure
        and not a temporary object.
        """
        if self.number:
            self.season_initial_heading = self.hlu.heading
            layer = CambialLayer(thickness=self.radius, radius=0)
            self.layers.append(layer)
            self.nlayers += 1

        # The following attributes were added by Han on 29-04-2011
        # They are mainly used in the "attribute_list" for statistics output
        self.leaf_state = ""
        self.leaf_area = 0
        # Leaf area returned from plangGL after light interception
        self.ta_pgl = 0
        # Silhouette area returned from plantGL after light interception
        self.sa_pgl = 0
        self.star_pgl = 0

        # Added by Han on 11-07-2012, as a flag to control first-year sylleptic growth
        self.sylleptic = False
        # Flag to set if a metamer should be pruned
        self.to_prune = False
        # Flag to signal a cut
        self.cut = False

    # def reorient_frame(self, initial_hlu, rotation_velocity, length):
    #    self.hlu.reorient_frame(initial_hlu, rotation_velocity, length)

    def __str__(self):
        res = "\n number %s\n" % self.number
        res += "radius petiole %s\n" % (self.radius)
        res += "length %s\n" % self.length
        res += "age %s \n" % (self.age)
        res += "cumulated_mass %s \n" % (self.cumulated_mass)
        res += "fruit_mass %s and fruit mass unit\n" % (self.fruit.mass)
        res += "fruit state is %s\n" % (self.fruit.state)
        res += "leaf state %s \n" % (self.leaf.state)
        res += "developed %s \n" % (self.developped)
        res += "observation %s \n" % (self.observation)
        res += "parent observation %s \n" % (self.parent_observation)
        return res

    def organ_activity(self, simulation):
        """
        Update status of fruit and leaf components
        """

        additional_fruit = 0

        if self.fruit._state == FruitState.NO_FLOWER:
            if simulation.events.harvest.active:
                self.fruit.state = FruitState.FRUIT_SCAR

        elif self.fruit._state == FruitState.FLOWER:
            if self.age > self.fruit._flower_duration:
                if boolean_event(self.fruit._probability):
                    self.fruit.state = FruitState.FRUIT
                    additional_fruit += 1
                else:
                    self.fruit.state = FruitState.FRUIT_SCAR
        elif self.fruit._state == FruitState.FRUIT:
            if simulation.events.harvest.active:
                self.fruit.state = FruitState.FRUIT_SCAR
                self.fruit.mass = 0.0
            else:
                self.fruit.mass = (
                    self.fruit.compute_mass()
                )  # useless ? mass already set by compute_mass
        elif self.fruit._state == FruitState.FRUIT_SCAR:
            self.fruit.mass = 0.0

        if self.leaf.state != LeafState.SCAR:
            if simulation.events.leaf_out.active:
                self.leaf.state = LeafState.SCAR

            if simulation.events.leaf_fall.active:
                if boolean_event(self.leaf.fall_probability):
                    self.leaf.state = LeafState.SCAR

            if self.leaf.state == LeafState.GROWING:
                # If the value of "maturation" needs to be manipulated for sensitivity
                # analysis for instance, it would be easier to calculate the leaf
                # area based on the function (.fset) rather than using the numpy array (Han, 04-2011)
                if self.leaf.age < self.leaf.maturation:
                    self.leaf.compute_area_from_func(
                        self.number, simulation.func_leaf_area
                    )

                self.leaf.compute_mass()

        # added by Han on 29-04-2011
        if self.leaf.state == LeafState.SCAR:
            self.leaf.area = 0
            self.ta_pgl = 0
            self.sa_pgl = 0
            self.star_pgl = 0
        # Note that, in lpy code, the update_metamer_parameters() is used in advance of the
        # organ_activity(). Thus the self.leaf_state and the self.leaf_area should be updated
        # here rather than in update_metamer_parameters()
        self.leaf_state = self.leaf.state
        self.leaf_area = self.leaf.area

        return additional_fruit

    def update_metamer_parameters(self, simulation, cambial=None):
        """update metamer parameters

        :param Simulation simulation: Simulation instance
        :param cambial:


        fields required from simualtion:dt, cal.year(), cal.current_data().new_cambial_layer
            pre_harvest,bud_break

        Update :
            * age.
            * cambial layer if required
            * moment of area
            * rigidity

        """
        self.age += simulation.dt.days
        self.leaf.age += simulation.dt.days
        self.fruit.age += simulation.dt.days

        # new cambial layer event
        if (
            self.year < simulation.date.year
            and simulation.events.new_cambial_layer.active
        ):
            self.season_initial_heading = self.hlu.heading
            # if we create a new layer, then computation on previous one will
            # be redundant. Compute them once for all
            second_moment_of_area = (
                second_moment_of_area_annular_section(
                    self.layers[-1].radius,
                    self.layers[-1].thickness,
                    self.layers[-1].reaction_wood,
                )
                * self.wood._reaction_wood_inertia_coefficient
            )
            self.layers[-1].second_moment_of_area = second_moment_of_area
            # cumulate the second moment
            self.total_second_moment_of_area += second_moment_of_area
            layer = CambialLayer(radius=self.radius)
            self.layers.append(layer)
            self.nlayers += 1

        # TEST if not the central layer
        # TODO days or seconds ?
        if self.nlayers >= 2:
            r = reaction_wood_target(
                self.hlu.up, self.hlu.heading, self.season_initial_heading
            )
            if r > self.layers[-1].reaction_wood:
                self.layers[-1].reaction_wood += (
                    self.wood._reaction_wood_rate
                    * simulation.dt.days
                    * (r - self.layers[-1].reaction_wood)
                )

        # Growth of internode
        if self.age < self.internode._elongation_period:
            self.length += (
                self.internode.growth_rate(self.zone) * simulation.dt.days
            )  # TODO this is in meters per day (merge to seconds ? )

        # Updating second_moment_of_area
        second_moment_of_area = (
            self.total_second_moment_of_area + second_moment_of_area_circle(self.radius)
        )
        second_moment_of_area += (
            second_moment_of_area_annular_section(
                self.layers[-1].radius,
                self.layers[-1].thickness,
                self.layers[-1].reaction_wood,
            )
            * self.wood._reaction_wood_inertia_coefficient
        )

        self.rigidity = second_moment_of_area * self.wood._youngs_modulus

        if simulation.events.pre_harvest.active:
            self.pre_harvest_mass = self.cumulated_mass
            self.pre_harvest_rotation = self.rotation_velocity

        if simulation.events.bud_break.active:
            self.pre_harvest_radius = self.radius

    def compute_mass(self, mr=None, mb=None):
        r"""Compute the cumulated mass

        :param float mr:
        :param float mb:

        .. math::

            M = \pi r^2 h  \rho_{\rm{wood}} + m_{\rm{leaf}} + m_{\rm{fruit}}

        """
        self.cumulated_mass = (
            constants.pi * self.radius * self.radius * self.length * self.wood._density
        )
        self.cumulated_mass += self.leaf.mass + self.fruit.mass

        if mr is not None:
            self.cumulated_mass += mr.cumulated_mass
        if mb is not None:
            self.cumulated_mass += mb.cumulated_mass

    def calculate_rotation_velocity(self, simulation, stake=True):
        r"""Calculate the rotation velocity

        :param bool stake: (default is True)

        Calculate the rotation velocity of a torque

        .. math::

            \Omega_\tau = \frac{\tau}{R}

        where R is the rigidity and :math:`\tau` the cumulated total torque.

        The memory rotation depends on the lost masses

        .. math::

            \Omega_m =  \frac{\Delta m }{m} ?

        .. math::

            \Omega' = \Omega_\tau + \Omega_m

        .. math::

            \Omega = \Omega' * \alpha + (1-\alpha)*\Omega
        """
        if stake and self.trunk:
            self.rotation_velocity = Vector3()
            return None

        # Calculate the rotation velocity (Taylor-Hell, 2005)
        self.acting_rotation = self.cumulated_torque / self.rigidity

        # Hypothesis: the shape memory is proportional to the mass
        # removed (inspired by Almeras. 2002)
        # The if-else here was added by Han on 22-04-2011 to avoid the case that
        # self.pre_harvest_mass is sometimes euqal to 0
        if simulation.events.harvest.active:
            if self.pre_harvest_mass != 0:
                delta_mass = (
                    self.pre_harvest_mass - self.cumulated_mass
                ) / self.pre_harvest_mass
            else:
                delta_mass = 0
            self.rotation_memory = self.pre_harvest_rotation * delta_mass

        new_rotation_velocity = self.acting_rotation + self.rotation_memory
        # Hypothesis: The total rotation velocity is the sum of the acting
        # rotation and the shape memory
        self.rotation_velocity = (
            new_rotation_velocity * simulation.rotation_convergence.step
            + self.rotation_velocity * (1.0 - simulation.rotation_convergence.step)
        )

        self.rv_norm = self.rotation_velocity.normalize()

    def update_position(self, left_metamer_position=None):
        """Update position according to the left metamer position

        :param left_metamer_position: (default None)

        If there is no left metamer, the position is simply::

            position = HLU.heading * length

        otherwise::

            position = left metamer position + HLU.heading * length

        """
        if left_metamer_position is None:
            self.position = self.hlu.heading * self.length
        else:
            self.position = left_metamer_position + self.hlu.heading * self.length

    def pruning_reaction_angle(self, phylo_angle):
        """
        :param hlu: Frame
        :param phyllo_angle: float
        :param farthest_apex: int
        :param number: int
        :returns branching_angle: float
        :returns phyllotactic_angle: float
        """

        # Determining angle between heading and vertical
        angle_to_vert = round(acos(dot(self.hlu.heading.normed(), Vector3(0, 0, 1))), 2)

        # Fixing the ratio of that angle to be used as branching angle depending on the pruning intensity
        vert_ratio = 1 - ((1.0 * self.number) / (self.number + self.farthest_apex))

        new_branching_angle = vert_ratio * angle_to_vert

        # Determining a possible phyllotactic angle that will divert the less from vertical
        angles = []

        for i in range(5):
            hlu = rotate_frame_at_branch(
                self.hlu, new_branching_angle, i * phylo_angle + self.phyllotactic_angle
            )
            angles.append((acos(dot(hlu.heading.normed(), Vector3(0, 0, 1)))))
        return (
            new_branching_angle,
            angles.index(min(angles)) * phylo_angle + self.phyllotactic_angle,
        )

    # expose child properties to make then available in e.g. mtg export
    @property
    def fruit_age(self):
        return self.fruit.age

    @property
    def fruit_mass(self):
        return self.fruit.mass

    @property
    def leaf_age(self):
        return self.leaf.age

    @property
    def leaf_mass(self):
        return self.leaf.mass


def _clamp_if_near_zero(data, tol=0.0001):
    if data < tol and data > -tol:
        return 0
    else:
        return data


def clamp_v3d_components_if_near_zero(v):
    """clamp values near zero in a Vector3

    :param Vector3 v:

    Used when saving results into MTG only.
    """
    v.x = _clamp_if_near_zero(v.x)
    v.y = _clamp_if_near_zero(v.y)
    v.z = _clamp_if_near_zero(v.z)
