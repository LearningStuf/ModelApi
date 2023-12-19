from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

'''
This python scripts loads up the sqllite baic configurations for the model class to
load as a Base.


'''

project_path = Path(__file__).resolve().parent.parent
path = project_path / "data/users.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
