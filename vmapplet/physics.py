"""
.. topic:: summary

    The physics module implements functions to calculate the moment of inertia
    and to reorient the frame with respect to torque effects.


    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :References:
        1. Colin Smith, Costes Evelyne, On the Simulation of Apple Trees Using
           Statistical and Biomechanical Principles, INRIA technical report, 2007

    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.physics import *

.. testsetup::

    from openalea.stocatree.physics import *

.. note:: many functions have been reimplemented in optimisation.pyx

"""

from math import sin

import openalea.plantgl.all as pgl

from . import constants
from . import optimisation
from .frame import Frame

error_tolerance = 0.0001


def reorient_frame(initial_hlu, rotation_velocity, length):
    """Reorient frame

    The initial frame is an HLU (Heading Up Left, turtle axes) frame, made of tree orthogonal vectors that indicate the heading,
    upwards and left directions of the beam.

    Then, the HLU frame is rotated around the rotation velocity vector.

    length is used to rotate the frame only when the product of rotation_velocity and length
    is large enough.

    :param initial_hlu: a `Frame` defining the initial HLU frame at the beginning of the season
    :param rotation_velocity:
    :param length: length of metamer

    :returns: a new rotated frame

    .. todo:: describe the algorithm

    .. note:: this function has been optimised to used the rotate function from
        optimisation.pyx that computes the rotation of the AxisAngle around a
        given vector. It replaces the AxisAngle./quaternion of the origninal code of
        MappleT.

     ::

        import openalea.stocatree.optimisation as optimisation
        optimisation.rotate(hlu, pgl.Vector3, length)


    """

    heading = pgl.Vector3(initial_hlu.heading)
    heading.normalize()
    left = pgl.Vector3(initial_hlu.left)
    left.normalize()
    velocity = rotation_velocity.normalize()
    if abs(velocity * length) >= 0.01:
        heading = optimisation.rotate(
            rotation_velocity.x,
            rotation_velocity.y,
            rotation_velocity.z,
            velocity * length,
            heading.x,
            heading.y,
            heading.z,
        )
        left = optimisation.rotate(
            rotation_velocity.x,
            rotation_velocity.y,
            rotation_velocity.z,
            velocity * length,
            left.x,
            left.y,
            left.z,
        )
    heading.normalize()
    left.normalize()
    return Frame(heading, left, pgl.cross(heading, left))


def second_moment_of_area_circle(radius):
    """Returns second moment of area of a circular cross section

    The internodes of the branches are assumed to be circular, with a radius
    :math:`r`, and so the moment of inertia for the cross-section bend around an
    axis on the same plane is :

    .. math::

        I_c = \dfrac{\pi}{4} r^4 = \dfrac{\pi}{64}D^4

    This is used for new shoots with no cambial layers.

    .. note:: This equation is useful in calculating the required strength of masts.
        Taking the area moment of inertia calculated from the previous formula,
        and entering it into Euler's formula gives the maximum force that a mast
        can theoretically withstand.

        .. math::

            F = \dfrac{\pi ^2 E I}{l ^2}

        where

            * E is [Young's modulus|Young (elastic) modulus of material]
            * :math:`\\textrm{I}` is the second moment of area of examined object
            * l is the length of panel

    :param radius: the radius in meters

    :Returns: :math:`I_c`

    :References: MappleT

    .. note::    this function is duplicated in a cython version inside optimisation.pyx

        >>> import openalea.stocatree.optimisation as optimisation
        >>> a = optimisation.second_moment_of_area_circle(1.)


    """

    quarter_pi = 0.7853981633974483
    return quarter_pi * radius * radius * radius * radius


def _second_moment_of_area_circular_section(radius, section):
    """Returns second moment of area (circular section)

    This is a particular case of annular section.

    This is used for code wood of a shoot under the cambial layers.

    :param radius: the radius in meters
    :param section: the section angle in radians

    .. math::

        \dfrac{2}{3}  r^3 \sin \dfrac{section}{2}
    """
    return (2.0 / 3.0) * radius * radius * radius * sin(section * 0.5)


