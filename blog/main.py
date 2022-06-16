from os import name
from typing import List
from fastapi import Depends, FastAPI, status, Response, HTTPException
from .schemas import BlogSchema, BlogShow, UserSchema, UserShow
from .import models
from .models import Blog, User
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app=FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Blog CRUD Operations
@app.post("/blog", status_code=status.HTTP_201_CREATED,tags=["Blog CRUD"])
def create_new_blog(request:BlogSchema, db:Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[BlogShow], tags=["Get All Blogs"])
def get_all_blog(db:Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@app.get("/blog/{id}", response_model=BlogShow, status_code=status.HTTP_200_OK, tags=["Blog CRUD"])
def get_blog_by_id(id,response: Response,db:Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Blog with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} is not available"}
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blog CRUD"])
def delete_blog(id:int,db:Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'response': f"Blog with id {id} deleted sucessfully"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blog CRUD"])
def update_blog(id:int, request:BlogSchema, db:Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Blog with id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return {'response': f"Blog with id {id} updated sucessfully"}


@app.post("/user", response_model=UserShow,  status_code=status.HTTP_201_CREATED, tags=["User CRUD"])
def create_new_user(request: UserSchema, db:Session = Depends(get_db)):
    new_user = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=UserShow, tags=["User CRUD"])
def get_user_by_id(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"User with id {id} is not available")
    return user
    

@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User CRUD"])
def delete_user(id:int,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"User with id {id} is not available")
    user.delete(synchronize_session=False)
    db.commit()
    return {'response': f"User with id {id} deleted sucessfully"}

