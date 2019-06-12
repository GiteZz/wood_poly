from collections import defaultdict

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