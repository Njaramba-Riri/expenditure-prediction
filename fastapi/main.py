from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import Union
import uvicorn
from todo import todo_router

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer : Union [bool, None]=None

@app.get('/')
async def home() -> dict:
    return { 
        "Hello": "World!!"
    }

@app.get('/items/{item_id}')
def read_item(item_id: int, q:Union[str, None]=None):
    return {
        "item_id":item_id, 
        "q":q
    }


@app.put("/items/{item_id}")
def update_item(item_id: int, item:Item):
    return{
        "item_price":item.price, 
        "item_id": item_id
    }

app.include_router(todo_router)

if __name__=="__main__":
    uvicorn.run(app, host="127:0:0:1", port=8000)
