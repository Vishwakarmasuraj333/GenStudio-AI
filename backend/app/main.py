from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models.model_registry import ModelRegistryEntry
from app.providers.registry import CURATED_MODELS
from app.api.v1 import api_router

def seed_model_registry():
    """Populates model registry with curated real model records if empty."""
    db = SessionLocal()
    try:
        for model_data in CURATED_MODELS:
            existing = db.query(ModelRegistryEntry).filter(
                ModelRegistryEntry.model_id == model_data["model_id"]
            ).first()
            if not existing:
                entry = ModelRegistryEntry(
                    provider=model_data["provider"],
                    model_id=model_data["model_id"],
                    display_name=model_data["display_name"],
                    version=model_data.get("version"),
                    task_types=model_data["task_types"],
                    max_resolution=model_data.get("max_resolution", "1024x1024"),
                    supported_aspect_ratios=model_data.get("supported_aspect_ratios", []),
                    capabilities_json=model_data.get("capabilities_json", {}),
                    pricing_json=model_data.get("pricing_json", {}),
                    license_info=model_data.get("license_info", "Open"),
                    is_enabled=model_data.get("is_enabled", True)
                )
                db.add(entry)
        db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables automatically on startup
    Base.metadata.create_all(bind=engine)
    # Seed model registry entries
    seed_model_registry()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="GenStudio AI — Advanced AI Image & Video Generation Research Platform",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs_url": "/docs",
        "api_v1_prefix": settings.API_V1_STR
    }
