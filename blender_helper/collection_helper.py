from collections import defaultdict


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


class WoodConnector:
    """
    This class is used to contain the information about connection pieces
    :return:
    """
    def __init__(self, mesh, middle_vert, top_rim):
        self.mesh = mesh
        self.middle_vert = middle_vert
        self.top_rim = top_rim
        self.top_faces = None
        self.pairs = None

    def set_top_faces(self, faces):
        self.top_faces = faces

    def set_pairs(self, pairs):
        self.pairs = pairs


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