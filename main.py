from fastapi import FastAPI, HTTPException, status

app = FastAPI()

tasks = [
    {"id" : 1, "title": "Attend interview", "done": True},
    {"id" : 2, "title": "Cook lunch", "done": True},
    {"id" : 3, "title": "Vaccuum house", "done": False}
]

@app.get("/")
async def root():
    return {"name": "Task API", "version" : "1.0", "endpoints" : ["/tasks"]}

@app.get("/health")
async def getStatus():
    return{"status": "OK"}

@app.get("/tasks")
async def getTasks():
    return tasks

@app.get("/tasks/{id}")
async def getOneTask(id: int):
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
    if not userTask.get("title"):
        raise HTTPException(
        status_code=400,
        detail="Title of task is missing or empty"
        )
    
    else:
        userID = len(tasks) + 1
        tasks.append({"id": userID, "title": userTask["title"], "done": False})