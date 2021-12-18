import os.path
from enum import Enum

node_c_path = r"source\blender\nodes\shader\nodes"
node_glsl_path = r"source\blender\gpu\shaders\material"
bke_node_path = r"source\blender\blenkernel\BKE_node.h"
nod_static_types_path = r"source\blender\nodes\NOD_static_types.h"
nod_shader_path = r"source\blender\nodes\NOD_shader.h"
node_cc_path = r"source\blender\blenkernel\intern\node.cc"
gpu_material_lib_path = r"source\blender\gpu\intern\gpu_material_library.c"
gpu_cmake_path = r"source\blender\gpu\CMakeLists.txt"
node_cmake_path = r"source\blender\nodes\CMakeLists.txt"
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
# bsdf_two_side
node_kw = "bsdf_two_side"
# bsdf two side
node_kw1 = node_kw.replace("_", " ")
# Bsdf Two Side
node_kw2 = node_kw1.title()
# BSDF_TWO_SIDE
node_kw3 = node_kw.upper()
# BsdfTwoSide
node_kw4 = node_kw2.replace(" ", "")


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
    contents.insert(end_line, "#define SH_NODE_" + node_kw.upper() + " " + str(now_num) + "\n")
    f = open(bke_node_path, 'w')
    f.writelines(contents)
    f.close()


def add_node_c():
    f = open(node_c_path + "/node_shader_" + node_kw + ".c", 'a')
    in_func = "sh_node_" + node_kw + "_in"
    out_func = "sh_node_" + node_kw + "_out"
    gpu_func = "node_shader_gpu_" + node_kw
    f.write("#include \"../node_shader_util.h\"\n")
    f.write("static bNodeSocketTemplate " + in_func + "[] = {\n")
    f.write("\t{SOCK_RGBA, N_(\"TestColor\"), 0.5f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, PROP_FACTOR},\n")
    f.write("\t{-1, \"\"},\n")
    f.write("};\n")
    f.write("static bNodeSocketTemplate " + out_func + "[] = {\n")
    f.write("\t{SOCK_SHADER, N_(\"BSDF\")},\n")
    f.write("\t{-1, \"\"},\n")
    f.write("};\n")
    f.write(
        "static int " + gpu_func + "(GPUMaterial* mat,  bNode* node,  bNodeExecData*UNUSED(execdata),  GPUNodeStack* in, GPUNodeStack* out)\n")
    f.write("{\n")
    f.write("\treturn GPU_stack_link(mat,node, \"shader_func_" + node_kw + "\", in, out);\n")
    f.write("};\n")
    ##
    f.write("void register_node_type_sh_" + node_kw + "(void)\n")
    f.write("{\n")
    f.write("\tstatic bNodeType ntype;\n")
    f.write("\tsh_node_type_base(&ntype, SH_NODE_" + node_kw3 + ", \"" + node_kw2 + "\", NODE_CLASS_SHADER, 0);" + "\n")
    f.write(
        "\tnode_type_socket_templates(&ntype, " + in_func + ", " + out_func + ");\n")
    f.write("\tnode_type_size_preset(&ntype, NODE_SIZE_LARGE);\n")
    f.write("\tnode_type_init(&ntype, NULL);\n")
    f.write("\tnode_type_storage(&ntype, \"\", NULL, NULL);\n")
    f.write("\tnode_type_gpu(&ntype, " + gpu_func + ");\n")
    f.write("\tnodeRegisterType(&ntype);\n")
    f.write("}\n")
    f.close()


def shader_file():
    f = open(node_glsl_path + "/gpu_shader_material_" + node_kw + ".glsl", 'a')
    f.write("#ifndef VOLUMETRICS\n")
    f.write("void shader_func_" + node_kw + "(vec4 TestColor, out Closure result)\n")
    f.write("{\n")
    f.write("\tresult.radiance = TestColor;\n")
    f.write("}\n")
    f.write("#endif\n")
    f.close()


def add_node_def():
    f = open(nod_static_types_path, 'r')
    contents = f.readlines()
    f.close()
    begin_line = contain_find(contents, "SH_NODE_OUTPUT_AOV")
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
    insert_content = "void register_node_type_sh_" + node_kw + "(void);\n"
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
    insert_content = "\tregister_node_type_sh_" + node_kw + "();\n"
    contents.insert(target_line, insert_content)
    f = open(node_cc_path, 'w')
    f.writelines(contents)
    f.close()


def config_mat_lib():
    f = open(gpu_material_lib_path, 'r')
    contents = f.readlines()
    f.close()
    line1 = contain_find(contents, "datatoc_gpu_shader_material_world_normals_glsl")

    if line1 == -1:
        raise RuntimeError("config_mat_lib error")
    insert_str1 = "extern char datatoc_gpu_shader_material_" + node_kw + "_glsl[];\n"
    contents.insert(line1 + 1, insert_str1)

    line2 = find_func_end(contents, "gpu_material_libraries[]")
    if line2 == -1:
        raise RuntimeError("config_mat_lib error")
    insert_str2 = "\t\t&gpu_shader_material_" + node_kw + "_library,\n"
    contents.insert(line2, insert_str2)

    line3 = contain_find(contents, "GPUMaterialLibrary *gpu_material_libraries[]")
    if line3 == -1:
        raise RuntimeError("config_mat_lib error")
    insert_str3 = "static GPUMaterialLibrary gpu_shader_material_" + node_kw + "_library = {\n" + \
                  "\t.code = datatoc_gpu_shader_material_" + node_kw + "_glsl,\n" + "\t.dependencies = {NULL},\n" + "};\n"
    contents.insert(line3 - 1, insert_str3)
    f = open(gpu_material_lib_path, 'w')
    f.writelines(contents)
    f.close()


def config_gpu_cmake_file():
    f = open(gpu_cmake_path, 'r')
    contents = f.readlines()
    f.close()
    line = contain_find(contents, "data_to_c_simple(shaders/material/gpu_shader_material_world_normals.glsl SRC)")
    if line == -1:
        raise RuntimeError("config_cmake_file error")
    insert_str = "\ndata_to_c_simple(shaders/material/" + "gpu_shader_material_" + node_kw + ".glsl SRC)\n"
    contents.insert(line + 1, insert_str)
    f = open(gpu_cmake_path, 'w')
    f.writelines(contents)
    f.close()


def config_node_cmake_file():
    f = open(node_cmake_path, 'r')
    contents = f.readlines()
    f.close()
    line = contain_find(contents, "shader/node_shader_util.c")
    if line == -1:
        raise RuntimeError("config_node_cmake_file error")
    insert_str = "\n\tshader/nodes/" + "node_shader_" + node_kw + ".c\n"
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
        insert_str = "\t\tNodeItem(\"ShaderNode" + node_kw4 + "\", poll=" + str(poll_type.value) +"),\n"
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
    config_mat_lib()
    config_gpu_cmake_file()
    config_node_cmake_file()
    config_startup_script()

##print(os.path.abspath(node_c_path))
##add_node_macro()
# f = open(node_cc_path, "r")
# contents = f.readlines()
# f.close()
#
# # TODO:DELETE PRINT
# contents.insert(end_idx, "\ttest_func();\n")
# print(end_idx)
# f = open(node_cc_path, "w")
# f.write("".join(contents))
# f.close()
