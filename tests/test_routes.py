import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to demo-devops-project"}


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_info(client):
    response = client.get("/api/info")

    assert response.status_code == 200
    assert response.get_json() == {
        "name": "demo-devops-project",
        "version": "0.1.0",
    }
