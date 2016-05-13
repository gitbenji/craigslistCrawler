
from session import Base, engine
from sqlalchemy import Column, String, Text, DateTime


class Posting(Base):
    __tablename__ = 'postings'

    id = Column(String, primary_key=True, unique=True)
    uri = Column(String)
    created = Column(DateTime)
    description = Column(Text)
    title = Column(String)
    compensation = Column(String)
    employment_type = Column(String)
    meta = Column(String)
    categories = Column(String)

Base.metadata.create_all(engine)
