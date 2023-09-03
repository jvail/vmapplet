from openalea.plantgl.all import Vector3, Vector4

from vmapplet.physics import (
    stress,
    rupture,
    second_moment_of_area_annular_section,
    second_moment_of_area_circle,
    second_moment_of_area_circular_section,
    Frame,
    rotate_frame_at_branch,
)


def test_stress():
    torque = Vector3(100, 100, 500)
    radius = 0.1
    stress(torque, radius)


def test_rupture():
    torque = Vector3(0, 0, 50e5)
    radius = 1
    assert rupture(torque, radius) is False
    torque = Vector3(0, 0, 50e6)
    radius = 1
    assert rupture(torque, radius) is True


def test_second_moment_of_area_circle():
    second_moment_of_area_circle(1)


def test_second_moment_of_area_circular_section():
    second_moment_of_area_circular_section(1, 1)


def test_second_moment_of_area_annular_section():
    second_moment_of_area_annular_section(1, 1, 1)


def test_Frame():
    v1 = Vector3(2, 1, 1)
    v2 = Vector3(1, 2, 1)
    v3 = Vector3(1, 1, 2)
    Frame(v1, v2, v3)


def test_rotate_frame_at_branch():
    v1 = Vector3(2, 1, 1)
    v2 = Vector3(1, 2, 1)
    v3 = Vector3(1, 1, 2)
    frame = Frame(v1, v2, v3)
    rotate_frame_at_branch(frame, 45, 45)
