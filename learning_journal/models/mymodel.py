from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    title1 = Column(Unicode)
    creation_date = Column(Date)
    body = Column(Unicode)


Index('my_index', MyModel.title, unique=True, mysql_length=500)
