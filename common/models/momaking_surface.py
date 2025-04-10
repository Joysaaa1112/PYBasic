from . import db
from sqlalchemy import Column, Integer, String, DateTime, func


class MomakingSurface(db.Model):
    __tablename__ = 'mk_momaking_surface'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    cn_name = Column(String(255), nullable=False, default='', comment='表面处理中文名')
    en_name = Column(String(255), nullable=False, default='', comment='表面处理英文名称')
    price = Column(String(255), nullable=False, default='', comment='基础价格')
    cn_remark = Column(String(255), nullable=False, default='', comment='备注')
    en_remark = Column(String(255), nullable=False, default='', comment='备注')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'cn_name': self.cn_name,
            'en_name': self.en_name,
            'price': self.price,
            'cn_remark': self.cn_remark,
            'en_remark': self.en_remark,
        }

    def to_attr(self):
        return {
            'id': self.id,
            'name': self.cn_name + ' ' + self.en_name,
            'price': self.price,
        }
