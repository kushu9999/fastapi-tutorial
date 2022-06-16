from pydantic import BaseModel


class BlogSchema(BaseModel):
    title:str
    body:str

class BlogShow(BaseModel):
    title:str
    body:str

    class Config():
        orm_mode = True
