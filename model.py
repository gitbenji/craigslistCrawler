
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

# select database file
engine = create_engine('sqlite:///craigslist.db')
engine.echo = False

Base = declarative_base()

class Posting(Base):
    __tablename__ = 'postings'

    id = Column(String, primary_key=True)
    uri = Column(String)
    created = Column(DateTime)
    description = Column(Text)
    title = Column(String)
    compensation = Column(String)
    employment_type = Column(String)
    meta = Column(String)
    categories = Column(String)

Base.metadata.create_all(engine)
