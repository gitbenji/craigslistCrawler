
from session import Base, engine
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


# association_table = Table('association', Base.metadata,
#     Column('posting_id', Integer, ForeignKey('postings.id')),
#     Column('category_id', Integer, ForeignKey('categories.id'))
# )


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
    categories = relationship('Category', backref='postings', lazy='joined')
    # categories = relationship('Category', secondary=association_table)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=True)
    posting_id = Column(Integer, ForeignKey('postings.id'))


Base.metadata.create_all(engine)
