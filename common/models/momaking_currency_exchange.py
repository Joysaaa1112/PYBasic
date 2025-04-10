from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func, JSON
from sqlalchemy.dialects.mysql import DECIMAL as Decimal


class MomakingCurrencyExchange(db.Model):
    __tablename__ = 'mk_momaking_currency_exchange'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    currency = Column(String(255), nullable=False, default='', comment='货币名称')
    symbol = Column(String(255), nullable=False, default='', comment='货币符号')
    chinese_name = Column(String(255), nullable=False, default='', comment='中文名')
    rate = Column(Decimal(10, 2), nullable=False, default=0, comment='汇率')
    sort = Column(Integer, nullable=False, default=99, comment='排序')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'currency': self.currency,
            'symbol': self.symbol,
            'chinese_name': self.chinese_name,
            'rate': self.rate,
            'sort': self.sort,
            'create_time': create_time_str,
            'update_time': update_time_str
        }
