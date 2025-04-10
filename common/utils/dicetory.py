import os
from pathlib import Path


def root_path(path=None):
    """
    获取根目录
    :param path:
    :return:
    """
    r = os.environ.get("PROJECT_ROOT")

    if path is not None:
        r = str(Path(r) / path)
    return r


def get_files_by_ext(directory, ext, recursive=False):
    """
    使用 pathlib 实现
    :param directory: 目标目录路径（字符串或 Path 对象）
    :param ext: 后缀名（例如 ".txt"）
    :param recursive: 是否递归子目录
    :return: 生成器（节省内存）或列表
    """
    path = Path(directory)
    ext = ext.lower()

    if recursive:
        # 递归搜索所有子目录（通配符 **）
        return path.rglob(f"*{ext}")
    else:
        # 仅当前目录
        return path.glob(f"*{ext}")
