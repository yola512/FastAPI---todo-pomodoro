from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models import Task, TaskBase, Pomodoro
from app.database import tasks, pomodoro_sessions, generate_id
from datetime import datetime, timedelta

router = APIRouter()

# tasks:
# creating new tasks
@router.post("/tasks", response_model=Task)
def create_new_task(task: TaskBase):
    for t in tasks:
      if t["title"].lower() == task.title.lower():
        raise HTTPException(status_code=400, detail="That title already exists")
      
    new_task = task.model_dump() # dictionary representation of the model
    new_task['id'] = generate_id(tasks)

    tasks.append(new_task)
    return new_task

# get task list (optional filter by status)
@router.get("/tasks", response_model=list[Task])
def get_all_tasks(status: Optional[str] = None):
    if status:
        return [task for task in tasks if task["status"].lower() == status.lower()]
    return tasks

# get task details
@router.get("/tasks/{task_id}", response_model = TaskBase)
def get_task_details(task_id: int):
  for task in tasks:
    if task["id"] == task_id:
       return task
    
  # if task wasnt found:
  raise HTTPException(status_code=404, detail="Task with this ID doesn't exist.")

# update task
@router.put("/tasks/{task_id}", response_model = Task)
def update_task(task_id: int, updated_task: TaskBase ):
    # check if task(task_id) exists
    task = None
    for t in tasks:
      if t["id"] == task_id:
         task = t
         break
    
    if task is None:
      raise HTTPException(status_code=404, detail="Task with this ID doesn't exist.")

    # check if title is unique
    for t in tasks:
       if t["title"].lower() == updated_task.title.lower() and t["id"] != task_id:
          raise HTTPException(status_code=400, detail="This task title already exists")
    
    # update task
    task.update(updated_task.model_dump())
    return task

# deleting task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    # check if task(task_id) exists
    task = None
    for t in tasks:
      if t["id"] == task_id:
         task = t
         break
      
    if task is None:
       raise HTTPException(status_code=404, detail="Task with this ID doesn't exist.")
    
    # delete task
    tasks.remove(task)

    #return {"message": "Task has been deleted"}

# pomodoro
# create pomodoro timer
@router.post("/pomodoro")
def create_timer(task_id: int, timer: Pomodoro, end_time: int = 25):
    # check if task(task_id) exists
    task = None
    for t in tasks:
      if t["id"] == task_id:
         task = t
         break
      
    if task is None:
       raise HTTPException(status_code=404, detail="Task with this ID doesn't exist.")
    
    # check if there's an active pomodoro timer
    for session in pomodoro_sessions:
       if session["task_id"] == task_id and session["completed"] == False:
          raise  HTTPException(status_code=400, detail="Pomodoro timer is already running for this task.")
    
    # create a new pomodoro timer
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=end_time)

    pom_session = Pomodoro(task_id = task_id,
                                 start_time=start_time,
                                 end_time=end_time,
                                 completed=False)
    
    # add new timer to sessions list
    pomodoro_sessions.append(pom_session.model_dump())

    #return {"message": "Pomodoro timer has been created", "pomodoro": pom_session.modeldump()}

# stop pomodoro timer
@router.post("/pomodoro/{task_id}/stop")
def stop_timer(task_id: int):
   # check if task(task_id) exists
    task = None
    for t in tasks:
      if t["id"] == task_id:
         task = t
         break
      
    if task is None:
       raise HTTPException(status_code=404, detail="Task with this ID doesn't exist.")
    
    # check if there's an active timer
    active_session = None
    for session in pomodoro_sessions:
       if session["task_id"] == task_id and session["completed"] == False:
          active_session = session
          break
    
    if not active_session:
       raise HTTPException(status_code=400, detail="No active Pomodoro timer for this task.")
    
    # stop timer
    active_session["completed"] = True
    active_session["end_time"] = datetime.now()

    return {"message": "Timer has been stopped!", "pomodoro": active_session}

# get pomodoro stats
@router.get("/pomodoro/stats")
def get_timer_stats():
   count_sessions = 0
   total_time = 0 # seconds
   
   for session in pomodoro_sessions:
      if session["completed"] == True:
         count_sessions += 1

         start_time = session["start_time"]
         end_time = session["end_time"]
         
         # calculate session duration
         session_duration = (end_time - start_time).total_seconds()
         total_time += session_duration
    
   if count_sessions == 0:
      return { "completed_sessions": 0, "total_time_spent_minutes": 0}
   
   total_time_in_minutes = total_time / 60
   
   return { 
        "completed_sessions": count_sessions,
        "total_time_spent_minutes": total_time_in_minutes
    }
