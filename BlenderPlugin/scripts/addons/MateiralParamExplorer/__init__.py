import bpy

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

support_node_type = [
    'VALUE',
    'RGB',
    'COMBXYZ',
    'TEX_IMAGE',
    'CLAMP'
]

def 

class NodeInfo:
    node_name = ''
    node_type = ''
    node_obj = None

    def __init__(self, node):
        if node is not None:
            node_obj = None
            node_type = node.type
            node_name = node.name


def collect_param(node_tree):
    global param_list
    param_list = []
    if node_tree is not None and node_tree.type == 'SHADER':
        for node in node_tree.nodes:
            ##TODO:DELETE
            print(node.name + " :: " + node.label + " :: " + node.type)
            ##TODO:DELETE
            print(support_node_type.__contains__(node.type))
            ##TODO:DELETE
            if support_node_type.__contains__(node.type):
                node_info = NodeInfo(node)
                param_list.append(node_info)


class RefreshParam(bpy.types.Operator):
    bl_idname = "param_explorer.refresh_param"
    bl_label = "RefreshParam"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if node_tree is not None and node_tree.type == 'SHADER':
            collect_param(node_tree)
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
        tree = context.space_data.edit_tree
        if node_tree != tree and tree.type == 'SHADER':
            node_tree = tree
        for node in tree.nodes:
            if node.type == 'CLAMP':
                layout.prop(node.inputs[0], 'default_value', slider=True)
        # I1 = tree.nodes['I1']
        # I2 = tree.nodes['I2']
        # layout.template_ID(I1, "image", open='image.open')
        # layout.template_ID(I2, "image", open='image.open')

    @classmethod
    def poll(cls, context):
        return context.space_data.edit_tree is not None and context.space_data.edit_tree.type == 'SHADER'


class_to_register = (
    RefreshParam,
    UI_PT_PivotPainterPanel,
)


def register():
    for c in class_to_register:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(class_to_register):
        bpy.utils.unregister_class(c)
