# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """
    Demonstrates path parameter and query parameter handling.
    Example GET request: /items/123?q=fastapi
    """
    return {"item_id": item_id, "q": q}