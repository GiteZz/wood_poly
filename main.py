import bpy
import bmesh
import sys

module_path = "D:/Programmeer projecten/wood_poly"
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import blender_helper.collection_helper
import blender_helper.print_helper
import blender_helper.vector_helper
import blender_helper.lin_alg_helper
import function_collection

import importlib
importlib.reload(blender_helper.collection_helper)
importlib.reload(blender_helper.print_helper)
importlib.reload(blender_helper.vector_helper)
importlib.reload(blender_helper.lin_alg_helper)
importlib.reload(function_collection)


import blender_helper.collection_helper as collection_helper
import blender_helper.print_helper as print_helper

if __name__ == "__main__":

    print("============== Starting script ====================")

    obj = bpy.context.active_object
    scene = bpy.context.scene
    or_bmesh = bmesh.new()
    or_bmesh.from_mesh(obj.data)
    or_colmesh = collection_helper.ConnectionMesh(or_bmesh)

    pair_list = function_collection.get_edge_face_pairs(or_colmesh)
    pair_list = function_collection.sort_pair_list(pair_list)

    hat_dict = function_collection.create_hat(pair_list)
    function_collection.create_thickness(hat_dict)


    for vert, bm in hat_dict.items():
        bm_mesh = bm.mesh
        name = "hat_" + str(vert.index)
        mesh = bpy.data.meshes.new("mesh")
        obj = bpy.data.objects.new(name, mesh)
        scene.objects.link(obj)
        bm_mesh.to_mesh(mesh)
        bm_mesh.free()

    print(print_helper.pretty_print(pair_list))

    print("============== End script ====================")
