from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine, Integer, String

DATABASE_URL="postgresql://postgres:postgres@db:5432/fastapidb"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=False, autocommit=False)
Base=declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()