from . import db
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func


class Quotes(db.Model):
    __tablename__ = 'mk_quotes'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    uid = Column(Integer, nullable=False, default=0, comment='User ID')
    uuid = Column(String(255), nullable=False, default='', unique=True, comment='UUID')
    snowflake_id = Column(String(255), nullable=False, default='', comment='Quote Snowflake ID')
    technology = Column(SmallInteger, nullable=False, default=1, comment='加工工艺')
    unit = Column(SmallInteger, nullable=False, default=1, comment='单位 1mm 2cm 3inc')
    create_time = Column(DateTime, server_default=func.now(), comment='Create Time')
    update_time = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='Update Time')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态 1正常')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'uid': self.uid,
            'uuid': self.uuid,
            'snowflake_id': self.snowflake_id,
            'create_time': create_time_str,
            'update_time': update_time_str,
            'status': self.status
        }
