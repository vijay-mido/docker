from pydantic import BaseModel

class create_user(BaseModel):
    name:str
    age:int
    
class update_user(create_user):
    pass