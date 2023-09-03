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

"""

from math import acos, cos, sin, pow, fabs

import openalea.plantgl.all as pgl

from . import constants
from .frame import Frame

error_tolerance = 0.0001


def reaction_wood_target(up, heading, previous_heading):
    r"""Reaction wood target

    The reaction wood is proportional to the change in inclination
    over a season (Almeras, 2001). Hypothesis: The reaction wood is
    also proportional to the inclination from gravity.

    .. math::

        P_r = 0.1635 - 0.1778 \theta_s

    where :math:`P_r` is the radial portion of the outermost cambial layer that
    become reaction wood and :math:`\theta_s` is the change in inclination of the
    internode over the season (i.e., the cahnge in :math:`\vec{H}`, the heading
    vector of the HLU frame since the start of the spring.

    In order to also take into account the gravity, The firs term in the equation above
    must be multiply by a coefficient that varies with the angle between the internode and
    :math:`\vec{u}` a unit vector opposite to  :math:`-\vec{g}`

    :param Vector3 up:
    :param heading: vector3
    :param previous_heading: vector3
    :returns: reaction_wood (double)
    """

    # multiply by gravity normalised
    cos_gh = pgl.Vector3(0.0, 0.0, 1.0) * heading
    cos_pu = previous_heading * up
    cos_ph = previous_heading * heading
    inclination = 0.0

    if cos_pu * cos_ph >= 0.0:
        try:
            inclination = acos(cos_ph / 1.0001)
        except Exception:
            print("Problem with acos(cos_ph) where cos_ph=%f" % cos_ph)
            inclination = 0.0
    else:
        try:
            inclination = -acos(cos_ph)
        except Exception:
            tol = 1e-6
            try:
                inclination = -acos(cos_ph - tol)
                ValueError("try again with tol set %s %s" % (cos_ph, cos_ph - 1.0))
            except Exception:
                print("cos+_pu=", cos_pu, " cos_ph=", cos_ph, "cosgh=", cos_gh)
                print(cos_ph - 1.0)
                raise ValueError("Problem with acos(cos_ph) where cos_ph=%f" % cos_ph)

    percentage = 0.1635 * (1.0 - cos_gh) - 0.1778 * inclination
    r = constants.two_pi * percentage

    if r < 0.0:
        r = 0.0
    elif r > constants.pi:
        r = constants.pi

    return r


def rotate(
    v3x: float, v3y: float, v3z: float, angle: float, vx: float, vy: float, vz: float
) -> pgl.Vector3:
    c = cos(angle)
    t2 = 1 - c
    t6 = t2 * v3x
    t7 = t6 * v3y
    s = sin(angle)
    t9 = s * v3z
    t11 = t6 * v3z
    t12 = s * v3y
    t19 = t2 * v3y * v3z
    t20 = s * v3x
    t24 = v3z * v3z
    R00 = c + t2 * v3x * v3x
    R01 = t7 - t9
    R02 = t11 + t12
    R10 = t7 + t9
    R11 = c + t2 * v3y * v3y
    R12 = t19 - t20
    R20 = t11 - t12
    R21 = t19 + t20
    R22 = c + t2 * t24

    return pgl.Vector3(
        [
            R00 * vx + R01 * vy + R02 * vz,
            R10 * vx + R11 * vy + R12 * vz,
            R20 * vx + R21 * vy + R22 * vz,
        ]
    )


def reorient_frame(initial_hlu, rotation_velocity, rv_norm, length):
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


    """

    h = pgl.Vector3(initial_hlu.heading)
    h.normalize()
    l = pgl.Vector3(initial_hlu.left)
    l.normalize()

    # vl = rotation_velocity.normalize() #_ look at v3d length definition
    # vl is replaced by rv_norm

    if fabs(rv_norm * length) >= 0.01:
        h = rotate(
            rotation_velocity.x,
            rotation_velocity.y,
            rotation_velocity.z,
            rv_norm * length,
            h.x,
            h.y,
            h.z,
        )
        l = rotate(
            rotation_velocity.x,
            rotation_velocity.y,
            rotation_velocity.z,
            rv_norm * length,
            l.x,
            l.y,
            l.z,
        )
    h.normalize()
    l.normalize()
    return Frame(h, l, pgl.cross(h, l))


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


    """

    quarter_pi = 0.7853981633974483
    return quarter_pi * radius * radius * radius * radius


def second_moment_of_area_circular_section(radius, section):
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
        pyx that computes the rotation of the AxisAngle around a
        given vector. It replaces the AxisAngle./quaternion of the origninal code of
        MappleT.
    .. note:: this function is not part of pyx since it already use the
        rotate function and is not called as much as the reorient_frame or rotate
        function itself.
    """

    hlu = Frame(initial_hlu.heading, initial_hlu.up, initial_hlu.left)

    hlu.heading = rotate(
        initial_hlu.left.x,
        initial_hlu.left.y,
        initial_hlu.left.z,
        branching_angle,
        initial_hlu.heading.x,
        initial_hlu.heading.y,
        initial_hlu.heading.z,
    )
    hlu.up = rotate(
        initial_hlu.left.x,
        initial_hlu.left.y,
        initial_hlu.left.z,
        branching_angle,
        initial_hlu.up.x,
        initial_hlu.up.y,
        initial_hlu.up.z,
    )
    hlu.heading.normalize()
    hlu.up.normalize()

    hlu.heading = rotate(
        initial_hlu.heading.x,
        initial_hlu.heading.y,
        initial_hlu.heading.z,
        phyllotactic_angle,
        hlu.heading.x,
        hlu.heading.y,
        hlu.heading.z,
    )
    hlu.up = rotate(
        initial_hlu.heading.x,
        initial_hlu.heading.y,
        initial_hlu.heading.z,
        phyllotactic_angle,
        hlu.up.x,
        hlu.up.y,
        hlu.up.z,
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


def get_new_radius(
    ra: float, rb: float, exponent: float = 2.49, previous_rt: float = -1.0
):
    rap = pow(ra, exponent)
    rbp = pow(rb, exponent)
    newrt = pow(rap + rbp, 1.0 / exponent)
    return newrt
