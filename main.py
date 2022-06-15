from fastapi import FastAPI

app = FastAPI(title="Kushal")

@app.get('/')
def index():
    return {"Status": {"API is Up and Running 200 ok"}}

@app.get('/about')
def about():
    return {"About": {"Kushal"}}