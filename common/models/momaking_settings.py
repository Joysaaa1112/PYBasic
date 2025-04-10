from . import db
from sqlalchemy import Column, Integer, String, DateTime, func, Text


class MomakingSettings(db.Model):
    __tablename__ = 'mk_momaking_settings'


    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    name = Column(String(255), nullable=False, default='', comment='名称')
    value = Column(Text, nullable=False, comment='值')
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'update_time': self.update_time,
        }
