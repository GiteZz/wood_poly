import bpy
import bmesh
import sys

module_path = "E:/Programmeer projecten/wood_poly"
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import blender_helper.collection_helper
import blender_helper.print_helper
import blender_helper.vector_helper
import blender_helper.lin_alg_helper
import create_mesh_functions

import importlib
importlib.reload(blender_helper.collection_helper)
importlib.reload(blender_helper.print_helper)
importlib.reload(blender_helper.vector_helper)
importlib.reload(blender_helper.lin_alg_helper)
importlib.reload(create_mesh_functions)


import blender_helper.collection_helper as collection_helper
import blender_helper.print_helper as print_helper

if __name__ == "__main__":

    print("============== Starting script ====================")

    obj = bpy.context.active_object
    scene = bpy.context.scene
    or_bmesh = bmesh.new()
    or_bmesh.from_mesh(obj.data)
    or_colmesh = collection_helper.ConnectionMesh(or_bmesh)

    pair_dict = create_mesh_functions.get_edge_face_pairs(or_colmesh)
    pair_dict = create_mesh_functions.sort_pair_list(pair_dict)

    for vert, pairs in pair_dict.items():
        bm = bmesh.new()
        new_middle = bm.verts.new(vert.co)
        # Boolean to check if the faces surrounding the vertex close
        closed_pairs = pairs[0][0] == pairs[-1][1]
        av_normal = or_colmesh.vertex_normal[vert]
        wood_con = blender_helper.collection_helper.WoodConnector(bm, new_middle, av_normal, pair_dict[vert])

        create_mesh_functions.create_hat(wood_con)
        create_mesh_functions.create_thickness(wood_con, thickness=7)
        create_mesh_functions.add_holes(wood_con)
        create_mesh_functions.fill_hole_faces(wood_con)
        create_mesh_functions.to_middle_point(wood_con)

        name = "hat_" + str(vert.index)
        mesh = bpy.data.meshes.new("mesh")
        obj = bpy.data.objects.new(name, mesh)
        scene.objects.link(obj)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()


    print("============== End script ====================")
