from fastapi import FastAPI
from . import schemas
from . import models
from . import database as db


app=FastAPI()

models.Base.metadata.create_all(db.engine)


@app.post("/")
def create(request:schemas.Blog):
    return request
    