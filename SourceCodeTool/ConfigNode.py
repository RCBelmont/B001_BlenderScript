import os.path
from datetime import date
from enum import Enum

###
project_path = "F:\\DevSSD\\Blender\\BlenderDev\\build_windows_Full_x64_vc16_Release\\"
node_c_path = r"source\blender\nodes\shader\nodes"
node_glsl_path = r"source\blender\gpu\shaders\material"
bke_node_path = r"source\blender\blenkernel\BKE_node.h"
nod_static_types_path = r"source\blender\nodes\NOD_static_types.h"
nod_shader_path = r"source\blender\nodes\NOD_shader.h"
node_cc_path = r"source\blender\blenkernel\intern\node.cc"
# deprecated
# gpu_material_lib_path = r"source\blender\gpu\intern\gpu_material_library.c"
gpu_source_list = project_path + r"source\blender\gpu\glsl_gpu_source_list.h"
gpu_cmake_path = r"source\blender\gpu\CMakeLists.txt"
node_cmake_path = r"source\blender\nodes\shader\CMakeLists.txt"
startup_py_path = r"release\scripts\startup\nodeitems_builtins.py"


class NodeType(Enum):
    Input = "Input"
    Output = "Output"
    Shader = "Shader"
    Texture = "Texture"
    Color = "Color"
    Vector = "Vector"
    Converter = "Converter"
    Script = "Script"
    Group = "Group"
    Layout = "Layout"


class PollType(Enum):
    none = ""
    line_style_shader_nodes_poll = "line_style_shader_nodes_poll"
    world_shader_nodes_poll = "world_shader_nodes_poll"
    object_shader_nodes_poll = "object_shader_nodes_poll"
    cycles_shader_nodes_poll = "cycles_shader_nodes_poll"
    eevee_shader_nodes_poll = "eevee_shader_nodes_poll"
    eevee_cycles_shader_nodes_poll = "eevee_cycles_shader_nodes_poll"
    object_cycles_shader_nodes_poll = "object_cycles_shader_nodes_poll"
    object_eevee_shader_nodes_poll = "object_eevee_shader_nodes_poll"
    object_eevee_cycles_shader_nodes_poll = "object_eevee_cycles_shader_nodes_poll"


def contain_find(target_list, find_content):
    r_idx = -1
    for i in range(0, len(target_list)):
        if target_list[i].__contains__(find_content):
            r_idx = i
            break
    return r_idx


def contain_find2(target_list, find_content1, find_content2):
    r_idx = -1
    for i in range(0, len(target_list)):
        if target_list[i].__contains__(find_content1) and target_list[i].__contains__(find_content2):
            r_idx = i
            break
    return r_idx


def find_func_end(target_list, func_name):
    r_idx = -1
    begin_idx = contain_find(target_list, func_name)
    if begin_idx != -1:
        for i in range(begin_idx, len(target_list)):
            if target_list[i].__contains__('}'):
                r_idx = i
                break
    return r_idx


node_type = NodeType.Shader
poll_type = PollType.eevee_shader_nodes_poll
author_name = 'RCB'
# bsdf_two_side
node_kw = "bsdf_new_shading"
# bsdf two side
node_kw1 = node_kw.replace("_", " ")
# Bsdf Two Side
node_kw2 = node_kw1.title()
# BSDF_TWO_SIDE
node_kw3 = node_kw.upper()
# BsdfTwoSide
node_kw4 = node_kw2.replace(" ", "")
# node_bsdf_two_side
shader_func_name = 'node_' + node_kw
# register_node_type_sh_bsdf_two_side
node_register_func_name = 'register_node_type_sh_' + node_kw
# node_shader_bsdf_two_side_cc
name_space = "node_shader_" + node_kw + "_cc"
# gpu_shader_material__bsdf_two_side
shader_file_name = 'gpu_shader_material_' + node_kw


def add_node_macro():
    f = open(bke_node_path, 'r')
    contents = f.readlines()
    begin_line = contain_find(contents, '#define SH_NODE_VECTOR_ROTATE 708')
    end_line = begin_line
    f.close()
    if begin_line == -1:
        raise RuntimeError("add_node_macro error")
    for i in range(begin_line, len(contents)):
        if not (contents[i].__contains__("#define")):
            end_line = i
            break

    last_define = contents[end_line - 1]
    num = last_define.split(' ')[2]
    now_num = int(num) + 1
    contents.insert(end_line, "#define SH_NODE_" + node_kw3 + " " + str(now_num) + "\n")
    f = open(bke_node_path, 'w')
    f.writelines(contents)
    f.close()


