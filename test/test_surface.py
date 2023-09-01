from vmapplet.tools import surface


class TestSurface:
    def test_leaf(self):
        surface.leafSurface(6)

    def test_ground(self):
        surface.groundSurface(12)

    def test_petal(self):
        surface.petalSurface(12)
