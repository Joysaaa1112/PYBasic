from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func, JSON


class MomakingConvertToGlb(db.Model):
    __tablename__ = 'mk_momaking_convert_to_glb'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    code = Column(String(255), nullable=False, default='', comment='文件哈希')
    file_name = Column(String(255), nullable=False, default='', comment='文件名')
    origin_path = Column(String(255), nullable=False, default='', comment='源文件路径')
    origin_ext = Column(String(64), nullable=False, default='', comment='源文件后缀')
    glb_path = Column(String(255), nullable=False, default='', comment='转换的glb文件路径')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态 0未生成 1已生成')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'code': self.code,
            'file_name': self.file_name,
            'origin_path': self.origin_path,
            'origin_ext': self.origin_ext,
            'glb_path': self.glb_path,
            'create_time': create_time_str,
            'update_time': update_time_str,
            'status': self.status,
        }
