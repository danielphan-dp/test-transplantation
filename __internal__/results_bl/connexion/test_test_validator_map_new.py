import json
import pytest
from connexion import App

def test_post_method(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()

    # Test with valid input
    res = app_client.post("/v1.0/minlength", json={"foo": "bar"})
    assert res.status_code == 201
    assert res.json == {'name': 'post', 'foo': 'bar'}

    # Test with empty input
    res = app_client.post("/v1.0/minlength", json={})
    assert res.status_code == 201
    assert res.json == {'name': 'post'}

    # Test with None input
    res = app_client.post("/v1.0/minlength", json=None)
    assert res.status_code == 201
    assert res.json == {'name': 'post'}

    # Test with unexpected data type
    res = app_client.post("/v1.0/minlength", json={"foo": 123})
    assert res.status_code == 201
    assert res.json == {'name': 'post', 'foo': 123}

    # Test with additional unexpected key
    res = app_client.post("/v1.0/minlength", json={"foo": "bar", "extra": "value"})
    assert res.status_code == 201
    assert res.json == {'name': 'post', 'foo': 'bar', 'extra': 'value'}