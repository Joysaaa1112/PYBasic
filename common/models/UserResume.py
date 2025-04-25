from sqlalchemy import Integer, String, JSON

from . import db


class UserResume(db.Model):
    __tablename__ = 'rs_user_resume'

    id = db.Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    uid = db.Column(Integer, nullable=False, default=0, comment='用户id')
    uuid = db.Column(String(255), nullable=False, default='', comment='用户标识（未登录使用）')
    code = db.Column(String(255), nullable=False, default='', comment='简历编号')
    template = db.Column(String(255), nullable=False, default='', comment='简历模板')
    configuration = db.Column(JSON, nullable=False, default={}, comment='简历配置')
    is_delete = db.Column(Integer, nullable=False, default=0, comment='是否删除')
    create_time = db.Column(db.DateTime, server_default=db.func.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'uuid': self.uuid,
            'code': self.code,
            'template': self.template,
            'configuration': self.configuration,
            'is_delete': self.is_delete,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
