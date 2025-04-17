import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_post_method_with_kwargs(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    # Test with no kwargs
    res = app_client.post("/v1.0/post", json={})
    assert res.status_code == 201
    assert res.json() == {'name': 'post'}

    # Test with additional kwargs
    res = app_client.post("/v1.0/post", json={'extra_param': 'value'})
    assert res.status_code == 201
    assert res.json() == {'extra_param': 'value', 'name': 'post'}

    # Test with multiple kwargs
    res = app_client.post("/v1.0/post", json={'param1': 'value1', 'param2': 'value2'})
    assert res.status_code == 201
    assert res.json() == {'param1': 'value1', 'param2': 'value2', 'name': 'post'}

    # Test with empty request body
    res = app_client.post("/v1.0/post", json=None)
    assert res.status_code == 201
    assert res.json() == {'name': 'post'}