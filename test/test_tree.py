from vmapplet.organs.tree import Tree

tolerance = 1e-16


def test_tree():
    tree = Tree()
    tree.phyllotactic_angle = 3.14 / 2.0
    tree.convert_to_degrees()
    tree.convert_to_radians()
    assert (
        tree.phyllotactic_angle > 3.139 / 2.0 and tree.phyllotactic_angle < 3.15 / 2.0
    )

    tree.convert_to_degrees()
    tree.convert_to_radians()
