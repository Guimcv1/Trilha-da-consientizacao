from models.model import engine
from sqlalchemy.orm import sessionmaker

def Session():
    try:
        SessionM = sessionmaker(bind=engine)
        session = SessionM()
        yield session
    finally:
        session.close()