def add_node_c():
    today = date.today()
    f = open(node_c_path + "/node_shader_" + node_kw + ".cc", 'a')
    # Write Comment
    f.write('//=====================================\n')
    f.write('//' + node_kw2 + '\n')
    f.write('//Created By ' + author_name + '\n')
    f.write('//' + " " + str(today) + '\n')
    f.write('//=====================================\n')
    # Add 'Include'
    f.write("#include \"node_shader_util.hh\"\n")
    # Begin NameSpace
    f.write('namespace blender::nodes::' + name_space + '\n')
    f.write('{\n')
    # Begin Declare Function
    f.write('\tstatic void node_declare(NodeDeclarationBuilder& b)\n')
    f.write('\t{\n')
    f.write('\t\tb.add_input<decl::Color>(N_(\"Color\"))\n')
    f.write('\t\t .default_value({0.8f, 0.8f, 0.8f, 1.0f});\n')
    f.write('\t\tb.add_input<decl::Float>(N_("Weight")).unavailable();\n')
    f.write('\t\t b.add_output<decl::Shader>(N_("BSDF"));\n')
    f.write('\t}\n')
    # End Declare Function
    # Begin Gpu Function
    f.write(
        '\tstatic int node_shader_' + node_kw + '(GPUMaterial* mat, bNode* node, bNodeExecData*UNUSED(execdata), GPUNodeStack* in, GPUNodeStack* out)\n')
    f.write('\t{\n')
    f.write('\t\tGPU_material_flag_set(mat, GPU_MATFLAG_DIFFUSE|GPU_MATFLAG_GLOSSY);\n')
    f.write('\t\treturn GPU_stack_link(mat, node, \"' + shader_func_name + '\", in, out);\n')
    f.write('\t}\n')
    # End Gpu Function
    f.write('}\n')
    # End NameSpace
    f.write('/* node type definition */\n')
    f.write('void ' + node_register_func_name + '()\n')
    f.write('{\n')
    f.write('\tnamespace file_ns = blender::nodes::' + name_space + ';\n')
    f.write('\tstatic bNodeType ntype;\n')
    f.write(
        '\tsh_node_type_base(&ntype, SH_NODE_' + node_kw3 + ', ' + '\"' + node_kw2 + '\"' + ', ' + 'NODE_CLASS_SHADER);\n')
    f.write('\tntype.declare = file_ns::node_declare;\n')
    f.write('\tnode_type_size_preset(&ntype, NODE_SIZE_LARGE);\n')
    f.write('\tnode_type_init(&ntype, NULL);\n')
    f.write('\tnode_type_storage(&ntype, "", NULL, NULL);\n')
    f.write('\tnode_type_gpu(&ntype, file_ns::node_shader_' + node_kw + ');\n')
    f.write('\tnodeRegisterType(&ntype);\n')
    f.write('}\n')
    f.close()


def shader_file():
    f = open(node_glsl_path + '/' + shader_file_name + ".glsl", 'a')
    f.write("\n")
    f.write('void ' + shader_func_name + "(vec4 TestColor, float weight, out Closure result)\n")
    f.write("{\n")
    f.write("\tresult.radiance = vec3(TestColor.r, TestColor.g, TestColor.b);\n")
    f.write("\tresult.radiance *= weight;\n")
    f.write("}\n")
    f.write("\n")
    f.close()


def add_node_def():
    f = open(nod_static_types_path, 'r')
    contents = f.readlines()
    f.close()
    begin_line = contain_find(contents, "SH_NODE_CURVE_FLOAT")
    if begin_line == -1:
        raise RuntimeError("add_node_def error")
    begin_line += 1
    insert_content = "DefNode(ShaderNode, " + "SH_NODE_" + node_kw.upper() + "," + " 0, " + "\"" + node_kw3 + "\", " + node_kw4 + ", \"" + node_kw2 + "\"" + ", \"\")\n"
    contents.insert(begin_line, insert_content)
    f = open(nod_static_types_path, 'w')
    f.writelines(contents)
    f.close()


def add_register_declear():
    f = open(nod_shader_path, 'r')
    contents = f.readlines()
    f.close()
    begin_line = contain_find(contents, "register_node_type_sh_tex_white_noise")
    if begin_line == -1:
        raise RuntimeError("add_register_declear error")
    begin_line += 1
    insert_content = 'void ' + node_register_func_name + '(void);\n'
    contents.insert(begin_line, insert_content)
    f = open(nod_shader_path, 'w')
    f.writelines(contents)
    f.close()


