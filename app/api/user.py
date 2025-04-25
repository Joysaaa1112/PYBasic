import os

from flask import request, current_app, g

from common.models.User import User
from common.utils.output import success, error
from . import api_blueprint


@api_blueprint.route('/user/info', methods=['GET'])
def user_info():
    if request.method == 'GET':
        user_id = g.uid
        if not user_id:
            return error(message='token is invalid')

        user = User.query.filter_by(id=user_id).first()

        return success(data=user.to_dict())


@api_blueprint.route('/user/avatar', methods=['GET'])
def user_avatar():
    if request.method == 'GET':
        avatar_folder = os.path.join(current_app.static_folder, 'avatar')
        try:
            files = os.listdir(avatar_folder)
            # 过滤掉隐藏文件或非图片
            images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

            # 构建前端可用的访问路径
            avatar_urls = [f'/static/avatar/{img}' for img in images]
            return success(data=avatar_urls)

        except FileNotFoundError:
            return error(message='Avatar folder not found')

        except Exception as e:
            return error(message=f'Unexpected error: {str(e)}')
