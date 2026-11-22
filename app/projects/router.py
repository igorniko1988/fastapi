from fastapi import APIRouter, HTTPException, Query

from app.projects.schemas import ProjectCreate, ProjectUpdate
from app.projects.storage import projects

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def get_projects(
    search: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    result = list(projects.values())

    if search:
        result = [b for b in result if search.lower() in b["name"].lower()]

    return result[offset : offset + limit]


@router.get("/{project_id}", status_code=200)
def get_project_by_id(project_id: int):
    project = projects.get(project_id)
    if not project:
        raise HTTPException(404, "No such project")
    return project


@router.post("", status_code=201)
def create_project(project: ProjectCreate):
    new_id = max(projects) + 1
    data = {"id": new_id, **project.model_dump()}
    projects[new_id] = data
    return data


@router.delete("/{project_id}", status_code=204)
def cancel_project(project_id: int):
    canceled_project = projects.pop(project_id, None)
    if not canceled_project:
        raise HTTPException(404, "No such project")


@router.patch("/{project_id}", status_code=200)
def update_project(project_id: int, project_update: ProjectUpdate):
    project = projects.get(project_id)
    if not project:
        raise HTTPException(404, "No such project")
    project.update(project_update.model_dump(exclude_unset=True))
    return project
