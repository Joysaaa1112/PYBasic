from datetime import timedelta
from io import BytesIO

from flask import make_response, request

from common.service.api.auth_service import make_register, get_user_info
from common.utils.captcha import generate_captcha, verify_captcha
from common.utils.jwt_token import generate_token
from common.utils.output import error, success
from common.validators.auth_validate import AuthValidate
from . import api_blueprint


@api_blueprint.route('/auth/captcha', methods=['GET', 'POST'])
def get_captcha():
    """生成与验证验证码接口"""
    if request.method == 'GET':
        img, code, captcha_id = generate_captcha()

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'image/png'
        response.headers['Cache-Control'] = 'no-store, no-cache'
        response.headers['Captcha-Id'] = captcha_id
        return response


@api_blueprint.route('/auth/register', methods=['POST'])
def register():
    """
    注册接口
    """
    if request.method == 'POST':
        if not request.is_json:
            return error(message='Invalid Content-Type', code=400)

        try:
            validated = AuthValidate(scene='register').validate_or_raise(request.get_json())

            # 验证码验证
            verify_result, verify_message = verify_captcha(user_input=validated['code'],
                                                           captcha_id=validated['captcha_id'])
            if not verify_result:
                return error(message=verify_message)

            # 注册
            result, data = make_register(validated)
            if not result:
                return error(message=data)

            # 生成token
            token = generate_token({'id': data.get('id'), 'email': data.get('email')})

            return success(message='success', data={'token': token})
        except AuthValidate.ErrorClass as e:
            return error(message='validate error', data=e.messages)


@api_blueprint.route('/auth/login', methods=['POST', 'GET'])
def login():
    """
    登录接口
    """
    if request.method == 'POST':
        if not request.is_json:
            return error(message='Invalid Content-Type', code=400)

        try:
            validated = AuthValidate(scene='login').validate_or_raise(request.get_json())
            # 验证码验证
            verify_result, verify_message = verify_captcha(user_input=validated['code'],
                                                           captcha_id=validated['captcha_id'])
            if not verify_result:
                return error(message=verify_message)
            # 获取用户信息
            check_user, result = get_user_info(email=validated['email'])
            if not check_user:
                return error(message=result)
            if validated['password'] != result.password:
                return error(message='email or password is error')
            # 生成token
            if validated['remember']:
                expires_delta = timedelta(days=7)
            else:
                expires_delta = timedelta(days=1)
            token = generate_token({'id': result.id, 'email': result.email}, expires_delta=expires_delta)

            return success(data={'token': token})
        except Exception as e:
            return error(message='validate error', data=e.messages)
    else:
        return error(message='method error')
