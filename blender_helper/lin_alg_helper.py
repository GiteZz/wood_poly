import mathutils
import math

def get_norm_from_face(face):
    p1 = face.verts[0]
    p2 = face.verts[1]
    p3 = face.verts[2]

    nor_dir = (p2.co - p1.co).cross((p3.co - p1.co))
    return nor_dir.normalized()

def dist_point_plane(plane, point):
    """

    :param plane: (a, b, c, d)
    :param point: (x, y, z)
    :return: distance from point to plane
    """
    # |a*x + b*y + c*z + d|
    top = abs(plane[0]*point[0] + plane[1]*point[1] + plane[2]*point[2] + plane[3])
    # sqrt(a^2 + b^2 + c^2)
    bottom = math.sqrt(math.pow(plane[0], 2) + math.pow(plane[1], 2) + math.pow(plane[2], 2))

    return top/bottom