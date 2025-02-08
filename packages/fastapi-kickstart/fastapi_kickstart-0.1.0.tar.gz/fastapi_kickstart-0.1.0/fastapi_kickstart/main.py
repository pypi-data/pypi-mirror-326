from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# In-memory data store
inventory = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the app!"}

@app.get("/get-item/{item_id}")
def get_item(item_id: int, name: Optional[str] = None):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID not found.")
    if name and inventory[item_id].name != name:
        raise HTTPException(status_code=404, detail="Item name not found.")
    
    return inventory[item_id]

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    inventory[item_id] = item

    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    # If name wasn't left blank, update name and so on...
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.description != None:
        inventory[item_id].description = item.description

    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    # Deletes the item from the item inventory dictionary, our data store
    del inventory[item_id]
    
    return {"Success": "Item deleted!"}
