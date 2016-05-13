
import model

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=model.engine)

session = Session()

def addPost (posting):
    session.add(posting)

def commitAll ():
    session.commit()

def closeConnection ():
    session.close()
