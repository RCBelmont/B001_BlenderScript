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

vert_group_check = False
vert_color_check = False


class OPT_SwitchModeWeight(bpy.types.Operator):
    bl_idname = "rcb_weight2color.switch_mode_weight"
    bl_label = "SwitchWeightModeTool"
    bl_options = {'REGISTER'}

    def execute(self, context):
        print(context.mode)
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
        return {"FINISHED"}


class OPT_TransferWeightToColor(bpy.types.Operator):
    bl_idname = "rcb_weight2color.transfer"
    bl_label = "TransferWeightToColor"
    bl_options = {'REGISTER'}

    def execute(self, context):
        act_obj = bpy.types.Object(context.active_object)
        mesh_data = bpy.types.Mesh(act_obj.data)
        vert_group = act_obj.vertex_groups.active
        vert_color_idx = mesh_data.color_attributes.active_color_index
        attr = bpy.types.FloatColorAttribute(mesh_data.color_attributes.active_color)
        for vert in mesh_data.vertices:
            idx = vert.index
            try:
                weight = vert_group.weight(idx)
            except RuntimeError:
                weight = 0.0
            attr.data[idx].color = (weight, 0, 0, 0)
        self.report({'INFO'}, 'Transfer Done!!')
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


def get_key_string(category, operator):
    kc = bpy.context.window_manager.keyconfigs
    if kc.addon.keymaps[category].keymap_items.find(operator) != -1:
        km = kc.addon.keymaps[category].keymap_items[operator]
        return '(' + km.to_string() + ')'
    return ""


class VIEW3D_PT_WeightToColorPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'WeightToColor'
    bl_category = 'RCBTool'

    @classmethod
    def poll(cls, context):
        return bpy.context.mode == "OBJECT" or bpy.context.mode == "PAINT_WEIGHT"

    def draw(self, context):
        layout = self.layout
        layout.operator('rcb_weight2color.switch_mode_weight',
                        text='SwitchMode' + get_key_string('3D View', 'rcb_weight2color.switch_mode_weight'))

        global vert_group_check
        global vert_color_check
        vert_group_check = False
        vert_color_check = False
        if len(context.selected_objects) > 0:
            actObj = bpy.types.Object(context.active_object)
            if type(actObj.data) != bpy.types.Mesh:
                layout.alert = True
                layout.label(text='Please Select Object With Mesh')
                return
            layout.label(text="TargetObject:")
            layout.label(text="    " + actObj.name)
            layout.split(factor=10)
            # Check VertGroup
            if actObj.vertex_groups.active_index != -1:
                layout.label(text="Source VertGroup:")
                layout.label(text="    " + actObj.vertex_groups.active.name)
                vert_group_check = True
            else:
                layout.alert = True
                layout.label(text="Need A Active VertexGroup!")
            layout.split(factor=25)
            meshData = bpy.types.Mesh(actObj.data)
            # Check VertColorAttribute
            if meshData.color_attributes.active_color_index != -1:
                layout.label(text="Target ColorAttribute:")
                layout.label(text="    " + meshData.color_attributes.active.name)
                vert_color_check = True
            else:
                layout.alert = True
                layout.label(text="Need A Active ColorAttribute!")
            layout.split(factor=25)
            # Draw Opt
            if vert_color_check and vert_group_check:
                layout.operator('rcb_weight2color.transfer')

        else:
            layout.alert = True
            layout.label(text="Please Select A Mesh Object")


cls = (
    OPT_SwitchModeWeight,
    OPT_TransferWeightToColor,
    VIEW3D_PT_WeightToColorPanel,
)

custom_keymaps = []


def menu_func(self, context):
    self.layout.operator('rcb_weight2color.switch_mode_weight')


def register():
    global vert_group_check
    global vert_color_check
    vert_group_check = False
    vert_color_check = False
    for c in cls:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('rcb_weight2color.switch_mode_weight', 'F', 'PRESS', alt=True)
        custom_keymaps.append((km, kmi))


def unregister():
    global vert_group_check
    global vert_color_check
    vert_group_check = False
    vert_color_check = False
    for c in reversed(cls):
        bpy.utils.unregister_class(c)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in custom_keymaps:
            km.keymap_items.remove(kmi)
    custom_keymaps.clear()
    bpy.types.VIEW3D_MT_object.remove(menu_func)