def add_register_call():
    f = open(node_cc_path, 'r')
    contents = f.readlines()
    f.close()
    begin_line = contain_find(contents, "registerShaderNodes")
    if begin_line == -1:
        raise RuntimeError("add_register_call error")
    target_line = find_func_end(contents, "registerShaderNodes")
    if target_line == -1:
        raise RuntimeError("add_register_call error")
    insert_content = '\t' + node_register_func_name + '();\n'
    contents.insert(target_line, insert_content)
    f = open(node_cc_path, 'w')
    f.writelines(contents)
    f.close()


# deprecated
# def config_mat_lib():
#     f = open(gpu_material_lib_path, 'r')
#     contents = f.readlines()
#     f.close()
#     line1 = contain_find(contents, "datatoc_gpu_shader_material_world_normals_glsl")
#
#     if line1 == -1:
#         raise RuntimeError("config_mat_lib error")
#     insert_str1 = "extern char datatoc_gpu_shader_material_" + node_kw + "_glsl[];\n"
#     contents.insert(line1 + 1, insert_str1)
#
#     line2 = find_func_end(contents, "gpu_material_libraries[]")
#     if line2 == -1:
#         raise RuntimeError("config_mat_lib error")
#     insert_str2 = "\t\t&gpu_shader_material_" + node_kw + "_library,\n"
#     contents.insert(line2, insert_str2)
#
#     line3 = contain_find(contents, "GPUMaterialLibrary *gpu_material_libraries[]")
#     if line3 == -1:
#         raise RuntimeError("config_mat_lib error")
#     insert_str3 = "static GPUMaterialLibrary gpu_shader_material_" + node_kw + "_library = {\n" + \
#                   "\t.code = datatoc_gpu_shader_material_" + node_kw + "_glsl,\n" + "\t.dependencies = {NULL},\n" + "};\n"
#     contents.insert(line3 - 1, insert_str3)
#     f = open(gpu_material_lib_path, 'w')
#     f.writelines(contents)
#     f.close()
#


def add_gpu_source_list():
    f = open(gpu_source_list, 'r')
    contents = f.readlines()
    f.close()
    insert_str = '\nSHADER_SOURCE(datatoc_' + shader_file_name + '_glsl, ' + '\"' + shader_file_name + '.glsl\", ' + '\"shaders/material/' + shader_func_name + '.glsl\")'
    f = open(gpu_source_list, 'w')
    contents.append(insert_str)
    f.writelines(contents)
    f.close()


def config_gpu_cmake_file():
    f = open(gpu_cmake_path, 'r')
    contents = f.readlines()
    f.close()
    line = contain_find(contents, "shaders/material/gpu_shader_material_world_normals.glsl")
    if line == -1:
        raise RuntimeError("config_cmake_file error")
    insert_str = "  shaders/material/" + shader_file_name + ".glsl\n"
    contents.insert(line + 1, insert_str)
    f = open(gpu_cmake_path, 'w')
    f.writelines(contents)
    f.close()


def config_node_cmake_file():
    f = open(node_cmake_path, 'r')
    contents = f.readlines()
    f.close()
    line = contain_find(contents, "nodes/node_shader_wireframe.cc")
    if line == -1:
        raise RuntimeError("config_node_cmake_file error")
    insert_str = "  nodes/" + "node_shader_" + node_kw + ".cc\n"
    contents.insert(line + 1, insert_str)
    f = open(node_cmake_path, 'w')
    f.writelines(contents)
    f.close()


def config_startup_script():
    f = open(startup_py_path, 'r')
    contents = f.readlines()
    f.close()
    line = contain_find2(contents, "ShaderNodeCategory(", "\"" + str(node_type.value) + "\", items=")
    if line == -1:
        raise RuntimeError("config_startup_script error")
    if poll_type == PollType.none:
        insert_str = "\t\tNodeItem(\"ShaderNode" + node_kw4 + "\"),\n"
    else:
        insert_str = "\t\tNodeItem(\"ShaderNode" + node_kw4 + "\", poll=" + str(poll_type.value) + "),\n"
    contents.insert(line + 1, insert_str)
    f = open(startup_py_path, 'w')
    f.writelines(contents)
    f.close()


if __name__ == '__main__':
    # print(node_kw)
    # print(node_kw1)
    # print(node_kw2)
    # print(node_kw3)
    # print(node_kw4)
    add_node_macro()
    add_node_c()
    shader_file()
    add_node_def()
    add_register_declear()
    add_register_call()
    config_gpu_cmake_file()
    config_node_cmake_file()
    add_gpu_source_list()
    config_startup_script()
    print("Shader: " + node_kw + " Add Done!!")
