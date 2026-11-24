from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.generation import MediaAsset
from app.schemas.generation import MediaAssetOut

router = APIRouter()

@router.get("/", response_model=List[MediaAssetOut])
def list_library_assets(
    media_type: Optional[str] = None, # image, video
    favorites_only: bool = False,
    project_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(MediaAsset).filter(MediaAsset.user_id == current_user.id)
    if media_type:
        query = query.filter(MediaAsset.media_type == media_type)
    if favorites_only:
        query = query.filter(MediaAsset.is_favorite == True)
    if project_id:
        query = query.filter(MediaAsset.project_id == project_id)

    assets = query.order_by(MediaAsset.created_at.desc()).offset(offset).limit(limit).all()
    return assets

@router.put("/{asset_id}/favorite", response_model=MediaAssetOut)
def toggle_favorite(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    asset = db.query(MediaAsset).filter(
        MediaAsset.id == asset_id,
        MediaAsset.user_id == current_user.id
    ).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Media asset not found.")

    asset.is_favorite = not asset.is_favorite
    db.commit()
    db.refresh(asset)
    return asset

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    asset = db.query(MediaAsset).filter(
        MediaAsset.id == asset_id,
        MediaAsset.user_id == current_user.id
    ).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Media asset not found.")

    import os
    if asset.file_path and os.path.exists(asset.file_path):
        try:
            os.remove(asset.file_path)
        except Exception:
            pass

    db.delete(asset)
    db.commit()
    return None
