
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

# select database file
engine = create_engine('sqlite:///craigslist.db')
engine.echo = True

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# merges ignores the postings which already exist
def addPost(posting):
    try:
        session.add(posting)
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.merge(posting)
        session.commit()


def closeConnection():
    session.close()
