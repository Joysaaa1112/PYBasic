from . import db
from sqlalchemy import Column, Integer, DECIMAL, JSON, DateTime, func, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class MomakingCNCAnalysis(db.Model):
    __tablename__ = 'mk_momaking_cnc_analysize'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    file_id = Column(Integer, nullable=False, default=0, comment='文件ID')
    unit = Column(SmallInteger, nullable=False, default=1, comment='单位 1mm 2cm 3inc')
    info = Column(JSON, nullable=False, comment='模型几何数据')
    material = Column(JSON, nullable=False, comment='材料基础数据')
    analysis = Column(JSON, nullable=False, comment='分析数据')
    reports = Column(JSON, nullable=False, comment='报告数据')
    difficulty = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='难度系数')
    forecast_time = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='难度预计工时 (min)')
    volume_time = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='预计体积时间 (min)')
    total_time = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='总工时 (min)')
    processing_cost = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='加工费用')
    surface_treatment_cost = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='表面处理费用')
    packaging_cost = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='包装费')
    management_fee = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='管理费')
    tax_invoice_fee = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='税费')
    material_cost = Column(String(32), nullable=False, default='0', comment='材料费用')
    total_cost = Column(DECIMAL(10, 2), nullable=False, default='0', comment='总费用')
    origin_cost = Column(DECIMAL(10, 2), nullable=False, default='0', comment='原始价格')
    programming_debugging_fee = Column(String(32), nullable=False, default=0.00, comment='编程和调机费')
    materials_pro_debug_cost = Column(String(32), nullable=False, default=0.00, comment='材料和编程+调机费')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态 1正常')

    def to_dict(self):
        create_time_str = self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        update_time_str = self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        return {
            'id': self.id,
            'file_id': self.file_id,
            'unit': self.unit,
            'info': self.info,
            'material': self.material,
            'analysis': self.analysis,
            'reports': self.reports,
            'difficulty': self.difficulty,
            'forecast_time': self.forecast_time,
            'volume_time': self.volume_time,
            'total_time': self.total_time,
            'processing_cost': self.processing_cost,
            'surface_treatment_cost': self.surface_treatment_cost,
            'packaging_cost': self.packaging_cost,
            'management_fee': self.management_fee,
            'tax_invoice_fee': self.tax_invoice_fee,
            'total_cost': self.total_cost,
            'origin_cost': self.origin_cost,
            'programming_debugging_fee': self.programming_debugging_fee,
            'materials_pro_debug_cost': self.materials_pro_debug_cost,
            'material_cost': self.material_cost,
            'create_time': create_time_str,
            'update_time': update_time_str,
            'status': self.status
        }
