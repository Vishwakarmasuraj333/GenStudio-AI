import pytest

def test_create_project(client, user_auth_headers):
    response = client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={
            "name": "Neural Art Thesis",
            "description": "Experiments with FLUX.1 architecture"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Neural Art Thesis"
    assert "id" in data

def test_list_projects(client, user_auth_headers):
    # Create project first
    client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={"name": "Project A"}
    )
    response = client.get("/api/v1/projects/", headers=user_auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_project_detail(client, user_auth_headers):
    create_res = client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={"name": "Project B"}
    )
    p_id = create_res.json()["id"]

    get_res = client.get(f"/api/v1/projects/{p_id}", headers=user_auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Project B"

def test_delete_project(client, user_auth_headers):
    create_res = client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={"name": "Project To Delete"}
    )
    p_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/projects/{p_id}", headers=user_auth_headers)
    assert del_res.status_code == 204

    # Verify deleted
    get_res = client.get(f"/api/v1/projects/{p_id}", headers=user_auth_headers)
    assert get_res.status_code == 404

def test_user_isolation_cannot_read_other_user_project(client, user_auth_headers, second_user_auth_headers):
    # User 1 creates project
    create_res = client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={"name": "User 1 Private Project"}
    )
    p_id = create_res.json()["id"]

    # User 2 tries to read it
    get_res = client.get(f"/api/v1/projects/{p_id}", headers=second_user_auth_headers)
    assert get_res.status_code == 404

def test_user_isolation_cannot_update_other_user_project(client, user_auth_headers, second_user_auth_headers):
    create_res = client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={"name": "User 1 Protected Project"}
    )
    p_id = create_res.json()["id"]

    # User 2 tries to update it
    update_res = client.put(
        f"/api/v1/projects/{p_id}",
        headers=second_user_auth_headers,
        json={"name": "Hacked Name"}
    )
    assert update_res.status_code == 404

def test_user_isolation_cannot_delete_other_user_project(client, user_auth_headers, second_user_auth_headers):
    create_res = client.post(
        "/api/v1/projects/",
        headers=user_auth_headers,
        json={"name": "User 1 Safe Project"}
    )
    p_id = create_res.json()["id"]

    # User 2 tries to delete it
    del_res = client.delete(f"/api/v1/projects/{p_id}", headers=second_user_auth_headers)
    assert del_res.status_code == 404

    # Verify project still exists for User 1
    get_res = client.get(f"/api/v1/projects/{p_id}", headers=user_auth_headers)
    assert get_res.status_code == 200
