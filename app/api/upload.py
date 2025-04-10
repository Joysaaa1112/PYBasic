from flask import request
from . import api_blueprint
from common.utils.output import success, error
from common.service.upload import save_file

@api_blueprint.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            result = save_file(file, subfolder="uploads/2fa6a058-5a41-4379-b389-ebb34ce0a68e/20250410")
            return success(message="File uploaded successfully", data=result)
        else:
            return error(1, "No file uploaded")