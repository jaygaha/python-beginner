from fastapi import FastAPI

app = FastAPI(title="My First API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
