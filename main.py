import bpy
import bmesh
import sys

module_path = "D:/Programmeer projecten/wood_poly"
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import blender_helper.collection_helper
import blender_helper.print_helper
import function_collection

import importlib
importlib.reload(blender_helper.collection_helper)
importlib.reload(blender_helper.print_helper)
importlib.reload(function_collection)


from blender_helper.collection_helper import ConnectionMesh
import blender_helper.print_helper as print_helper

if __name__ == "__main__":

    print("============== Starting script ====================")

    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    mesh = ConnectionMesh(bm)

    pair_list = function_collection.get_edge_face_pairs(mesh)
    print_helper.pretty_print(pair_list)
    print()
    pair_list = function_collection.sort_pair_list(pair_list)

    n_vertices = function_collection

    print(print_helper.pretty_print(pair_list))

    print("============== End script ====================")
