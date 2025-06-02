from sqlmodel import SQLModel, create_engine, Session
from app.core.config import SQLMODEL_DATABASE_URL

engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Add SessionLocal for backward compatibility
SessionLocal = Session