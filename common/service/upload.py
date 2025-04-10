import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# 加载环境变量
load_dotenv()

# 配置参数（修正版）
BASE_FOLDER = os.getenv("BASE_FOLDER", "storge").strip('/')  # 基础存储目录
UPLOAD_SUBFOLDER = os.getenv("UPLOAD_SUBFOLDER", "").strip('/')  # 子目录（可选）
ALLOWED_EXTENSIONS = set(
    ext.strip().lower() for ext in
    os.getenv("ALLOWED_EXTENSIONS", "stp,step,stl,obj,jpeg,jpg,png,gif").split(',')
    if ext.strip()
)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 20971520))  # 默认20MB

def get_full_upload_path(subfolder=""):
    """获取完整的上传路径"""
    subfolder = subfolder.strip('/') if subfolder else ""
    if subfolder:
        return os.path.join(BASE_FOLDER, subfolder)
    return BASE_FOLDER

def validate_upload(file, subfolder="", extensions=None, max_size=None):
    """
    验证上传文件的合法性
    :param file: 文件对象
    :param subfolder: 相对于BASE_FOLDER的子目录
    :param extensions: 允许的扩展名集合
    :param max_size: 最大文件大小
    :return: (bool, result_dict)
    """
    # 参数处理
    extensions = extensions or ALLOWED_EXTENSIONS
    max_size = max_size or MAX_FILE_SIZE
    full_upload_path = get_full_upload_path(subfolder)

    # 基本验证
    if not file or file.filename == '':
        return False, {"code": 4001, "message": "No file uploaded"}

    # 文件名处理
    filename = secure_filename(file.filename)
    if '.' not in filename:
        return False, {"code": 4002, "message": "File has no extension"}

    # 扩展名验证
    file_ext = filename.rsplit('.', 1)[1].lower()
    if file_ext not in extensions:
        return False, {
            "code": 4003,
            "message": f"Invalid file type. Allowed: {', '.join(sorted(extensions))}",
            "allowed_extensions": sorted(extensions)
        }

    # 文件大小验证
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > max_size:
        return False, {
            "code": 4004,
            "message": f"File too large (max {max_size//1024//1024}MB)",
            "max_size": max_size,
            "file_size": file_size
        }

    # 路径安全验证
    save_path = os.path.join(full_upload_path, filename)
    try:
        if not os.path.abspath(save_path).startswith(os.path.abspath(BASE_FOLDER)):
            return False, {"code": 4005, "message": "Invalid save path"}
    except Exception:
        return False, {"code": 4006, "message": "Path validation failed"}

    return True, {
        "code": 0,
        "message": "Validation passed",
        "filename": filename,
        "file_ext": file_ext,
        "file_size": file_size,
        "save_path": save_path.replace('\\', '/')
    }

def save_file(file, subfolder="", custom_name=None, allowed_extensions=None, max_size=None):
    """
    安全保存文件（最终修正版）
    :param file: 文件对象
    :param subfolder: 存储子目录（相对于BASE_FOLDER）
    :param custom_name: 自定义文件名（不带扩展名）
    :return: (success, result_dict)
    """
    # 验证文件
    is_valid, validation = validate_upload(
        file,
        subfolder=subfolder,
        extensions=allowed_extensions,
        max_size=max_size
    )
    if not is_valid:
        return False, validation

    # 准备存储路径
    full_upload_path = get_full_upload_path(subfolder)
    os.makedirs(full_upload_path, exist_ok=True)

    # 生成文件名
    file_ext = validation['file_ext']
    if custom_name:
        filename = f"{secure_filename(custom_name)}.{file_ext}"
    else:
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{file_ext}"

    save_path = os.path.join(full_upload_path, filename).replace('\\', '/')

    # 保存文件
    try:
        file.save(save_path)
        return True, {
            "code": 0,
            "message": "File saved successfully",
            "original_name": validation['filename'],
            "saved_name": filename,
            "file_path": save_path,
            "file_url": os.path.relpath(save_path, BASE_FOLDER).replace('\\', '/'),
            "file_size": validation['file_size'],
            "is_custom_name": custom_name is not None
        }
    except Exception as e:
        return False, {
            "code": 5001,
            "message": "File save failed",
            "error": str(e),
            "attempted_path": save_path
        }