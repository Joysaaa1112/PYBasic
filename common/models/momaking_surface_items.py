from . import db
from sqlalchemy import Column, Integer, String, func, JSON


class MomakingSurfaceItems(db.Model):
    __tablename__ = 'mk_momaking_surface_items'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    cn_name = Column(String(255), nullable=False, default='', comment='表面处理中文名')
    en_name = Column(String(255), nullable=False, default='', comment='表面处理英文名称')
    price = Column(String(255), nullable=False, default='', comment='基础价格')
    films = Column(JSON, nullable=False, comment='膜厚选项')

    def to_dict(self):
        return {
            'id': self.id,
            'cn_name': self.cn_name,
            'en_name': self.en_name,
            'price': self.price,
            'films': self.films,
        }
