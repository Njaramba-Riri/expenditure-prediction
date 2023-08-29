from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []

templates = Jinja2Templates(directory="templates/")

@todo_router.post("/todo", status_code=201)
async def add_todo(request=Request, todo: todo = Depends(todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "todos": todo_list
    })

@todo_router.get('/todo', response_model=TodoItems)
async def retrieve_todos(request: Request):
    return templates.TemplateResponse("todo.html", {
        "request": request,
        "todos": todo_list 
    })

@todo_router.get("/todo/{todo_id}")
async def retrieve_single_todo(request: Request, todo_id: int = Path(..., title="This is the id of the todo to retrieve.")):
    for todo in todo_list:
        if todo.Id == todo_id:
            return templates.TemplateResponse("todo.html", {
                "request": request,
                "todo": todo
            })
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with the suplied ID doesn't exist."
    ) 

@todo_router.put("/todo/{to_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The ID of the todo to be update")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Todo update successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with the supplied ID doesn't exist.",
       
       )

@todo_router.delete("todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for i in range(len(todo_list)):
        todo = todo_list[i]
        if todo.id == todo_id:
            todo_list.pop(i)
            return {
                "message": "Todo deleted successfully."
            }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with the supplied ID doens't exist.",
        )

@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "All todos deleted successfully."
    }

