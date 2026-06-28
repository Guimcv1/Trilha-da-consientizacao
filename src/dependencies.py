from main import engine
from sqlalchemy.orm import sessionmaker

# Depêndencia que gera uma sessão SQLAlchemy para cada requisição.
# O FastAPI fecha a sessão automaticamente ao final do request.

def get_session():
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
