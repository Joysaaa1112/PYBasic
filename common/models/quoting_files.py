from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func
from sqlalchemy.dialects.mysql import DECIMAL as Decimal
from datetime import datetime


class QuotingFiles(db.Model):
    __tablename__ = 'mk_quoting_files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, nullable=False, default=0, comment='用户ID')
    uuid = Column(String(255), nullable=False, default='', comment='上传用户')
    file_id = Column(String(255), nullable=False, default='', comment='文件ID')
    quote_id = Column(String(255), nullable=False, default='', comment='计价id')
    name = Column(String(255), nullable=False, default='', comment='文件名')
    path = Column(String(255), nullable=False, default='', comment='文件路径')
    unit = Column(SmallInteger, nullable=False, default=1, comment='1mm 2cm 3in')
    type = Column(SmallInteger, nullable=False, default=1, comment='文件类型 1stl 2obj')
    area = Column(Decimal(10, 2), nullable=False, default=0.00, comment='面积')
    volume = Column(Decimal(10, 2), nullable=False, default=0.00, comment='体积')
    count = Column(Integer, nullable=False, default=0, comment='零件数量')
    width = Column(Decimal(10, 2), nullable=False, default=0.00, comment='宽')
    length = Column(Decimal(10, 2), nullable=False, default=0.00, comment='边')
    height = Column(Decimal(10, 2), nullable=False, comment='高')
    weight = Column(Decimal(10, 2), nullable=False, comment='重量 g')
    image = Column(String(255), nullable=False, default='', comment='预览图')
    is_checked = Column(SmallInteger, nullable=False, default=0, comment='是否选中')
    quotation = Column(Decimal(10, 2), nullable=False, default=0, comment='当前报价')
    quantity = Column(Integer, nullable=False, default=1, comment='数量')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态 1正常')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'uid': self.uid,
            'uuid': self.uuid,
            'file_id': self.file_id,
            'quote_id': self.quote_id,
            'name': self.name,
            'unit': self.unit,
            'type': self.type,
            'area': self.area,
            'volume': self.volume,
            'count': self.count,
            'width': self.width,
            'length': self.length,
            'height': self.height,
            'weight': self.weight,
            'image': self.image,
            'path': self.path,
            'is_checked': self.is_checked,
            'quotation': self.quotation,
            'quantity': self.quantity,
            'create_time': create_time_str,
            'update_time': update_time_str,
            'status': self.status
        }
