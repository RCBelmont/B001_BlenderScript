import mathutils

import bpy
import bmesh

targetObj = bpy.context.active_object
targetMesh = targetObj.data


def check_uv(mesh):
    uv_count = len(mesh.uv_layers)
    if uv_count == 0:
        mesh.uv_layers.new(name="UVChannel_1")
        mesh.uv_layers.new(name="UVChannel_2")
        mesh.uv_layers.new(name="UVChannel_3")
    elif uv_count == 1:
        mesh.uv_layers[0].name = "UVChannel_1"
        mesh.uv_layers.new(name="UVChannel_2")
        mesh.uv_layers.new(name="UVChannel_3")
    elif uv_count == 2:
        mesh.uv_layers[0].name = "UVChannel_1"
        mesh.uv_layers[1].name = "UVChannel_2"
        mesh.uv_layers.new(name="UVChannel_3")
    else:
        mesh.uv_layers[0].name = "UVChannel_1"
        mesh.uv_layers[1].name = "UVChannel_2"
        mesh.uv_layers[2].name = "UVChannel_3"

    vertColorCount = len(mesh.vertex_colors)
    if vertColorCount == 0:
        mesh.vertex_colors.new(name="Col")
    else:
        mesh.vertex_colors[0].name = "Col"


def check_uv_recursion(rootObj):
    check_uv(rootObj.data)
    for ch in rootObj.children:
        check_uv_recursion(ch)


def get_pivot(obj):
    wl = obj.matrix_world.to_translation()  # Gives world location
    r = wl[0]
    g = wl[1]
    b = wl[2]
    return mathutils.Vector((r, g, b))


def bake_pivot_info(obj):
    mesh = obj.data

    pivot = get_pivot(obj)

    # Calc MaxDis
    max_distance = 0
    for loop in mesh.loops:
        vertexIdx = loop.vertex_index
        vert = mesh.vertices[vertexIdx]
        distanceToZero = (obj.matrix_world @ vert.co - pivot).length
        if distanceToZero > max_distance:
            max_distance = distanceToZero
    for loop in obj.data.loops:
        vertIdx = loop.vertex_index
        vert = mesh.vertices[vertIdx]
        offset = obj.matrix_world @ vert.co - pivot
        length = offset.length
        loopID = loop.index
        mesh.uv_layers[1].data[loopID].uv = (offset.x, offset.z)
        mesh.uv_layers[2].data[loopID].uv = (-offset.y, length / max_distance)
        a = 0
        if obj.name.endswith("_rotate"):
            a = 1
        xAixs = obj.matrix_world @ mathutils.Vector((1, 0, 0, 0))
        # TODO:DELETE PRINT
        print("X: " + str(xAixs))
        mesh.vertex_colors[0].data[loopID].color = (xAixs.x * 0.5 + 0.5, xAixs.z * 0.5 + 0.5, -xAixs.y * 0.5 + 0.5, a)


def bake_pivot_recursion(obj):
    bake_pivot_info(obj)
    for ch in obj.children:
        bake_pivot_recursion(ch)


def main():
    # TODO:DELETE PRINT
    print('\n')
    obj_list = bpy.context.selected_objects
    ## check UV
    for obj in obj_list:
        check_uv_recursion(obj)
        bake_pivot_recursion(obj)
        isRootPart = len(obj.children) > 0
        if isRootPart:
            for loop in obj.data.loops:
                obj.data.uv_layers[1].data[loop.index].uv = (0, 0)
                obj.data.uv_layers[2].data[loop.index].uv = (0, 0)

    all_obj_list = []
    for obj in obj_list:
        all_obj_list.append(obj)
        for child in obj.children:
            all_obj_list.append(child)

    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_obj_list:
        obj.select_set(True)

    bpy.ops.object.duplicate()
    bpy.ops.object.join()


main()
