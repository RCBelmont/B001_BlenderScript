import bpy

bl_info = {
    "name": "WeightToVertColor",
    "description": "WeightToVertColor",
    "author": "RCB",
    "version": (0, 0, 1),
    "blender": (3, 2, 0),
    "location": "View 3D > Sidebar > RCBTool > WeightToVertColor (panel)",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}
class OPT_TransferWeightToColor(bpy.types.Operator):
    bl_idname = "rcb_weight2color.transfer"
    bl_label = "TransferWeight"
    bl_options = {'REGISTER'}
    
    def execute(self, context):

        pass
    @classmethod
    def poll(cls, context: 'Context'):
        return True;


class VIEW3D_PT_WeightToColorPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'WeightToColor'
    bl_category = 'RCBTool'

    def draw(self, context):
        layout = self.layout
        if len(context.selected_objects) > 0:
            actObj = bpy.types.Object(context.active_object)
            layout.label(text="TargetObject:")
            layout.label(text="    " + actObj.name)
            layout.split(factor=10)
            if actObj.vertex_groups.active_index != -1:
                layout.label(text="Source VertGroup:")
                layout.label(text="    " + actObj.vertex_groups.active.name)
            else:
                layout.label(text="Need A Active VertexGroup!")
            layout.split(factor=25)
            meshData = bpy.types.Mesh(actObj.data)
            if meshData.color_attributes.active_color_index != -1:
                layout.label(text="Target ColorAttribute:")
                layout.label(text="    " + meshData.color_attributes.active.name)
            else:
                layout.label(text="Need A Active ColorAttribute!")
            layout.split(factor=25)
        else:
            layout.label(text="Please Select A Mesh Object")


cls = (
    VIEW3D_PT_WeightToColorPanel,
)


def register():
    for c in cls:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(cls):
        bpy.utils.unregister_class(c)
