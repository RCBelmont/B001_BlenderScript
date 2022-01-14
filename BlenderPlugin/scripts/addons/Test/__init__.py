bl_info = {
    "name": "AddonLearn",
    "description": "LearnHowToDevAddon",
    "author": "RCB",
    "version": (2, 5, 3),
    "blender": (2, 80, 0),
    "location": "View 3D > Sidebar > Edit Tab > AutoMirror (panel)",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

import bpy


class Test(bpy.types.Operator):
    bl_idname = "learn.test"
    bl_label = "Learn"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # TODO:DELETE PRINT
        print("GOOD")
        return {'FINISHED'}


def register():
    print("register")
    bpy.utils.register_class(Test)


def unregister():
    bpy.utils.unregister_class(Test)


if __name__ == "__main__":
    register()
