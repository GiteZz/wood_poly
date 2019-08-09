from blender_helper.print_helper import pretty_print

def get_dir_edge(edge, starting_vert=None, normalized=True):
    first_vert, second_vert = edge.verts
    if starting_vert is not None:
        diff = sum(starting_vert.co - first_vert.co)
        if diff > 1 or diff < -1:
            first_vert, second_vert = second_vert,  first_vert

    dir_vec = second_vert.co - first_vert.co
    if normalized:
        return dir_vec.normalized()
    else:
        return dir_vec

