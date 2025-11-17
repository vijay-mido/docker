from fastapi import APIRouter, Depends
from .database import get_db,Session
from .models import PersonModle
from .Schema import *

route=APIRouter()

@route.get("/get_user")
def all_users(db: Session=Depends(get_db)):
    all_users=db.query(PersonModle).all()
    return all_users

@route.post("/create_user")
def Create_user(user:create_user,db:Session=Depends(get_db)):
    new_user= PersonModle(name=user.name,age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.name

@route.put("/update_user/{id}")
def Update_user(id:int,user:update_user,db: Session=Depends(get_db)):
    update_user= db.query(PersonModle).filter(PersonModle.id==id).first()
    update_user.age=user.age
    update_user.name=user.name
    db.commit()
    db.refresh(update_user)
    return {f"name of the user is {update_user.name} and age of the user is {update_user.age} has been updated"}


@route.delete("/delete-user/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(PersonModle).filter(PersonModle.id == id).first()
    if not user:
        return {"error": "User not found"}
    username = user.name  # store BEFORE deleting
    db.delete(user)
    db.commit()
    return {"message": f"User '{username}' has been deleted successfully"}
