from pydantic import BaseModel
from typing import List, Optional

class todo(BaseModel):
    id: Optional[int]
    item: str

    @classmethod
    def as_form(
        cls, 
        item: str = Form(...)
    ):
        return cls(item=item)

"""
#Nested model
class Item(BaseModel):
    item: str
    status: str 

class todo(BaseModel):
    id: int
    item: Item
"""

class TodoItem(BaseModel):
    item: str

    class Config:
        schema_extra = {
            "example": {
                "item": "Moving to Paris."
            }
        } 

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {
                        "item": "Example schema 1!."
                    },
                    {
                        "item": "Example schema 2!"
                    }
                ]
            }
        }   