import mathutils

def get_norm_from_face(face):
    p1 = face.verts[0]
    p2 = face.verts[1]
    p3 = face.verts[2]

    nor_dir = (p2.co - p1.co).cross((p3.co - p1.co))
    return nor_dir.normalized()