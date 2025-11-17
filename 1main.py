from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# FastAPI app
app = FastAPI()

# Database URL (change user, password, host, dbname as per your setup)
DATABASE_URL = "postgresql://postgres:postgres@db:5432/fastapidb"
# DATABASE_URL = "mysql+pymysql://root:Mido@127.0.0.1:3306/fastapidb"


# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM Model

class PersonModel(Base):
    __tablename__ = "persons"  # ✅ required!

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for input/output
class Person(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True


# GET method
@app.get("/")
def greet():
    return {"message": "Hey! Welcome"}


@app.get("/look_user")
def get_user(db: Session =Depends(get_db)):
    all_user=db.query(PersonModel).all()
    return all_user

# POST method - Add a new person
@app.post("/add-person")
def add_person(person: Person, db: Session = Depends(get_db)):
    existing = db.query(PersonModel).filter(PersonModel.name == person.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Person already exists")

    new_person = PersonModel(name=person.name, age=person.age)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return {"message": f"{person.name} added successfully", "data": {"id": new_person.id, "name": new_person.name, "age": new_person.age}}


# PUT/PATCH method - Update age
@app.put("/update-age/{name}")
def update_age(name: str, age: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).filter(PersonModel.name == name).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    person.age = age
    db.commit()
    db.refresh(person)

    return {"message": f"{name}'s age updated successfully", "data": {"id": person.id, "name": person.name, "age": person.age}}


# DELETE method - Delete a person
@app.delete("/delete-person/{name}")
def delete_person(name: str, db: Session = Depends(get_db)):
    person = db.query(PersonModel).filter(PersonModel.name == name).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.commit()

    return {"message": f"{name} deleted successfully"}