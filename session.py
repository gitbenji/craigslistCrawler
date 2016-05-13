
import model

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=model.engine)

session = Session()

# merges ignores the postings which already exist
def addPost (posting):
    session.merge(posting)

def commitAll ():
    session.commit()

def closeConnection ():
    session.close()
