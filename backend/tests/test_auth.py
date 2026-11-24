import uuid
import pytest

def test_register_new_user(client):
    unique_email = f"student_{uuid.uuid4().hex[:8]}@univ.edu"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "password": "Password123!",
            "full_name": "Graduate Student"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == unique_email

def test_register_duplicate_email_fails(client, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "AnotherPassword123!",
            "full_name": "Imposter"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_success(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "SecurePass123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "WrongPassword!"
        }
    )
    assert response.status_code == 401

def test_get_current_user_me(client, user_auth_headers, test_user):
    response = client.get("/api/v1/auth/me", headers=user_auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email

def test_unauthorized_access_rejected(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_rbac_user_cannot_access_admin(client, user_auth_headers):
    response = client.get("/api/v1/admin/users", headers=user_auth_headers)
    assert response.status_code == 403

def test_rbac_user_cannot_access_audit_logs(client, user_auth_headers):
    response = client.get("/api/v1/admin/audit-logs", headers=user_auth_headers)
    assert response.status_code == 403

def test_rbac_admin_can_access_audit_logs(client, admin_auth_headers):
    response = client.get("/api/v1/admin/audit-logs", headers=admin_auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_health_check_reports_honest_provider_mode(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "provider_mode" in data
    assert "providers_configured" in data
    assert "huggingface" in data["providers_configured"]
    assert "required_env_vars" in data
