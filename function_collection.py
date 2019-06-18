import blender_helper.collection_helper as collection_helper
from blender_helper.collection_helper import WoodConnector
from blender_helper.print_helper import pretty_print, pretty_string
import blender_helper.vector_helper as vector_helper
import blender_helper.lin_alg_helper as lin_alg_helper
from collections import defaultdict
import bmesh
import mathutils
import math

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


def create_hat(wood_con, distance=20):
    """

    :param pair_dict: dict[vertex] = [[e1, e2], [e2, e3], ...] -> should be sorted
    :return: dict[vertex] = WoodConnector
    """

    # new_vertices should be ordered like [edge_vert, pair_vert, edge_vert, pair_verts, edge_vert]
    # where edge_vert is a new vert place on top the old edges
    # and pair_vert is a new vert placed between the two edges of a pair
    # each trio of edge_vert, pair_vert, edge_vert should belong to a pair
    new_vertices = []
    for pair in wood_con.pairs:
        dir_edge1 = vector_helper.get_dir_edge(pair[0], starting_vert=wood_con.middle_vert)
        dir_edge2 = vector_helper.get_dir_edge(pair[1], starting_vert=wood_con.middle_vert)

        edge_vert = wood_con.mesh.verts.new(wood_con.middle_vert.co + distance * dir_edge1)
        new_vertices.append(edge_vert)
        dir_middle = ((dir_edge1 + dir_edge2) / 2).normalized()
        new_vertices.append(wood_con.mesh.verts.new(wood_con.middle_vert.co + distance * dir_middle))

    if not wood_con.is_closed:
        dir_edge = vector_helper.get_dir_edge(wood_con.pairs[-1][1], starting_vert=wood_con.middle_vert)
        edge_vert = wood_con.mesh.verts.new(wood_con.middle_vert.co + distance * dir_edge)
        new_vertices.append(edge_vert)

    wood_con.set_top_rim_verts(new_vertices)


def create_thickness(wood_con, thickness=10):
    """
    This method creates the mesh
    :param hat_dict:
    :param col_mesh:
    :return:
    """
    print("Creating thickness")

    av_normal = -1 * wood_con.av_normal

    d = -1 * (av_normal * wood_con.middle_vert.co)
    plane = (av_normal[0], av_normal[1], av_normal[2], d)

    # Find the point that is furthest from the middle point according to the normal vector
    max_dist = 0
    max_vert = wood_con.top_rim_verts[0]
    for rim_vert in wood_con.top_rim_verts:
        dist = lin_alg_helper.dist_point_plane(plane, rim_vert.co)
        if dist > max_dist:
            max_dist = dist
            max_vert = rim_vert

    # Create new vertices that are the rim vertices extended along the normal vector
    dn = -1 * (av_normal * max_vert.co) - thickness * av_normal * av_normal
    f_plane = (av_normal[0], av_normal[1], av_normal[2], dn)
    new_vertices = []
    for rim_vert in wood_con.top_rim_verts:
        dist = lin_alg_helper.dist_point_plane(f_plane, rim_vert.co)
        v = wood_con.mesh.verts.new((rim_vert.co + dist * av_normal))
        new_vertices.append(v)
    wood_con.set_bottom_rim_verts(new_vertices)

    # if the pairs are not closed the middle vertex has to also be extended
    dist = lin_alg_helper.dist_point_plane(f_plane, wood_con.middle_vert.co)
    middle_extended = wood_con.mesh.verts.new((wood_con.middle_vert.co + dist * av_normal))
    wood_con.set_extended_middle(middle_extended)

    if not wood_con.is_closed:
        wood_con.mesh.edges.new((middle_extended, wood_con.middle_vert))

    for i in range(len(new_vertices) - 1):
        v1_b = new_vertices[i]
        v2_b = new_vertices[i + 1]

        v1_t = wood_con.top_rim_verts[i]
        v2_t = wood_con.top_rim_verts[i + 1]

        wood_con.mesh.faces.new((v1_t, v1_b, v2_b, v2_t))

    vs_b = new_vertices[0]
    ve_b = new_vertices[-1]

    vs_t = wood_con.top_rim_verts[0]
    ve_t = wood_con.top_rim_verts[-1]
    if wood_con.is_closed:
        wood_con.mesh.faces.new((vs_t, vs_b, ve_b, ve_t))
    else:
        wood_con.mesh.faces.new((vs_t, vs_b, middle_extended, wood_con.middle_vert))
        wood_con.mesh.faces.new((wood_con.middle_vert, middle_extended, ve_b, ve_t))

    wood_con.set_bottom_plane(f_plane)

    print("end with thickness")


