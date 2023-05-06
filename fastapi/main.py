from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app=FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer : Union [bool, None]=None

@app.get('/')
def home():
    return{"Hello":"World!!"}

@app.get('/items/{item_id}')
def read_item(item_id: int, q:Union[str, None]=None):
    return {"item_id":item_id, "q":q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item:Item):
    return{"item_price":item.price, "item_id": item_id}
    
#if __name__=="__main__":
 #   uvicorn.run(app, host="127:0:0:1", port=8000)
