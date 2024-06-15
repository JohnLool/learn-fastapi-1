from fastapi import FastAPI

app = FastAPI()

storage = []


@app.get("/{text}")
def read_item(text):
    return {"text": text}


@app.get("/items/")
def get_items():
    return {"items": storage}


@app.post("/items/")
def create_item(item: dict):
    storage.append(item)
    return {"message": "Item added successfully", "item": item}
