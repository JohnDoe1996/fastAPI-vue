from datetime import datetime
 
from sqlalchemy import Column, Integer, DateTime, modifier
from sqlalchemy.orm import InstrumentedAttribute, properties
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from core.config import settings
from utils.transform import camel_case_2_underscore


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_time = Column(DateTime, default=datetime.now, server_default=func.now(), comment="创建时间")
    creator_id = Column(Integer, default=0, server_default='0', comment="创建人id")
    modified_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, server_default=func.now(),
                           server_onupdate=func.now(), comment="更新时间")
    modifier_id = Column(Integer, default=0, server_default='0', comment="修改人id")
    is_deleted = Column(Integer, default=0, comment="逻辑删除:0=未删除,1=删除", server_default='0')

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        return (settings.SQL_TABLE_PREFIX or "") + camel_case_2_underscore(cls.__name__)

    @staticmethod
    def dt2ts(column: Column, label: str):
        """
        使用原生SQL把数据库时间转换为时间戳(使用时间戳解决时区问题)
        :param column:  type: Column    需要转换的数据库日期字段
        :param label:   type: string    转后时间戳的的字段名(相当于 sql 中的 AS )
        """
        # return func.strftime('%%s', column).label(label)  # sqlite
        # return func.date_part('EPOCH', column).label(label) # psql
        return func.unix_timestamp(column).label(label)  # mysql

    @classmethod
    def listColumns(cls):
        """
        列出所有字段
        """
        return [getattr(cls, i) for i in dir(cls) if isinstance(getattr(cls, i), InstrumentedAttribute) 
                and isinstance(getattr(cls, i).comparator, properties.ColumnProperty.Comparator)]

    def dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def list(self):
        return [getattr(self, c.name, None) for c in self.__table__.columns]



