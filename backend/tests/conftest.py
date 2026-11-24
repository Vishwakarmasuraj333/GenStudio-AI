import os
import sys
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.database import Base
from app.api.deps import get_db
from app.main import app, seed_model_registry
from app.core.security import hash_password, create_access_token
from app.models.user import User, UserRole

TEST_DB_FILE = backend_dir / "test_genstudio.db"
SQLALCHEMY_TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    settings.PROVIDER_MODE = "test"
    if TEST_DB_FILE.exists():
        try:
            TEST_DB_FILE.unlink()
        except Exception:
            pass
    Base.metadata.create_all(bind=engine)
    # Seed model registry in test DB
    db = TestingSessionLocal()
    from app.providers.registry import CURATED_MODELS
    from app.models.model_registry import ModelRegistryEntry
    for m in CURATED_MODELS:
        entry = ModelRegistryEntry(
            provider=m["provider"],
            model_id=m["model_id"],
            display_name=m["display_name"],
            version=m.get("version"),
            task_types=m["task_types"],
            max_resolution=m.get("max_resolution", "1024x1024"),
            supported_aspect_ratios=m.get("supported_aspect_ratios", []),
            capabilities_json=m.get("capabilities_json", {}),
            pricing_json=m.get("pricing_json", {}),
            license_info=m.get("license_info", "Open"),
            is_enabled=m.get("is_enabled", True)
        )
        db.add(entry)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)
    if TEST_DB_FILE.exists():
        try:
            TEST_DB_FILE.unlink()
        except Exception:
            pass

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client():
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db) -> User:
    user = db.query(User).filter(User.email == "researcher@genstudio.ai").first()
    if not user:
        user = User(
            email="researcher@genstudio.ai",
            hashed_password=hash_password("SecurePass123!"),
            full_name="AI Researcher",
            role=UserRole.USER,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@pytest.fixture
def test_admin(db) -> User:
    admin = db.query(User).filter(User.email == "admin@genstudio.ai").first()
    if not admin:
        admin = User(
            email="admin@genstudio.ai",
            hashed_password=hash_password("AdminPass123!"),
            full_name="Lead Architect",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    return admin

@pytest.fixture
def user_auth_headers(test_user) -> dict:
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_auth_headers(test_admin) -> dict:
    token = create_access_token(test_admin.id)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def second_test_user(db) -> User:
    user = db.query(User).filter(User.email == "other_user@genstudio.ai").first()
    if not user:
        user = User(
            email="other_user@genstudio.ai",
            hashed_password=hash_password("OtherPass123!"),
            full_name="Other Researcher",
            role=UserRole.USER,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@pytest.fixture
def second_user_auth_headers(second_test_user) -> dict:
    token = create_access_token(second_test_user.id)
    return {"Authorization": f"Bearer {token}"}
