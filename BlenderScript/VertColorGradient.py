import bpy


def main():
    obj_list = bpy.context.selected_objects
    for obj in obj_list:
        mesh = obj.data
        vertColorCount = len(mesh.vertex_colors)
        if vertColorCount <= 0:
            mesh.vertex_colors.new(name="Col")
        else:
            mesh.vertex_colors[0].name = "Col"
        maxZ = 0
        minZ = 0
        for loop in mesh.loops:
            vertIdx = loop.vertex_index
            vert = mesh.vertices[vertIdx]
            z = vert.co.z
            if z > maxZ:
                maxZ = z
            if z < minZ:
                minZ = z
        totalLength = maxZ - minZ
        for loop in mesh.loops:
            vertIdx = loop.vertex_index
            vert = mesh.vertices[vertIdx]
            deltaZ = (vert.co.z - minZ) / totalLength
            mesh.vertex_colors[0].data[loop.index].color = (deltaZ, 0, 0, 0)


main()
