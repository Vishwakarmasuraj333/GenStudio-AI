from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.project import Project
from app.models.generation import MediaAsset, GenerationJob
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.schemas.generation import MediaAssetOut

router = APIRouter()

@router.get("/", response_model=List[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    projects = db.query(Project).filter(
        Project.user_id == current_user.id,
        Project.is_archived == False
    ).order_by(Project.created_at.desc()).all()

    results = []
    for p in projects:
        j_count = db.query(GenerationJob).filter(GenerationJob.project_id == p.id).count()
        a_count = db.query(MediaAsset).filter(MediaAsset.project_id == p.id).count()
        results.append(ProjectOut(
            id=p.id,
            user_id=p.user_id,
            name=p.name,
            description=p.description,
            is_archived=p.is_archived,
            created_at=p.created_at,
            updated_at=p.updated_at,
            job_count=j_count,
            asset_count=a_count
        ))
    return results

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = Project(
        user_id=current_user.id,
        name=project_in.name,
        description=project_in.description
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        is_archived=project.is_archived,
        created_at=project.created_at,
        updated_at=project.updated_at,
        job_count=0,
        asset_count=0
    )

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    j_count = db.query(GenerationJob).filter(GenerationJob.project_id == project.id).count()
    a_count = db.query(MediaAsset).filter(MediaAsset.project_id == project.id).count()
    return ProjectOut(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        is_archived=project.is_archived,
        created_at=project.created_at,
        updated_at=project.updated_at,
        job_count=j_count,
        asset_count=a_count
    )

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    if project_in.name is not None:
        project.name = project_in.name
    if project_in.description is not None:
        project.description = project_in.description
    if project_in.is_archived is not None:
        project.is_archived = project_in.is_archived

    db.commit()
    db.refresh(project)
    j_count = db.query(GenerationJob).filter(GenerationJob.project_id == project.id).count()
    a_count = db.query(MediaAsset).filter(MediaAsset.project_id == project.id).count()
    return ProjectOut(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        is_archived=project.is_archived,
        created_at=project.created_at,
        updated_at=project.updated_at,
        job_count=j_count,
        asset_count=a_count
    )

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    db.delete(project)
    db.commit()
    return None

@router.get("/{project_id}/assets", response_model=List[MediaAssetOut])
def get_project_assets(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assets = db.query(MediaAsset).filter(
        MediaAsset.project_id == project_id,
        MediaAsset.user_id == current_user.id
    ).order_by(MediaAsset.created_at.desc()).all()
    return assets
