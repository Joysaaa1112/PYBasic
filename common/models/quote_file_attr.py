from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func, JSON


class QuoteFileAttr(db.Model):
    __tablename__ = 'mk_quote_file_attr'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    uid = Column(Integer, nullable=False, default=0, comment='用户ID')
    quote_id = Column(Integer, nullable=False, default=0, comment='报价ID')
    file_id = Column(Integer, nullable=False, default=0, comment='文件ID')
    attr_values = Column(JSON, nullable=False, comment='属性值')
    create_time = Column(DateTime, server_default=func.now(), comment='Create Time')
    update_time = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp(),
                         comment='Update Time')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'uid': self.uid,
            'quote_id': self.quote_id,
            'file_id': self.file_id,
            'attr_values': self.attr_values,
            'create_time': create_time_str,
            'update_time': update_time_str,
            'status': self.status
        }
