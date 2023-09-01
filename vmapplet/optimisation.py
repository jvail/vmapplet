from math import fabs, acos

import cppyy

from .frame import Frame

rotate = cppyy.gbl.optimization.rotate
second_moment_of_area_annular_section = (
    cppyy.gbl.optimization.second_moment_of_area_annular_section
)
second_moment_of_area_circle = cppyy.gbl.optimization.second_moment_of_area_circle
get_new_radius = cppyy.gbl.optimization.get_new_radius
# _reaction_wood_target = cppyy.gbl.optimization.reaction_wood_target

import openalea.plantgl.all as pgl


def reorient_frame(initial_hlu, rotation_velocity, rv_norm, length):
    h = pgl.Vector3(initial_hlu.heading)
    h.normalize()
    l = pgl.Vector3(initial_hlu.left)
    l.normalize()

    # vl = rotation_velocity.normalize() #_ look at v3d length definition
    # vl is replaced by rv_norm

    if fabs(rv_norm * length) >= 0.01:
        h = pgl.Vector3(
            rotate(
                rotation_velocity.x,
                rotation_velocity.y,
                rotation_velocity.z,
                rv_norm * length,
                h.x,
                h.y,
                h.z,
            )
        )
        l = pgl.Vector3(
            rotate(
                rotation_velocity.x,
                rotation_velocity.y,
                rotation_velocity.z,
                rv_norm * length,
                l.x,
                l.y,
                l.z,
            )
        )
    h.normalize()
    l.normalize()
    return Frame(h, l, pgl.cross(h, l))


# cppyy complains maybe clash with boost PyObjects and plantgl types
# def reaction_wood_target(a, b, c):
#     # print('reaction_wood_target')
#     return _reaction_wood_target(list(a), list(b), list(c))


def reaction_wood_target(up, heading, previous_heading):
    cos_gh = pgl.Vector3(0.0, 0.0, 1.0) * heading
    cos_pu = previous_heading * up
    cos_ph = previous_heading * heading

    inclination = 0
    if cos_pu * cos_ph >= 0.0:
        try:
            inclination = acos(cos_ph)
        except Exception:
            pass
            # print(str(cos_ph))
    else:
        try:
            inclination = -acos(cos_ph)
        except Exception:
            pass
            # print(str(cos_ph))
    percentage = 0.1635 * (1.0 - cos_gh) - 0.1778 * inclination
    r = 3.14159 * 2.0 * percentage

    if r < 0.0:
        r = 0.0
    elif r > 3.14159:
        r = 3.141459

    return r


def max(a, b):
    if a > b:
        return a
    else:
        return b
