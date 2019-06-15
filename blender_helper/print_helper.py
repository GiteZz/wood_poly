import bmesh
import bpy
from collections import defaultdict
import mathutils

BM_Seq = [bmesh.types.BMEdgeSeq, bmesh.types.BMVertSeq, bmesh.types.BMFaceSeq, list, bpy.types.bpy_prop_collection]
BM_Elem = [bmesh.types.BMVert, bmesh.types.BMEdge, bmesh.types.BMFace, mathutils.Vector]


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
    elif type(obj) == bmesh.types.BMVert or type(obj) == bpy.types.MeshVertex:
        return vert_print(obj)
    elif type(obj) == bmesh.types.BMEdge or type(obj) == bpy.types.MeshEdge:
        return edge_print(obj)
    elif type(obj) == bmesh.types.BMFace or type(obj) == bpy.types.MeshPolygon:
        return face_print(obj)
    elif type(obj) == mathutils.Vector:
        return vector_print(obj)
    else:
        return None


def vert_print(v, print_co=False):
    if print_co:
        return f'<Vert #{v.index} {co_string(v.co)}>'
    else:
        return f'<Vert #{v.index}>'


def edge_print(e, print_co=False, print_v_index=False):
    if print_v_index:
        string1 = f'<Edge #{e.verts[0].index} => #{e.verts[1].index}'
    else:
        string1 = f'<Edge #{e.index}'
    string2 = f'{co_string(e.verts[0].co)} => {co_string(e.verts[1].co)}>'

    if print_co:
        return string1 + ' | ' + string2
    else:
        return string1 + '>'


def face_print(f):
    return '<Face>'


def vector_print(v):
    print("vector")
    return f'<Vector ({float_string(v[0])}, {float_string(v[1])}, {float_string(v[2])})>'


def seq_string(obj):
    print_string = '['
    for index, list_item in enumerate(obj):
        print_string += b_string(list_item)
        print_string += ', '
    print_string = print_string[:-2] + ']'
    return print_string


def co_string(co):
    return f'({float_string(co[0])}, {float_string(co[1])}, {float_string(co[2])})'


def float_string(number):
    return "%.1f" % number