def second_moment_of_area_annular_section(inner_radius, thickness, section):
    """Returns second moment of area (annular section)

    The annular cross section of an internode, with an inner **radius**
    :math:`r_i`, a **thickness** :math:`\theta` and a **section** :math:`\gamma`
    has a second moment of area defined by

    .. math::

        I_s = \dfrac{1}{4}  \left( \left( r_i+ \theta \right)^4-r_i^4\right)\times(\gamma+\sin \gamma)


    This function is used within metamer classes to compute in association the reaction wood


    :param inner_radius: the inner radius in meters
    :param thickness: the thickness in meters
    :param section: the section angle in radians

    .. warning::    this function is duplicated in a cython version inside optimisation.pyx

        >>> import openalea.stocatree.optimisation as optimisation
        >>> a = optimisation.second_moment_of_area_annular_section(1., 0.1, 0.78)
    """

    assert section <= 2 * constants.pi
    return (
        0.125
        * ((inner_radius + thickness) ** 4 - inner_radius**4)
        * (section + sin(section))
    )


def rotate_frame_at_branch(initial_hlu, branching_angle, phyllotactic_angle):
    """Rotate an initial frame around branching and phyllotactic angle

    Given an initial HLU frame, return a new frame after rotation around branching
    and phyllotactic angle.

    :param initial_hlu: the initial HLU frame
    :param branching_angle: the angle between main trunk and the branch.
    :param phyllotactic_angle: the angle related to phyllotaxy

    .. note:: this function has been optimised to used the rotate function from
        optimisation.pyx that computes the rotation of the AxisAngle around a
        given vector. It replaces the AxisAngle./quaternion of the origninal code of
        MappleT.
    .. note:: this function is not part of optimisation.pyx since it already use the
        rotate function and is not called as much as the reorient_frame or rotate
        function itself.
    """

    hlu = Frame(initial_hlu.heading, initial_hlu.up, initial_hlu.left)

    hlu.heading = pgl.Vector3(
        optimisation.rotate(
            initial_hlu.left.x,
            initial_hlu.left.y,
            initial_hlu.left.z,
            branching_angle,
            initial_hlu.heading.x,
            initial_hlu.heading.y,
            initial_hlu.heading.z,
        )
    )
    hlu.up = pgl.Vector3(
        optimisation.rotate(
            initial_hlu.left.x,
            initial_hlu.left.y,
            initial_hlu.left.z,
            branching_angle,
            initial_hlu.up.x,
            initial_hlu.up.y,
            initial_hlu.up.z,
        )
    )
    hlu.heading.normalize()
    hlu.up.normalize()

    hlu.heading = pgl.Vector3(
        optimisation.rotate(
            initial_hlu.heading.x,
            initial_hlu.heading.y,
            initial_hlu.heading.z,
            phyllotactic_angle,
            hlu.heading.x,
            hlu.heading.y,
            hlu.heading.z,
        )
    )
    hlu.up = pgl.Vector3(
        optimisation.rotate(
            initial_hlu.heading.x,
            initial_hlu.heading.y,
            initial_hlu.heading.z,
            phyllotactic_angle,
            hlu.up.x,
            hlu.up.y,
            hlu.up.z,
        )
    )

    hlu.heading.normalize()
    hlu.up.normalize()
    hlu.left = pgl.cross(hlu.up, hlu.heading)

    return hlu


def stress(torque, radius):
    """Stress. Not used for the moment"""

    moment_of_bending = torque.__norm__()

    r4 = radius * radius * radius * radius
    second_moment_of_area = constants.quarter_pi * r4
    return moment_of_bending * radius / second_moment_of_area


def rupture(torque, radius, modulus_of_rupture=50e6):
    """
    :param torque: v3d
    :param radius: si::length

    .. todo: not used for the moment
    """
    return stress(torque, radius) > modulus_of_rupture
