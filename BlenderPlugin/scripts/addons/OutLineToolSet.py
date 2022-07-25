import nt

import bpy

bl_info = {
    "name": "OutLineTool",
    "description": "OutLineTool",
    "author": "RCB",
    "version": (0, 0, 1),
    "blender": (3, 2, 0),
    "location": "View 3D > Sidebar > RCBTool > OutLineTool (panel)",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

vert_group_check = False
vert_color_check = False
modifier_name = 'MyOutline'
vert_group_name = 'OutlineGroup'
material_name = 'OutlineMaterial'
vert_color_name = 'Col'
def_material_name = 'default_mat'


def prepare_vertex_group(obj: 'bpy.types.Object'):
    groups = obj.vertex_groups
    if vert_group_name not in groups.keys():
        group = obj.vertex_groups.new(name=vert_group_name)
        mesh_data = bpy.types.Mesh(obj.data)
        group.add([v.index for v in mesh_data.vertices], 1, 'ADD')


def init_modifier(obj: 'bpy.types.Object'):
    mods = obj.modifiers
    if modifier_name in mods:
        mod = mods.get(modifier_name)
    else:
        mod = obj.modifiers.new(modifier_name, "SOLIDIFY")
    mod = bpy.types.SolidifyModifier(mod)
    mod.offset = 1
    mod.thickness = 0.05
    mod.use_flip_normals = True
    mod.vertex_group = vert_group_name
    mod.material_offset = 100
    mod.use_rim = False


def create_default_mat():
    mat = bpy.data.materials.new(def_material_name)
    mat.use_nodes = True
    return mat


def create_material():
    mat = bpy.data.materials.new(material_name)
    mat.use_nodes = True
    mat.shadow_method = 'NONE'
    mat.blend_method = 'BLEND'
    node_tree = mat.node_tree
    for n in node_tree.nodes:
        node_tree.nodes.remove(n)
    nodes = node_tree.nodes
    n_output = nodes.new("ShaderNodeOutputMaterial")
    n_mix = nodes.new("ShaderNodeMixShader")
    n_rgb = nodes.new("ShaderNodeRGB")
    n_rgb.outputs[0].default_value = (0, 0, 0, 1)
    n_geo = nodes.new("ShaderNodeNewGeometry")
    n_sub = nodes.new("ShaderNodeMath")
    n_sub.operation = 'SUBTRACT'
    n_multi = nodes.new('ShaderNodeMath')
    n_multi.operation = 'MULTIPLY'
    n_speRGB = nodes.new("ShaderNodeSeparateRGB")
    n_trans = nodes.new("ShaderNodeBsdfTransparent")
    n_vertColor = nodes.new("ShaderNodeVertexColor")
    n_vertColor.layer_name = vert_color_name

    n_mix.location = (-200, 0)
    n_trans.location = (-600, -50)
    n_rgb.location = (-600, -250)
    n_multi.location = (-400, 250)
    n_sub.location = (-600, 450)
    n_geo.location = (-800, 450)
    n_speRGB.location = (-600, 150)
    n_vertColor.location = (-800, 150)

    n_sub.inputs[0].default_value = 1
    node_tree.links.new(n_geo.outputs[6], n_sub.inputs[1])
    node_tree.links.new(n_sub.outputs[0], n_multi.inputs[0])
    node_tree.links.new(n_vertColor.outputs[0], n_speRGB.inputs[0])
    node_tree.links.new(n_speRGB.outputs[1], n_multi.inputs[1])
    node_tree.links.new(n_multi.outputs[0], n_mix.inputs[0])
    node_tree.links.new(n_trans.outputs[0], n_mix.inputs[1])
    node_tree.links.new(n_rgb.outputs[0], n_mix.inputs[2])
    node_tree.links.new(n_mix.outputs[0], n_output.inputs[0])
    return mat


def init_material(obj: 'bpy.types.Object'):
    if def_material_name not in bpy.data.materials:
        def_mat = create_default_mat()
    else:
        def_mat = bpy.data.materials.get(def_material_name)

    if material_name not in bpy.data.materials:
        mat = create_material()
    else:
        mat = bpy.data.materials.get(material_name)
    mesh = bpy.types.Mesh(obj.data)
    if len(mesh.materials) <= 0:
        mesh.materials.append(def_mat)

    if material_name in mesh.materials:
        idx = mesh.materials.find(material_name)
        obj.active_material_index = idx
        for i in range(idx, len(mesh.materials)):
            bpy.ops.object.material_slot_move(direction="DOWN")
    else:
        mesh.materials.append(mat)


def init_vert_color(obj: 'bpy.types.Object'):
    mesh = bpy.types.Mesh(obj.data)
    if vert_color_name not in mesh.color_attributes:
        attr = mesh.color_attributes.new(vert_color_name, domain='CORNER', type='BYTE_COLOR')
    else:
        attr = mesh.color_attributes.get(vert_color_name)
    mesh.color_attributes.active_color = attr
    mesh.attributes.active = attr


def get_key_string(category, operator):
    kc = bpy.context.window_manager.keyconfigs
    if kc.addon.keymaps[category].keymap_items.find(operator) != -1:
        km = kc.addon.keymaps[category].keymap_items[operator]
        return '(' + km.to_string() + ')'
    return ""


class OPT_RemoveVertFromGroup(bpy.types.Operator):
    bl_idname = "rcb_weight2color.remove_vert_from_group"
    bl_label = "RemoveFormGroup"
    bl_options = {'REGISTER'}

    def execute(self, context):
        act_obj = context.active_object
        mesh_data = bpy.types.Mesh(act_obj.data)
        vert_group = act_obj.vertex_groups.active
        for v in mesh_data.vertices:
            if v.select:
                vert_group.add(v.index, 0.5, 'SUBTRACT')

    @classmethod
    def poll(cls, context):
        if bpy.context.mode is not 'EDIT_MESH':
            return False
        act_obj = bpy.types.Object(context.active_object)
        mesh_data = bpy.types.Mesh(act_obj.data)
        vert_group = act_obj.vertex_groups.active
        return vert_group is not None


class OPT_AddVertToGroup(bpy.types.Operator):
    bl_idname = "rcb_weight2color.add_vert_to_group"
    bl_label = "AddToGroup"
    bl_options = {'REGISTER'}

    def execute(self, context):
        act_obj = context.active_object
        mesh_data = bpy.types.Mesh(act_obj.data)
        vert_group = act_obj.vertex_groups.active
        verL = [v.index for v in mesh_data.vertices if v.select]
        vert_group.add(verL, 0.5, 'ADD')

    @classmethod
    def poll(cls, context):
        if bpy.context.mode != 'EDIT_MESH':
            return False
        act_obj = bpy.types.Object(context.active_object)
        vert_group = act_obj.vertex_groups.active
        return vert_group is not None


class OPT_AddOutLine(bpy.types.Operator):
    bl_idname = "rcb_weight2color.add_outline"
    bl_label = "AddModifier"
    bl_options = {'REGISTER'}
    global modifier_name

    def execute(self, context):
        if context.active_object and type(context.active_object.data) == bpy.types.Mesh:
            act_obj = bpy.types.Object(context.active_object)
            # Deal Modifier
            init_vert_color(act_obj)
            prepare_vertex_group(act_obj)
            init_modifier(act_obj)
            init_material(act_obj)
        return {'FINISHED'}


class OPT_SwitchModeWeight(bpy.types.Operator):
    bl_idname = "rcb_weight2color.switch_mode_weight"
    bl_label = "SwitchWeightModeTool"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if context.mode == 'PAINT_WEIGHT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.space_data.shading.type = 'MATERIAL'
        else:
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
            bpy.context.space_data.shading.type = 'SOLID'
            bpy.context.object.data.use_paint_mask_vertex = True
        return {"FINISHED"}


class OPT_ConvertColorAttr(bpy.types.Operator):
    bl_idname = "rcb_weight2color.convert_attr"
    bl_label = "ConvertAttr"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.geometry.attribute_convert(domain='CORNER', data_type='BYTE_COLOR')
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
        attr = mesh_data.color_attributes.active_color

        # Transfer Data
        for loops in mesh_data.loops:
            loop_idx = loops.index
            vert_idx = loops.vertex_index
            try:
                weight = vert_group.weight(vert_idx)
                in_group = 1
            except RuntimeError:
                weight = 0
                in_group = 0
            attr = bpy.types.ByteColorAttribute(attr)
            attr.data[loop_idx].color = (weight, in_group, 0, 0)
        self.report({'INFO'}, 'Transfer Done!!')

        # for vert in mesh_data.vertices:
        #     idx = vert.index
        #     try:
        #         weight = vert_group.weight(idx)
        #     except RuntimeError:
        #         weight = 0.0
        #     attr.data[idx].color = (weight, 0, 0, 0)
        # self.report({'INFO'}, 'Transfer Done!!')
        # bpy.ops.object.mode_set(mode='VERTEX_PAINT')

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


class VIEW3D_PT_WeightToColorPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'OutlineTools'
    bl_category = 'RCBTool'

    @classmethod
    def poll(cls, context):
        return bpy.context.mode in ["OBJECT", "PAINT_WEIGHT", 'EDIT_MESH']

    def draw(self, context):
        layout = self.layout
        # Button Switch Edit Mode
        layout.operator('rcb_weight2color.switch_mode_weight',
                        text='SwitchMode' + get_key_string('3D View', 'rcb_weight2color.switch_mode_weight'))
        layout.split(factor=25)
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

            valid_mods = [x for x in actObj.modifiers if modifier_name == x.name and x.type == "SOLIDIFY"]

            box = layout.box()
            box.label(text="Operate:")
            # Button Add Modifier
            box.operator('rcb_weight2color.add_outline', text='Init Outline')
            box.split(factor=10)
            if len(valid_mods):
                mod = valid_mods[0]
                box.prop(mod, 'thickness')
            box.split(factor=10)
            box.label(text="VertGroup Operate:")
            row = box.row()
            row.operator('object.vertex_group_assign', text='Assign')
            row.operator('object.vertex_group_remove_from', text='Remove')
            row = box.row()
            row.operator('object.vertex_group_select', text='SelectGroup')
            row.operator('object.vertex_group_deselect', text='DeselectGroup')
            box.split(factor=10)
            box.label(text="Weight Operate:")
            box.operator('object.vertex_group_smooth', text='Smooth')
            box.split(factor=10)
            box.prop(bpy.context.scene.tool_settings.unified_paint_settings, 'weight')
            box.operator('paint.weight_set', text='SetWeight')

            # InfomationText
            box = layout.box()
            box.label(text="INFO:")
            box.label(text="TargetObject:")
            box.label(text="    " + actObj.name)
            # Check VertGroup
            if actObj.vertex_groups.active_index != -1:
                box.label(text="Source VertGroup:")
                box.label(text="    " + actObj.vertex_groups.active.name)
                vert_group_check = True
            else:
                box.alert = True
                box.label(text="Source VertGroup:")
                box.label(text="Need A Active VertexGroup!")
            box.split(factor=15)
            meshData = bpy.types.Mesh(actObj.data)
            # Check VertColorAttribute
            if meshData.color_attributes.active_color_index != -1:
                attr = meshData.color_attributes.active
                box.label(text="Target ColorAttribute:")
                box.label(
                    text="    " + meshData.color_attributes.active.name)
                if attr.data_type != 'BYTE_COLOR' or attr.domain != 'CORNER':
                    box.alert = True
                box.label(text="    domain: " + attr.domain + "  data_type: " + attr.data_type)
                vert_color_check = True
            else:
                box.alert = True
                box.label(text="Target ColorAttribute:")
                box.label(text="    Need A Active ColorAttribute!")
            box.split(factor=15)

            if vert_color_check:
                attr = meshData.color_attributes.active_color
                if attr.data_type != 'BYTE_COLOR' or attr.domain != 'CORNER':
                    box.alert = True
                    box.label(text="This Color Attr Cannot Be Read By Engine")
                    box.operator('rcb_weight2color.convert_attr', text='Click To Convert')
                else:
                    # Draw Opt
                    if vert_color_check and vert_group_check:
                        box.operator('rcb_weight2color.transfer')
        else:
            layout.alert = True
            layout.label(text="Please Select A Mesh Object")


cls = (
    OPT_RemoveVertFromGroup,
    OPT_AddVertToGroup,
    OPT_AddOutLine,
    OPT_ConvertColorAttr,
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
        kmi = km.keymap_items.new('rcb_weight2color.switch_mode_weight', 'ACCENT_GRAVE', 'PRESS', alt=True)
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
