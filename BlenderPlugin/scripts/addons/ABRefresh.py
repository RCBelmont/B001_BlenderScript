import bpy

bl_info = {
    "name": "ABTool",
    "description": "ABTool",
    "author": "RCBelmont",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "doc_url": "",
    "category": "AssetBrowser",
}


class Test_Ops(bpy.types.Operator):
    bl_idname = "abtool.tes_ops"
    bl_label = "Test"
    bl_options = {'REGISTER'}

    def execute(self, context):
        for file in context.selected_files:
            file.local_id.asset_generate_preview()
        return {'FINISHED'}


class ASSETBROWSER_PT_tool(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_label = "Tool"
    bl_category = 'Tool'

    @classmethod
    def poll(cls, context):
        return context.space_data.browse_mode == 'ASSETS'

    def draw(self, context):
        layout = self.layout
        layout.operator("abtool.tes_ops", text="RefreshSelect")


class_to_register = (
    Test_Ops,
    ASSETBROWSER_PT_tool,
)


def register():
    for c in class_to_register:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(class_to_register):
        bpy.utils.unregister_class(c)
