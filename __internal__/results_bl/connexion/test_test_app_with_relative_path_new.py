import json
import unittest.mock
import pytest
import yaml
from connexion.App import App
from connexion.exceptions.InvalidSpecification import InvalidSpecification

def test_get_with_kwargs(simple_api_spec_dir, spec):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
    )
    app.add_api(spec)

    app_client = app.test_client()
    response = app_client.get("/v1.0/get", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert json.loads(response.data) == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(simple_api_spec_dir, spec):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
    )
    app.add_api(spec)

    app_client = app.test_client()
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert json.loads(response.data) == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_api_spec_dir, spec):
    app = App(
        __name__,
        specification_dir=".." / simple_api_spec_dir.relative_to(TEST_FOLDER),
    )
    app.add_api(spec)

    app_client = app.test_client()
    response = app_client.get("/v1.0/get", query_string={})
    assert response.status_code == 200
    assert json.loads(response.data) == [{'name': 'get'}]