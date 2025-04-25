# common/validators/base.py
from marshmallow import Schema, validates_schema


class BaseValidateError(Exception):
    def __init__(self, messages):
        self.messages = messages
        super().__init__('验证失败')


class BaseValidate(Schema):
    ErrorClass = BaseValidateError  # 默认异常类型，可被子类覆盖

    def __init__(self, scene=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scene = scene

    def validate_or_raise(self, data):
        errors = self.validate(data)
        if errors:
            raise self.ErrorClass(errors)
        return data

    @validates_schema
    def _validate_scene(self, data, **kwargs):
        if hasattr(self, 'scene_validate'):
            print(self._scene)
            self.scene_validate(data)
        else:
            print('未定义场景验证方法')
