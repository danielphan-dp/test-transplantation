import json
import pytest
from connexion import App
from connexion.uri_parsing import FirstValueURIParser

def test_json_method_with_valid_data(simple_api_spec_dir):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
        uri_parser_class=FirstValueURIParser,
    )
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=a,b,c&items=d,e,f")
    assert resp.status_code == 200
    j = resp.json()
    assert j == ["a", "b", "c"]

def test_json_method_with_empty_data(simple_api_spec_dir):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
        uri_parser_class=FirstValueURIParser,
    )
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=")
    assert resp.status_code == 200
    j = resp.json()
    assert j == []

def test_json_method_with_invalid_json(simple_api_spec_dir):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
        uri_parser_class=FirstValueURIParser,
    )
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=invalid_json")
    assert resp.status_code == 400
    j = resp.json()
    assert "error" in j

def test_json_method_with_special_characters(simple_api_spec_dir):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
        uri_parser_class=FirstValueURIParser,
    )
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=%40%23%24%25")
    assert resp.status_code == 200
    j = resp.json()
    assert j == ["@#$%"]