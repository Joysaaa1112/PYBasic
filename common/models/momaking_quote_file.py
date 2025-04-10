from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func
from sqlalchemy.dialects.mysql import DECIMAL as Decimal


class MomakingQuoteFile(db.Model):
    __tablename__ = 'mk_momaking_quote_file'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    uid = Column(Integer, nullable=False, default=0, comment='用户ID')
    quote_no = Column(String(255), nullable=False, default='', comment='报价单号')
    hash = Column(String(32), nullable=False, default='', comment='报价单号')
    uuid = Column(String(255), nullable=False, default='', comment='上传用户')
    name = Column(String(255), nullable=False, default='', comment='文件名称')
    path = Column(String(255), nullable=False, default='', comment='文件路径')
    area = Column(Decimal(10, 2), nullable=False, default=0.00, comment='面积')
    length = Column(Decimal(10, 2), nullable=False, default=0.00, comment='长度')
    width = Column(Decimal(10, 2), nullable=False, default=0.00, comment='宽度')
    height = Column(Decimal(10, 2), nullable=False, default=0.00, comment='高度')
    volume = Column(Decimal(10, 2), nullable=False, default=0.00, comment='体积')
    weight = Column(Decimal(10, 2), nullable=False, default=0.00, comment='重量')
    quantity = Column(Integer, nullable=False, default=0, comment='数量')
    price = Column(Decimal(10, 2), nullable=False, default=0.00, comment='单价')
    preview = Column(String(255), nullable=False, default='', comment='预览图')
    notes = Column(String(255), nullable=False, default='', comment='备注')
    is_assembly = Column(SmallInteger, nullable=False, default=0, comment='是否是装配体')
    is_checked = Column(SmallInteger, nullable=False, default=0, comment='是否选中')
    is_analyze = Column(SmallInteger, nullable=False, default=0, comment='是否分析过')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态 1正常')
    is_delete = Column(SmallInteger, nullable=False, default=1, comment='是否删除')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'uid': self.uid,
            'quote_no': self.quote_no,
            'uuid': self.uuid,
            'name': self.name,
            'path': self.path,
            'area': self.area,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'volume': self.volume,
            'weight': self.weight,
            'quantity': self.quantity,
            'price': self.price,
            'preview': self.preview,
            'notes':self.notes,
            'is_assembly': self.is_assembly,
            'is_checked': self.is_checked,
            'create_time': create_time_str,
            'update_time': update_time_str,
            'status': self.status
        }
