from fastapi import APIRouter, Query

from app.projects.exceptions import ProjectNotFoundError
from app.projects.schemas import ProjectCreate, ProjectUpdate
from app.projects.storage import projects

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_or_404(project_id: int):
    project = projects.get(project_id)
    if not project:
        raise ProjectNotFoundError(project_id)
    return project


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
    return get_project_or_404(project_id)


@router.post("", status_code=201)
def create_project(project: ProjectCreate):
    new_id = max(projects) + 1
    data = {"id": new_id, **project.model_dump()}
    projects[new_id] = data
    return data


@router.delete("/{project_id}", status_code=204)
def cancel_project(project_id: int):
    get_project_or_404(project_id)
    del projects[project_id]


@router.patch("/{project_id}", status_code=200)
def update_project(project_id: int, project_update: ProjectUpdate):
    project = get_project_or_404(project_id)
    project.update(project_update.model_dump(exclude_unset=True))
    return project
