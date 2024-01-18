from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(schema='public')


class SharedBase(DeclarativeBase):
    metadata = MetaData(schema='shared')
