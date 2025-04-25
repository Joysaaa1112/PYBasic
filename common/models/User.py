from sqlalchemy import Column, Integer, String, DateTime, func

from . import db


class User(db.Model):
    __tablename__ = 'rs_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255), nullable=False, default='', unique=True, comment='用户标识（未登录使用，登陆后储存到用户）')
    email = Column(String(255), nullable=False, default='', unique=True, comment='邮箱')
    phone = Column(String(255), nullable=False, default='', unique=True, comment='手机号')
    password = Column(String(255), nullable=False, default='', comment='密码')
    password_hash = Column(String(255), nullable=False, default='', comment='密文密码')
    nickname = Column(String(255), nullable=False, default='', comment='昵称')
    avatar = Column(String(255), nullable=False, default='', comment='头像')
    role = Column(Integer, nullable=False, default=0, comment='角色ID')
    gender = Column(Integer, nullable=False, default=0, comment='性别')
    status = Column(Integer, nullable=False, default=0, comment='状态')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'email': self.email,
            'phone': self.phone,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'gender': self.gender,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
