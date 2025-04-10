from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func, JSON
from sqlalchemy.dialects.mysql import DECIMAL as Decimal


class MomakingCategory(db.Model):
    __tablename__ = 'mk_momaking_category'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    cn_name = Column(String(255), nullable=False, default='', comment='中文名')
    en_name = Column(String(255), nullable=False, default='', comment='英文名')
    parent = Column(Integer, nullable=False, default=0, comment='父ID')
    type = Column(SmallInteger, nullable=False, default=1, comment='分类类型 1Process 2Finish 3Material 4Color')
    color = Column(String(255), nullable=False, default='', comment='颜色')
    price = Column(String(255), nullable=False, default='', comment='每单位价格')
    craft = Column(SmallInteger, nullable=False, default=1, comment='工艺 1:3d打印 2:CNC Machining 3:Sheet Metal Fabrication 4:Injection Molding 5:Die Casting')
    unit = Column(SmallInteger, nullable=False, default=1, comment='单位 1:mm 2:cm 3:inc')
    density = Column(String(255), nullable=False, default='', comment='密度')
    difficulty = Column(String(255), nullable=False, default='', comment='加工难度 基准值为1')
    weight = Column(String(255), nullable=False, default='', comment='重量')
    alias = Column(String(255), nullable=False, default='', comment='别名')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态 1正常')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'cn_name': self.cn_name,
            'en_name': self.en_name,
            'parent': self.parent,
            'type': self.type,
            'color': self.color,
            'price': self.price,
            'craft': self.craft,
            'unit': self.unit,
            'density': self.density,
            'difficulty': self.difficulty,
            'weight': self.weight,
            'alias': self.alias,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'status': self.status
        }
