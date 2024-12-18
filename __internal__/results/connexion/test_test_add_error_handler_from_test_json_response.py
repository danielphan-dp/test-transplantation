import json
import pytest
from connexion.lifecycle import ConnexionRequest, ConnexionResponse

def test_get_method_with_kwargs(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")
    app_client = app.test_client()

    response = app_client.get("/get_method", query_string={"key": "value"})
    assert response.status_code == 200
    assert response.json == {"key": "value", "name": "get"}

def test_get_method_without_kwargs(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")
    app_client = app.test_client()

    response = app_client.get("/get_method")
    assert response.status_code == 200
    assert response.json == [{"name": "get"}]

def test_get_method_with_empty_kwargs(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")
    app_client = app.test_client()

    response = app_client.get("/get_method", query_string={})
    assert response.status_code == 200
    assert response.json == [{"name": "get"}]