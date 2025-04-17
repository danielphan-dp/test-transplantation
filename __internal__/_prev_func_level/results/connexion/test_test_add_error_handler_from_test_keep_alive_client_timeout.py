import json
import pytest
from connexion import App

@pytest.fixture
def app_class():
    return App

@pytest.fixture
def simple_api_spec_dir():
    return "path/to/spec"

def test_get_with_kwargs(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")
    app_client = app.test_client()

    response = app_client.get("/endpoint", query_string={"key": "value"})
    assert response.status_code == 200
    assert response.json() == {"key": "value", "name": "get"}

def test_get_without_kwargs(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")
    app_client = app.test_client()

    response = app_client.get("/endpoint")
    assert response.status_code == 200
    assert response.json() == [{"name": "get"}]

def test_get_with_empty_kwargs(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")
    app_client = app.test_client()

    response = app_client.get("/endpoint", query_string={})
    assert response.status_code == 200
    assert response.json() == [{"name": "get"}]