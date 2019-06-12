import bmesh
from collections import defaultdict

BM_Seq = [bmesh.types.BMEdgeSeq, bmesh.types.BMVertSeq, bmesh.types.BMFaceSeq, list]
BM_Elem = [bmesh.types.BMVert, bmesh.types.BMEdge, bmesh.types.BMFace]


def pretty_print(obj):
    print(pretty_string(obj))


def pretty_string(obj):
    if type(obj) in BM_Seq or type(obj) in BM_Elem:
        return b_string(obj)
    elif type(obj) == dict or type(obj) == defaultdict:
        return dict_string(obj)
    else:
        print(type(obj))
        return str(obj)


def dict_string(d):
    print_str = ""
    for key, value in d.items():
        print_str += f'{pretty_string(key)}: {pretty_string(value)}\n'

    return print_str[:-1]


def b_string(obj):
    if type(obj) in BM_Seq:
        return seq_string(obj)
    elif type(obj) == bmesh.types.BMVert:
        return vert_print(obj)
    elif type(obj) == bmesh.types.BMEdge:
        return edge_print(obj)
    elif type(obj) == bmesh.types.BMFace:
        return face_print(obj)
    else:
        return None


def vert_print(v):
    return f'<Vert #{v.index} {co_string(v.co)}>'


def edge_print(e):
    string1 = f'<Edge #{e.verts[0].index} => #{e.verts[1].index}'
    string2 = f'{co_string(e.verts[0].co)} => {co_string(e.verts[1].co)}>'

    return string1 + ' | ' + string2


def face_print(f):
    return '<Face>'


def seq_string(obj):
    print_string = '['
    for index, list_item in enumerate(obj):
        print_string += b_string(list_item)
        if index != len(obj):
            print_string += ', '
    print_string += ']'
    return print_string


def co_string(co):
    return f'({float_string(co[0])}, {float_string(co[1])}, {float_string(co[2])})'


def float_string(number):
    return "%.1f" % number