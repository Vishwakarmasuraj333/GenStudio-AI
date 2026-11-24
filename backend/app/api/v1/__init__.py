from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.studio import router as studio_router
from app.api.v1.projects import router as projects_router
from app.api.v1.library import router as library_router
from app.api.v1.history import router as history_router
from app.api.v1.experiments import router as experiments_router
from app.api.v1.usage import router as usage_router
from app.api.v1.admin import router as admin_router
from app.api.v1.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(studio_router, prefix="/studio", tags=["Studio Generation"])
api_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
api_router.include_router(library_router, prefix="/library", tags=["Library"])
api_router.include_router(history_router, prefix="/history", tags=["History"])
api_router.include_router(experiments_router, prefix="/experiments", tags=["Research & Benchmarks"])
api_router.include_router(usage_router, prefix="/usage", tags=["Usage & Costs"])
api_router.include_router(admin_router, prefix="/admin", tags=["Administration"])
