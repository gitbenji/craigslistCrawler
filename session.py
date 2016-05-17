
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


def addToDb(row):
    try:
        session.add(row)
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.commit()


def getFromDb(class_name, **kwargs):
    return session.query(class_name).filter_by(**kwargs).first()


def closeConnection():
    session.close()
