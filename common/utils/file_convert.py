# -*- coding: utf-8 -*-
import os
import trimesh
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh


def read_step(filename):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        return step_reader.Shape(1)
    else:
        raise ValueError('Cannot read the file')


def write_stl(shape, filename, definition=0.1):
    directory = os.path.split(__name__)[0]
    stl_output_dir = os.path.abspath(directory)
    assert os.path.isdir(stl_output_dir)

    stl_file = os.path.join(stl_output_dir, filename)

    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False)

    mesh = BRepMesh_IncrementalMesh(shape, definition)
    mesh.Perform()
    assert mesh.IsDone()

    stl_writer.Write(shape, stl_file)
    assert os.path.isfile(stl_file)
    return stl_file


def stl_to_gltf(input_stl, definition=0.1):
    # 获取输入文件的目录和文件名（去除后缀）
    directory = os.path.dirname(input_stl)
    base_filename = os.path.splitext(os.path.basename(input_stl))[0]

    # 构建输出 GLTF 文件的路径
    output_filename = os.path.join(directory, base_filename + '.glb')

    try:
        # 加载 STL 文件
        mesh_trimesh = trimesh.load(input_stl)
        if mesh_trimesh.is_empty:
            raise ValueError("加载的 STL 文件为空或格式不正确")
        # 导出为 GLTF 格式
        mesh_trimesh.export(output_filename, file_type='glb')
        glb_file_path = os.path.abspath(output_filename)

        return glb_file_path

    except Exception as e:
        raise ValueError(f"Error converting STL to GLTF: {str(e)}")


def stp_to_gltf(filename, definition=0.1):
    # 读取 STEP 文件并获取形状
    shape = read_step(filename)

    # 为形状生成网格
    mesh = BRepMesh_IncrementalMesh(shape, definition)
    mesh.Perform()
    assert mesh.IsDone()

    # 获取输入文件的目录和文件名（去除后缀）
    directory = os.path.dirname(filename)
    base_filename = os.path.splitext(os.path.basename(filename))[0]

    # 暂时保存为 STL 文件，稍后通过 trimesh 读取
    temp_stl = 'temp_output.stl'
    write_stl(shape, temp_stl, definition)

    # 构建输出 GLTF 文件的路径
    output_filename = os.path.join(directory, base_filename + '.glb')

    try:
        # 将 STL 加载到 Trimesh 对象中
        mesh_trimesh = trimesh.load(temp_stl)

        # 检查是否为空或包含多个实体
        if mesh_trimesh.is_empty:
            raise ValueError("加载的文件为空或格式不正确")

        # 如果是组合模型，可以分解并处理每个部分
        if isinstance(mesh_trimesh, trimesh.Scene):
            # 如果是场景对象（包含多个部分），可以进行适当处理
            mesh_trimesh.export(output_filename, file_type='glb')
        else:
            # 单一网格的处理方式
            mesh_trimesh.export(output_filename, file_type='glb')

        glb_file_path = os.path.abspath(output_filename)

        # 删除临时 STL 文件
        os.remove(temp_stl)

        return glb_file_path

    except Exception as e:
        # 如果发生错误，删除临时 STL 文件
        if os.path.exists(temp_stl):
            os.remove(temp_stl)
        raise e


if __name__ == '__main__':
    stp_to_gltf('../../assets/ceshi001.STEP')
