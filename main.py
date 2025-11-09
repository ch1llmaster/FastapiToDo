from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="Simple To-Do API")


class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool = False


# simple db
todos: List[TodoItem] = []


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to To-Do API!"}


@app.get("/todos", response_model=List[TodoItem], tags=["ToDo"])
def get_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=TodoItem, tags=["ToDo"])
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/todos", response_model=TodoItem, tags=["ToDo"])
def create_todo(item: TodoItem):
    for todo in todos:
        if todo.id == item.id:
            raise HTTPException(status_code=400, detail="ID is already exists")
    todos.append(item)
    return item


@app.put("/todos/{todo_id}", response_model=TodoItem, tags=["ToDo"])
def update_todo(todo_id: int, item: TodoItem):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = item
            return item
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/todos/{todo_id}", tags=["ToDo"])
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[i]
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    uvicorn.run("main:app")
