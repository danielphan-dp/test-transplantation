import pytest

@pytest.fixture
def app_client():
    from connexion import FlaskApp
    app = FlaskApp(__name__)
    return app.test_client()

def test_get_with_kwargs(app_client):
    response = app_client.get("/v1.0/welcome?name=test")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'name': 'test'}

def test_get_without_kwargs(app_client):
    response = app_client.get("/v1.0/welcome")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app_client):
    response = app_client.get("/v1.0/welcome?name=")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'name': ''}

def test_get_with_multiple_kwargs(app_client):
    response = app_client.get("/v1.0/welcome?name=test&extra=param")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'name': 'test', 'extra': 'param'}