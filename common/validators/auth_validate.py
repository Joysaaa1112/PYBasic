# common/validators/auth_validate.py
from marshmallow import fields, ValidationError

from .base import BaseValidate


class AuthValidateError(Exception):
    def __init__(self, messages):
        self.messages = messages
        super().__init__('Auth 验证失败')


class AuthValidate(BaseValidate):
    ErrorClass = AuthValidateError
    """Auth 相关验证器：支持注册、登录、验证码验证等场景"""
    email = fields.Email()
    password = fields.Str()
    password_confirm = fields.Str()
    code = fields.Str()
    captcha_id = fields.Str()
    remember = fields.Boolean()
    avatar = fields.Str()

    def scene_validate(self, data):
        print(self._scene)
        """按场景校验字段"""
        if self._scene == 'register':
            required_fields = ['email', 'password', 'password_confirm', 'code', 'captcha_id']
        elif self._scene == 'login':
            required_fields = ['email', 'password']
        elif self._scene == 'verify_captcha':
            required_fields = ['code', 'captcha_id']
        else:
            required_fields = []

        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            raise ValidationError({f: 'The field is required.' for f in missing})
        print(self._scene)
        # register 额外校验
        if self._scene == 'register':
            if data.get('password') != data.get('password_confirm'):
                raise ValidationError({'password1': 'The passwords do not match.'})
