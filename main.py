from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]


app = FastAPI(title="Kushal")

@app.get('/')
def index():
    return {"Status": "API is Up and Running 200 ok"}

@app.get('/blog')
def about(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published of blogs"}
    else:
        return {"data": f"{limit} of blogs"}

@app.get('/blog/unpublished')
def about():
    return {"data": "unpublished blogs"}

@app.get('/blog/{id}')
def about(id:int):
    return {"data": id}

@app.get('/blog/{id}/comments')
def about(id:int, limit=10):
    return limit
    return {"data": "comments here"}

@app.post('/blog')
def create_blog(blog:Blog):
    return {"data": f"blog is created title as {blog.title} and body as '{blog.body}'"}

# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=9000)