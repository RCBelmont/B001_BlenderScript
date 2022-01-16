import bpy
from . import PivotPainterPluginVer

bl_info = {
    "name": "PivotPainter",
    "description": "ZeroPivotPainter",
    "author": "RCB",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View 3D > Sidebar > Edit Tab > AutoMirror (panel)",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}


class PivotPainterSelectLink(bpy.types.Operator):
    bl_idname = "pivot_painter.select_linked"
    bl_label = "SelectLink"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.mesh.select_linked(delimit=set())
        return {'FINISHED'}


class PivotPainterSeparate(bpy.types.Operator):
    bl_idname = "pivot_painter.separate"
    bl_label = "Separate"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.mesh.separate(type='SELECTED')
        return {'FINISHED'}


class PivotPainterSetParent(bpy.types.Operator):
    bl_idname = "pivot_painter.set_parent"
    bl_label = "SetParent"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        return {'FINISHED'}


class PivotPainterClearParent(bpy.types.Operator):
    bl_idname = "pivot_painter.clear_parent"
    bl_label = "clearParent"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.object.parent_clear(type='CLEAR')
        return {'FINISHED'}


class PivotPainterSetRotateTag(bpy.types.Operator):
    bl_idname = "pivot_painter.set_rotate_tag"
    bl_label = "SetRotateTag"
    bl_options = {'REGISTER'}

    def execute(self, context):
        for obj in context.selected_objects:
            if not obj.name.endswith("_rotate"):
                obj.name += "_rotate"
            else:
                obj.name = obj.name.replace("_rotate", "")
        return {'FINISHED'}


class PivotPainterDoBake(bpy.types.Operator):
    bl_idname = "pivot_painter.do_bake"
    bl_label = "DoBake"
    bl_options = {'REGISTER'}

    def execute(self, context):
        PivotPainterPluginVer.pp_test()
        return {'FINISHED'}


class PivotPainterPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "PivotPainter"
    bl_category = 'Zero123'

    def draw(self, context):
        layout = self.layout
        layout.split(factor=5.0)
        layout.label(text="网格操作")
        layout.operator("object.join", text="合并")
        layout.operator("pivot_painter.set_parent", text="设置父子关系")
        layout.operator("pivot_painter.clear_parent", text="解除父子关系")
        layout.operator("pivot_painter.set_rotate_tag", text="设置旋转标签")
        layout.operator("pivot_painter.do_bake", text="BB")
        layout.split(factor=5.0)
        layout.label(text="编辑操作")
        layout.operator("object.editmode_toggle", text="切换编辑模式")
        layout.split(factor=5.0)
        layout.operator("pivot_painter.select_linked", text="连续选择")
        layout.operator("mesh.hide", text="隐藏选择")
        layout.operator("mesh.reveal", text="显示隐藏")
        layout.operator("pivot_painter.separate", text="分离选择")


def register():
    bpy.utils.register_class(PivotPainterSelectLink)
    bpy.utils.register_class(PivotPainterDoBake)
    bpy.utils.register_class(PivotPainterSeparate)
    bpy.utils.register_class(PivotPainterSetParent)
    bpy.utils.register_class(PivotPainterClearParent)
    bpy.utils.register_class(PivotPainterSetRotateTag)
    bpy.utils.register_class(PivotPainterPanel)


def unregister():
    bpy.utils.unregister_class(PivotPainterPanel)
    bpy.utils.register_class(PivotPainterSetRotateTag)
    bpy.utils.register_class(PivotPainterClearParent)
    bpy.utils.register_class(PivotPainterSetParent)
    bpy.utils.unregister_class(PivotPainterSeparate)
    bpy.utils.unregister_class(PivotPainterDoBake)
    bpy.utils.unregister_class(PivotPainterSelectLink)


if __name__ == "__main__":
    register()
