from .database import Base
from sqlalchemy import Column, String, Integer

class PersonModle(Base):
    __tablename__ = "persons"
    id= Column(Integer, primary_key=True)
    name = Column(String,unique=True)
    age = Column(Integer)