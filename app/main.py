from fastapi import FastAPI, HTTPException

from app.schemas.projectcreate import ProjectCreate, ProjectUpdate

APP_NAME = "Board API"
APP_VERSION = "0.1.0"


app = FastAPI(title=APP_NAME, version=APP_VERSION, description="This is Board Api")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def get_service_info():
    return {"name": APP_NAME, "version": APP_VERSION, "docs": "/docs"}


projects = {
    1: {"id": 1, "name": "Backend", "description": "aasadad"},
    2: {"id": 2, "name": "Frontend", "description": "df"},
    3: {"id": 3, "name": "Backend", "description": "32"},
    4: {"id": 4, "name": "Frontend", "description": "a21"},
    5: {"id": 5, "name": "Backend", "description": "sdf"},
    6: {"id": 6, "name": "Frontend", "description": "ddd"},
}


@app.get("/projects")
def get_projects():
    return list(projects.values())


@app.get("/projects/{project_id}", status_code=200)
def get_project_by_id(project_id: int):
    project = projects.get(project_id)
    if not project:
        raise HTTPException(404, "No such project")
    return project


@app.post("/projects", status_code=201)
def create_project(project: ProjectCreate):
    new_id = max(projects) + 1
    data = {"id": new_id, **project.model_dump()}
    projects[new_id] = data
    return data


@app.delete("/projects/{project_id}", status_code=204)
def cancel_project(project_id: int):
    canceled_project = projects.pop(project_id, None)
    if not canceled_project:
        raise HTTPException(404, "No such project")


@app.patch("/projects/{project_id}", status_code=200)
def update_project(project_id: int, project_update: ProjectUpdate):
    project = projects.get(project_id)
    if not project:
        raise HTTPException(404, "No such project")
    projects.update(**project_update.model_dump(exclude_unset=True))
    return projects[project_id]
