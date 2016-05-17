
from session import Base, engine
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Posting(Base):
    __tablename__ = 'postings'

    id = Column(Integer, primary_key=True, unique=True)
    uid = Column(String)
    uri = Column(String)
    created = Column(DateTime)
    description = Column(Text)
    title = Column(String)
    compensation = Column(String)
    employment_type = Column(String)
    meta = Column(String)
    categories = Column(String, ForeignKey('categories.category'))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, unique=True)
    category = Column(String, unique=True)
    postings = relationship('Posting')


Base.metadata.create_all(engine)