def add_holes(wood_con, hole_radius=1.5, nut_radius=3, bolt_dist=4, location=5, bolt_thickness=2.5):

    top_pair_bolt_vertices = []
    bottom_pair_bolt_vertices = []
    top_pair_nut_vertices = []
    bottom_pair_nut_vertices = []

    for pair_verts in wood_con.get_top_verts_pairs():
        # z_new = -1 * col_mesh.vertex_normal[dict_vert]
        y_new = (pair_verts[2].co - pair_verts[0].co).normalized()
        x_new = (wood_con.middle_vert.co - pair_verts[1].co).normalized()
        z_new = x_new.cross(y_new).normalized()

        # create the matrices to allow the verts to lay in the plane
        rot_matrix = mathutils.Matrix((x_new, y_new, z_new)).transposed()
        co_middle = pair_verts[1].co + x_new * location
        circle_vertices = 12
        bolt_angle = (2 * math.pi) / circle_vertices

        top_bolt_vertices = []
        bottom_bolt_vertices = []
        top_nut_vertices = []
        bottom_nut_vertices = []
        b_plane = wood_con.bottom_plane

        # Calculate bolt distance
        p = mathutils.Vector((-nut_radius, 0, 0))
        meas_vert = rot_matrix * p + co_middle
        circle_dist = lin_alg_helper.point_to_plane_via_dir(meas_vert, z_new, b_plane)
        if circle_dist < 0:
            circle_dist += bolt_thickness
        else:
            circle_dist -= bolt_thickness
        print("circle: " + str(circle_dist))

        # create pipe for bolt
        for i in range(circle_vertices):
            p = mathutils.Vector((math.cos(i * bolt_angle), math.sin(i * bolt_angle), 0)) * hole_radius

            vert_top = rot_matrix * p + co_middle
            top_bolt_vertices.append(wood_con.mesh.verts.new(vert_top))

            vert_middle = vert_top + circle_dist * z_new
            bottom_bolt_vertices.append(wood_con.mesh.verts.new(vert_middle))

        # Fill holes for the boltpipe
        for i in range(circle_vertices):
            v1_t = top_bolt_vertices[i]
            v1_b = bottom_bolt_vertices[i]
            v2_t = top_bolt_vertices[(i + 1) % circle_vertices]
            v2_b = bottom_bolt_vertices[(i + 1) % circle_vertices]
            wood_con.mesh.faces.new((v1_t, v1_b, v2_b, v2_t))

        nut_angle = (2 * math.pi) / 6
        # create pipe for nut
        for i in range(6):
            p = mathutils.Vector((math.cos(i * nut_angle), math.sin(i * nut_angle), 0)) * nut_radius

            vert_top = rot_matrix * p + co_middle + circle_dist * z_new
            top_nut_vertices.append(wood_con.mesh.verts.new(vert_top))

            dist = lin_alg_helper.point_to_plane_via_dir(vert_top, z_new, b_plane)
            vert_bottom = vert_top + dist * z_new
            bottom_nut_vertices.append(wood_con.mesh.verts.new(vert_bottom))

        # Fill holes for nutpip
        for i in range(6):
            v1_t = top_nut_vertices[i]
            v1_b = bottom_nut_vertices[i]
            v2_t = top_nut_vertices[(i + 1) % 6]
            v2_b = bottom_nut_vertices[(i + 1) % 6]
            wood_con.mesh.faces.new((v1_t, v1_b, v2_b, v2_t))

        circle_amount_half = len(bottom_bolt_vertices) // 2
        first_half_bolt = bottom_bolt_vertices[0:circle_amount_half + 1]
        second_half_bolt = bottom_bolt_vertices[circle_amount_half:] + [bottom_bolt_vertices[0]]

        first_half_bolt.extend([top_nut_vertices[3], top_nut_vertices[2], top_nut_vertices[1], top_nut_vertices[0]])
        second_half_bolt.extend([top_nut_vertices[0], top_nut_vertices[5], top_nut_vertices[4], top_nut_vertices[3]])

        wood_con.mesh.faces.new(first_half_bolt)
        wood_con.mesh.faces.new(second_half_bolt)

        top_pair_bolt_vertices.append(top_bolt_vertices)
        bottom_pair_bolt_vertices.append(bottom_bolt_vertices)
        top_pair_nut_vertices.append(top_nut_vertices)
        bottom_pair_nut_vertices.append(bottom_nut_vertices)

    wood_con.set_bolt_verts(top_pair_bolt_vertices, bottom_pair_bolt_vertices)
    wood_con.set_nut_verts(top_pair_nut_vertices, bottom_pair_nut_vertices)


def fill_hole_faces(w_con):
    for i in range(len(w_con.pairs)):
        fill_single_hole(w_con.get_top_verts_pairs()[i], w_con.top_bolt_verts[i], w_con.middle_vert, w_con.mesh)
        fill_single_hole(w_con.get_bottom_verts_pairs()[i], w_con.bottom_nut_verts[i], w_con.extended_middle, w_con.mesh)


def fill_single_hole(pair_verts, hole_verts, middle_vert, mesh):
    # print(pair_verts)
    # print(hole_verts)
    # print(middle_vert)
    # print(mesh)
    circle_amount_half = len(hole_verts) // 2
    print("=========================================")
    pretty_print(pair_verts)
    pretty_print(hole_verts)
    first_half = hole_verts[0:circle_amount_half + 1]
    second_half = hole_verts[circle_amount_half:] + [hole_verts[0]]
    first_half.extend([pair_verts[1], pair_verts[2], middle_vert])
    second_half.extend([middle_vert, pair_verts[0], pair_verts[1]])
    print(first_half)
    print(second_half)
    mesh.faces.new(first_half)
    mesh.faces.new(second_half)
