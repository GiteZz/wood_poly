import bpy
import bmesh
import sys

module_path = "D:/Programmeer projecten/wood_poly"
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import blender_helper.collection_helper
import blender_helper.print_helper

import importlib
importlib.reload(blender_helper.collection_helper)
importlib.reload(blender_helper.print_helper)


import blender_helper.collection_helper as collection_helper
import blender_helper.print_helper as print_helper

if __name__ == "__main__":

    print("============== Starting script ====================")

    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)

    vertex_edge_link = collection_helper.get_vertex_edge_link(bm)

    print(print_helper.pretty_print(vertex_edge_link))

    print("============== End script ====================")
