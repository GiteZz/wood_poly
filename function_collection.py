import blender_helper.collection_helper as collection_helper
from blender_helper.print_helper import pretty_print, pretty_string
import blender_helper.vector_helper as vector_helper
from collections import defaultdict
import bmesh
import mathutils

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def get_edge_face_pairs(mesh):
    """
    Constructs for each vertex the pairs of edges that are next to each other because they connect to the same face.

    :param mesh: bmesh object
    :return: dict[vertex] = [[edge1, edge2], [edge3, edge5], ...]
    """

    vert_edge = collection_helper.get_vertex_edge_link(mesh)
    vert_face = collection_helper.get_vertex_face_link(mesh)

    pair_dict = {}

    for vert in mesh.verts:
        faces = vert_face[vert]
        edges = vert_edge[vert]

        pair_list = []

        for face in faces:
            pair_list.append(intersection(face.edges, edges))

        pair_dict[vert] = pair_list

    return pair_dict


def sort_pair_list(pair_dict):
    """
    if given pair list [[e1, e2], [e3, e4], [e3, e2]]
    this function will give [[e1, e2], [e2, e3], [e3, e4]]
    :param pair_list: dict[vertex] = [[edge1, edge2], [edge3, edge5], ...]
    :return:
    """
    new_pair_dict = {}

    for vert in pair_dict:
        old_pair_list = pair_dict[vert]
        new_pair_list = []

        # method for selecting the edge where to start the loop
        # when the pairs don't make a complete circle the process should start with an edge
        # that only exist in one pair
        edge_count = defaultdict(int)

        for pair in old_pair_list:
            edge_count[pair[0]] += 1
            edge_count[pair[1]] += 1

        connect_edge = None
        for edge, amount in edge_count.items():
            if amount == 1:
                connect_edge = edge

        if connect_edge is None:
            connect_edge = old_pair_list[0][0]

        # Search for pair that contains connect_edge and add that edge to the new_pair_list
        while len(old_pair_list) != 0:
            connect_index = None
            for index, pair in enumerate(old_pair_list):
                if connect_edge in pair:
                    connect_index = index

            new_pair = old_pair_list.pop(connect_index)

            # Make sure that the pair edges are inserted correctly into pair list
            # The end of pair n-1 should always be equal to the start of pair n
            if connect_edge == new_pair[0]:
                connect_edge = new_pair[1]
                new_pair_list.append([new_pair[0], new_pair[1]])
            else:
                connect_edge = new_pair[0]
                new_pair_list.append([new_pair[1], new_pair[0]])

        new_pair_dict[vert] = new_pair_list

    return new_pair_dict


def create_hat(pair_dict, distance=0.5):
    """

    :param pair_dict: dict[vertex] = [[e1, e2], [e2, e3], ...] -> should be sorted
    :return: dict[vertex] = bmesh
    """
    bmesh_dict = {}

    for vert, pairs in pair_dict.items():
        bm = bmesh.new()
        new_middle = bm.verts.new(vert.co)
        closed_pairs = pairs[0][0] == pairs[-1][1]

        new_vertices = []
        for pair in pairs:
            dir_edge1 = vector_helper.get_dir_edge(pair[0], starting_vert=vert)
            dir_edge2 = vector_helper.get_dir_edge(pair[1], starting_vert=vert)
            new_vertices.append(bm.verts.new(vert.co + distance * dir_edge1))

            dir_middle = ((dir_edge1 + dir_edge2) / 2).normalized()
            new_vertices.append(bm.verts.new(vert.co + distance * dir_middle))

        if not closed_pairs:
            dir_edge = vector_helper.get_dir_edge(pairs[-1][1], starting_vert=vert)
            new_vertices.append(bm.verts.new(vert.co + distance * dir_edge))

        # add the faces to the hat vertices 0,1,2 and the middle should form a quad, then 2,3,4 and the middle
        for i in range(0, len(new_vertices) - 2, 2):
            bm.faces.new((new_vertices[i+0], new_vertices[i+1], new_vertices[i+2], new_middle))

        if closed_pairs:
            bm.faces.new((new_vertices[-2], new_vertices[-1], new_vertices[0], new_middle))

        bmesh_dict[vert] = bm

    return bmesh_dict

def create_thickness(hat_dict):
    for vert, mesh in hat_dict:
        av_normal = mathutils.Vector((0.0, 0.0, 0.0))
        for face in mesh.faces:
            av_normal += face.normal.normalized()
        av_normal /= len(mesh.faces)


