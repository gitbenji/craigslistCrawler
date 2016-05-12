
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

engine = create_engine('sqlite:///craigslist.db')
engine.echo = False

Base = declarative_base()

class Posting(Base):
    __tablename__ = 'postings'

    id = Column(Text, primary_key=True, unique=False)
    uri = Column(Text)
    created = Column(Text)
    description = Column(Text)
    title = Column(Text)
    compensation = Column(Text)
    employment_type = Column(Text)
    meta = Column(Text)
    categories = Column(Text)

Base.metadata.create_all(engine)
