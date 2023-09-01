from openalea.plantgl.all import Vector3

from vmapplet import Simulation, Options
from vmapplet.organs.metamer import MetamerData, CambialLayer
from vmapplet.optimisation import reaction_wood_target
from vmapplet.organs.wood import Wood
from vmapplet.organs.fruit import AppleFruit
from vmapplet.organs.leaf import AppleLeaf
from vmapplet.organs.internode import Internode
from vmapplet.physics import Frame
from vmapplet.enums import FruitState


def test_reaction_wood_target():
    up = Vector3(1.0, 1.0, 1.0)
    heading = Vector3(1.0, 0.0, -0.0)
    previous_heading = Vector3(-1.0, -1.0, -1.0)

    reaction_wood_target(up, heading, previous_heading)

    # r statement
    up = Vector3(0.0, 0.0, 1.0)
    heading = Vector3(0.0, 1.0, 0.0)
    previous_heading = Vector3(3.1, 1.0, 1.0)
    reaction_wood_target(up, heading, previous_heading)


def test_cambial():
    c = CambialLayer()
    assert c.thickness == 0
    assert c.radius == 0
    assert c.reaction_wood == 0
    assert c.second_moment_of_area == 0


class TestMetamerData:
    data = MetamerData(
        hlu=Frame(),
        wood=Wood(),
        leaf=AppleLeaf(),
        fruit=AppleFruit(),
        internode=Internode(),
        number=2,
    )
    sim = Simulation(options=Options())

    def test_organ_activity(self):
        self.data.organ_activity(self.sim)
        self.sim.events.harvest._active = True
        self.data.organ_activity(self.sim)
        self.data.fruit._state = FruitState.FLOWER
        self.data.age = 50
        for i in range(1, 10):
            self.data.organ_activity(self.sim)

    def test_update_parameters(self):
        self.data.update_metamer_parameters(self.sim)

    def test_compute_mass(self):
        self.data.compute_mass()

    def test_calculate_rotation_velocity(self):
        self.data.trunk = True
        self.data.calculate_rotation_velocity(self.sim)
        self.sim.events.harvest._active = True
        self.data.pre_harvest_mass = 1
        self.data.calculate_rotation_velocity(self.sim, stake=False)

    def test_update_position(self):
        self.data.update_position()
        self.data.update_position(left_metamer_position=Vector3(1, 1, 1))
