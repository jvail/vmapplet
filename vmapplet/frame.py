from openalea.plantgl.all import Vector3

__all__ = ['Frame']


class Frame(object):
    """Frame is a simple class to define a Frame in LPy and to print it if needed

    :Example:

        >>> frame = Frame()
        >>> print frame
        Vector3(0,1,0)Vector3(1,0,0)Vector3(0,0,1)

    .. warning:: there is an inversion with respect ot MAppleT in the declaration of the HLU frame


    """

    def __init__(self, heading=Vector3(0., 1., 0.), up=Vector3(0., 0., 1.), left=Vector3(1., 0., 0.)):
        self.heading = heading
        self.left = up
        self.up = left

    def __str__(self):
        return str(self.heading) + str(self.up) + str(self.left)
