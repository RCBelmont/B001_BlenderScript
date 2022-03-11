import bpy
import re

bl_info = {
    "name": "MaterialParamExplorer",
    "description": "ZeroPivotPainter",
    "author": "RCB",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "Node > ParamExplorer",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

node_tree = None
param_list = []
param_node_color = (0.087, 0.164, 0.246)
support_node_type = [
    'VALUE',
    'RGB',
    'COMBXYZ',
    'TEX_IMAGE',
    'CLAMP'
]
param_suffix = '_param'


def get_name(elem):
    return elem.node_label




class NodeInfo:
    node_name = ''
    node_type = ''
    node_label = ''
    node_obj = None

    def __init__(self, node):
        if node is not None:
            self.node_obj = node
            self.node_type = node.type
            self.node_name = node.name
            self.node_label = node.label


def collect_param(node_tree):
    global param_list
    param_list = []
    if node_tree is not None and node_tree.type == 'SHADER':
        for node in node_tree.nodes:
            if support_node_type.__contains__(node.type) and node.name.endswith(param_suffix):
                node_info = NodeInfo(node)
                param_list.append(node_info)
        param_list.sort(key=get_name)


class ConvertToParam(bpy.types.Operator):
    bl_idname = "param_explorer.convert_to_param"
    bl_label = "ConvertToParam"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if node_tree is not None and node_tree.type == 'SHADER':
            if node_tree.nodes.active is not None:
                target_node = node_tree.nodes.active
                if support_node_type.__contains__(target_node.type):
                    old_name = target_node.name
                    if old_name.endswith(param_suffix):
                        new_name = old_name.removesuffix(param_suffix)
                        target_node.name = new_name
                        target_node.use_custom_color = False
                    else:
                        new_name = old_name + param_suffix
                        target_node.name = new_name
                        target_node.use_custom_color = True
                        target_node.color = param_node_color
            collect_param(node_tree)
        return {'FINISHED'}


class RefreshParam(bpy.types.Operator):
    bl_idname = "param_explorer.refresh_param"
    bl_label = "RefreshParam"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if node_tree is not None and node_tree.type == 'SHADER':
            collect_param(node_tree)
            if node_tree is not None and node_tree.type == 'SHADER':
                for node in node_tree.nodes:
                    if support_node_type.__contains__(node.type) and node.name.endswith(param_suffix):
                        node.use_custom_color = True
                        node.color = param_node_color
        return {'FINISHED'}


class UI_PT_PivotPainterPanel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "ParamExplorer"
    bl_category = 'ParamExplorer'

    def draw(self, context):
        global node_tree
        layout = self.layout
        layout.split(factor=5.0)
        layout.label(text="材质参数")
        layout.operator('param_explorer.refresh_param')
        layout.separator()
        layout.operator('param_explorer.convert_to_param')
        layout.split(factor=15.0)
        tree = context.space_data.edit_tree
        if node_tree != tree and tree.type == 'SHADER':
            node_tree = tree
            if node_tree is not None and node_tree.type == 'SHADER':
                collect_param(node_tree)

        # for node in tree.nodes:
        #     if node.type == 'CLAMP':
        #         layout.prop(node.inputs[0], 'default_value', slider=True)
        #     elif node.type == 'VALUE':
        #         layout.prop(node.outputs[0], 'default_value')
        #     elif node.type == 'TEX_IMAGE':
        #         layout.template_ID(node, "image", open='image.open')
        # I1 = tree.nodes['I1']
        # I2 = tree.nodes['I2']
        # layout.template_ID(I1, "image", open='image.open')
        # layout.template_ID(I2, "image", open='image.open')
        box = layout.box()
        box.label(text="Parameters:")
        for node_info in param_list:
            if node_info is not None and node_info.node_obj is not None:
                box1 = box.box()
                type = node_info.node_type
                row = box1.column()
                if len(node_info.node_obj.label) == 0:
                    row.label(text="UnNamedParam" + ':')
                else:
                    row.label(text=node_info.node_obj.label + ':')
                ## VALUE
                if type == support_node_type[0]:
                    row.prop(node_info.node_obj.outputs[0], 'default_value', text='',
                             slider=False)
                ## RGB
                if type == support_node_type[1]:
                    row.prop(node_info.node_obj.outputs[0], 'default_value', text='',
                             slider=False)
                ## XYZ
                elif type == support_node_type[2]:
                    row.prop(node_info.node_obj.inputs[0], 'default_value', text='',
                             slider=True)
                    row.prop(node_info.node_obj.inputs[1], 'default_value', text='',
                             slider=True)
                    row.prop(node_info.node_obj.inputs[2], 'default_value', text='',
                             slider=True)
                ## IMAGE
                elif type == support_node_type[3]:
                    row.template_ID(node_info.node_obj, "image", open='image.open')
                ## CLAMP
                elif type == support_node_type[4]:
                    row.prop(node_info.node_obj.inputs[0], 'default_value', text='',
                             slider=True)
                row.split(factor=10.0)

    @classmethod
    def poll(cls, context):
        return context.space_data.edit_tree is not None and context.space_data.edit_tree.type == 'SHADER'


class_to_register = (
    RefreshParam,
    ConvertToParam,
    UI_PT_PivotPainterPanel,
)


def register():
    for c in class_to_register:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(class_to_register):
        bpy.utils.unregister_class(c)
