from fastapi import FastAPI, HTTPException, status

app = FastAPI()

tasks = [
    {"id" : 1, "title": "Attend interview", "done": True},
    {"id" : 2, "title": "Cook lunch", "done": True},
    {"id" : 3, "title": "Vaccuum house", "done": False}
]

@app.get("/")
async def root():
    """
    This endpoint returns the basic details of this API
    """
    return {"name": "Task API", "version" : "1.0", "endpoints" : ["/tasks"]}

@app.get("/health")
async def getStatus():
    """
    This endpoint returns the status of the API. If it returns OK, the API is working. Else, it is not.
    """
    return{"status": "OK"}

@app.get("/tasks")
async def getTasks():
    """
    This endpoint returns the list of tasks that serve as the local database for Assignment 1.
    """
    return tasks

@app.get("/tasks/{id}")
async def getOneTask(id: int):
    """
    This endpoint returns only one task depending on the ID in the URL.
    """
    for i in range(len(tasks)):
        currentTask = tasks[i]
        if(currentTask.get("id") == id):
            return tasks[i]
        
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

@app.post("/tasks", status_code=201)
async def makeTask(userTask: dict):
    """
    This endpoint makes a task depending on user input.
    """
    if not userTask.get("title"):
        raise HTTPException(
        status_code=400,
        detail="Title of task is missing or empty"
        )
    
    else:
        userID = len(tasks) + 1
        tasks.append({"id": userID, "title": userTask["title"], "done": False})

@app.put("/tasks/{id}", status_code=201)
async def updateTask(userTask: dict):
    """
    This endpoint updates the user's task depending on their input.
    """

    if not userTask:
        raise HTTPException(
            status_code=400,
            detail="Empty or invalid body"
        )

    id = userTask.get("id")
    if not id:
        raise HTTPException(
            status_code=404,
            detail="ID is missing"
        )
    
    taskToUpdate = tasks[id-1]

    if userTask.get("title"):
        taskToUpdate["title"] = userTask["title"]
    if userTask.get("done"):
        taskToUpdate["done"]= userTask["done"]
    return taskToUpdate

@app.delete("/tasks/{id}", status_code=204)
async def deleteTask(userTask: dict):
    """
    This endpoint deletes the task the user wants deleted
    """
    if not userTask.get("id"):
        raise HTTPException(
            status_code=404,
            detail="Unkown ID"
        )
    
    else:
        index = userTask.get("id")-1
        tasks.pop(index)
        return {}