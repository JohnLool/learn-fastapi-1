from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from models import Base, Item, SessionLocal, engine

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    cost: float

class ItemUpdate(BaseModel):
    id: int
    name: str
    cost: float

class ItemDelete(BaseModel):
    id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/", response_model=List[ItemCreate])
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).filter(Item.deleted == 0).all()
    return items

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, cost=item.cost)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/")
def update_item(item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item.id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.cost = item.cost
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/")
def delete_item(item: ItemDelete, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item.id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.deleted = 1
    db.commit()
    return {"detail": "Item deleted"}
