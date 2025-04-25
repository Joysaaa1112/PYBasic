import os
import requests

def download_file(url, save_path):
    """
    下载文件并保存到指定路径
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True, save_path
    else:
        # 返回错误消息
        return False, f"下载文件失败，状态码: {response.status_code}"

def split_file_path(file_path):
    """
    分解文件路径，返回路径、文件名和后缀

    Args:
        file_path (str): 完整的文件路径（相对或绝对）

    Returns:
        tuple: (dir_path, filename, extension)
            - dir_path: 文件所在目录（以 / 结尾）
            - filename: 文件名（不带后缀）
            - extension: 文件后缀（带点，如 ".txt"）
    """
    # 获取目录路径（确保以 / 结尾）
    dir_path = os.path.dirname(file_path)
    if dir_path and not dir_path.endswith(os.sep):  # 处理不同操作系统的路径分隔符
        dir_path += os.sep

    # 获取文件名和后缀
    full_filename = os.path.basename(file_path)
    filename, extension = os.path.splitext(full_filename)

    return dir_path.replace('\\', '/'), filename, extension.lower()

if __name__ == '__main__':
    print(split_file_path('a948fffe-8ebe-423a-9e7c-bfa92bdadd47/20250410/11791b9bdbc821dec268558f39f3cefc.STEP'))