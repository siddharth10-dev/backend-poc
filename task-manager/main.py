from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

db: List[Task] = []

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return db

@app.post("/tasks", status_code=201)
async def create_task(task: Task):
    db.append(task)
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(db):
        if task.id == task_id:
            db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(db):
        if task.id == task_id:
            deleted_task = db.pop(index)
            return {"message": f"Task '{deleted_task.title}' deleted"}
    raise HTTPException(status_code=404, detail="Task not found")