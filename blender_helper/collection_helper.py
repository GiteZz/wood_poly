from collections import defaultdict
import mathutils

class ConnectionMesh:
    """
    This class is used to group a bmesh together with dicts that are used to quickly get all
    the faces connected to a vertex etc.
    """
    def __init__(self, mesh):
        """

        :param mesh: bmesh object
        """
        self.mesh = mesh
        self.verts = mesh.verts
        self.edges = mesh.edges
        self.faces = mesh.faces
        self.vertex_edge = get_vertex_edge_link(mesh)
        self.vertex_face = get_vertex_face_link(mesh)
        self.edge_face = get_edge_face_link(mesh)
        self.vertex_normal = get_vertex_normal(self)

class WoodConnector:
    """
    This class is used to contain the information about connection pieces
    :return:
    """
    def __init__(self, mesh, middle_vert, top_rim):
        self.mesh = mesh
        self.middle_vert = middle_vert
        self.extended_middle = None
        self.top_rim_verts = top_rim
        self.bottom_rim_verts = None
        self.top_faces = None
        self.pairs = None
        self.is_closed = None
        self.bottom_plane = None

    def set_pairs(self, pairs):
        self.pairs = pairs

    def set_closed_pair(self, bool):
        self.is_closed = bool

    def set_bottom_rim_verts(self, verts):
        self.bottom_rim_verts = verts

    def set_extended_middle(self, vert):
        self.extended_middle = vert

    def set_bottom_plane(self, plane):
        self.bottom_plane = plane

    def get_top_verts_pairs(self):
        """
        As constructed in create_hat the top_rim_vertices should be ordered like
        [edge_vert, pair_vert, edge_vert, pair_verts, edge_vert]
        This function will give the vertices for each pair ([edge_vert, pair_vert, edge_vert])
        :return:
        """
        pair_verts = []
        for i in range(len(self.pairs)):
            pair_verts.append(self.top_rim_verts[i*2 + 0: i*2 + 3])

        if self.is_closed:
            pair_verts[-1].append(self.top_rim_verts[0])

        return pair_verts


def get_vertex_edge_link(mesh):
    """

    :param mesh: bmesh object
    :return: dict[vertex] = [edge1, ..., edge k]
    """

    link_dict = defaultdict(list)

    for edge in mesh.edges:
        for vert in edge.verts:
            link_dict[vert].append(edge)

    return link_dict


def get_edge_face_link(mesh):
    """

    :param mesh: bmesh object
    :return: dict[edge] = [face1, ..., face k]
    """

    link_dict = defaultdict(list)

    for face in mesh.faces:
        for edge in face.edges:
            link_dict[edge].append(face)

    return link_dict


def get_vertex_face_link(mesh):
    """

    :param mesh: bmesh object
    :return: dict[vertex] = [face1, ..., face k]
    """

    link_dict = defaultdict(list)

    for face in mesh.faces:
        for vert in face.verts:
            link_dict[vert].append(face)

    return link_dict


def get_vertex_normal(mesh):
    """

    :param mesh: ConnetionMesh
    :return: dict[v1] = Vector((n1, n2, n3))
    """
    normal_dict = {}
    for vert, faces in mesh.vertex_face.items():
        av_normal = mathutils.Vector((0.0, 0.0, 0.0))
        for face in faces:
            av_normal += face.normal
        av_normal /= len(faces)
        normal_dict[vert] = av_normal

    return normal_dict