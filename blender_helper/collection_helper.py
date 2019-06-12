from collections import defaultdict

def get_vertex_edge_link(mesh):
    """
    mesh should be a bmesh
    :param mesh: bmesh
    :return: dict[vertex] = [edge1, ..., edge k]
    """

    link_dict = defaultdict(list)

    for edge in mesh.edges:
        for vert in edge.verts:
            link_dict[vert].append(edge)

    return link_dict