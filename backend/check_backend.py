import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.main import app, seed_model_registry
from app.core.database import Base, engine, SessionLocal
from app.models import User, GenerationJob, ModelRegistryEntry

print("Creating database tables...")
Base.metadata.create_all(bind=engine)

print("Seeding curated model registry...")
seed_model_registry()

db = SessionLocal()
model_count = db.query(ModelRegistryEntry).count()
print(f"Verification successful: {model_count} models loaded in registry.")
db.close()
