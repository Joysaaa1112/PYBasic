from . import db
from sqlalchemy import Column, Integer, String, DateTime, func


class MomakingCncModels(db.Model):
    __tablename__ = 'mk_momaking_cnc_models'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    name = Column(String(255), nullable=False, default='', comment='模型名称')
    filename = Column(String(255), nullable=False, default='', comment='文件名')
    path = Column(String(255), nullable=False, default='', comment='模型文件路径')
    type = Column(Integer, nullable=False, default=1, comment='模型类型')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    status = Column(Integer, nullable=False, default=1, comment='状态')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'filename': self.filename,
            'path': self.path,
            'type': self.type,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'status': self.status,
        }
