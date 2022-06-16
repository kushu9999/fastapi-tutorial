from unicodedata import name
from pydantic import BaseModel, EmailStr


class BlogSchema(BaseModel):
    title:str
    body:str

class BlogShow(BaseModel):
    title:str
    body:str

    class Config():
        orm_mode = True

class UserSchema(BaseModel):
    name:str 
    email:EmailStr
    password:str

class UserShow(BaseModel):
    name:str 
    email:EmailStr

    class Config():
        orm_mode = True

