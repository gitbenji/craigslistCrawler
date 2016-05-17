
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

# select database file
engine = create_engine('postgresql://benji@localhost:5432/job_postings')
engine.echo = True

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# merges ignores the postings which already exist
def addToDb(row):
    try:
        session.add(row)
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.commit()


# merges ignores the postings which already exist
def addPosting(row):
    try:
        session.add(row)
        session.commit()
    except IntegrityError:
        session.rollback()
        session.merge(row)
    finally:
        session.commit()


def closeConnection():
    session.close()
