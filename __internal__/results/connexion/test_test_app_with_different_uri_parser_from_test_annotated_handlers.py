import json
import pytest
from connexion import App
from connexion.uri_parsing import FirstValueURIParser

@pytest.fixture
def app(simple_api_spec_dir):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
        uri_parser_class=FirstValueURIParser,
    )
    app.add_api("swagger.yaml")
    return app

def test_json_method_with_valid_input(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=x,y,z")
    assert resp.status_code == 200
    j = resp.json()
    assert j == ["x", "y", "z"]

def test_json_method_with_empty_input(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=")
    assert resp.status_code == 200
    j = resp.json()
    assert j == []

def test_json_method_with_invalid_input(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=123,456")
    assert resp.status_code == 200
    j = resp.json()
    assert j == ["123", "456"]

def test_json_method_with_special_characters(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=hello%20world,foo%20bar")
    assert resp.status_code == 200
    j = resp.json()
    assert j == ["hello world", "foo bar"]