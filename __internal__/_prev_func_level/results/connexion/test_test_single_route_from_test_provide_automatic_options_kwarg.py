import json
import pytest
from connexion import App

def test_post_method(app):
    app_client = app.test_client()

    # Test valid post request
    response = app_client.post("/single2", json={"key": "value"})
    assert response.status_code == 201
    assert response.json == {"key": "value", "name": "post"}

    # Test post request with no body
    response = app_client.post("/single2")
    assert response.status_code == 201
    assert response.json == {"name": "post"}

    # Test post request to an invalid route
    response = app_client.post("/invalid_route")
    assert response.status_code == 404

    # Test post request with unexpected data type
    response = app_client.post("/single2", data="string_instead_of_json")
    assert response.status_code == 400

    # Test post request with additional unexpected fields
    response = app_client.post("/single2", json={"key": "value", "extra": "unexpected"})
    assert response.status_code == 201
    assert response.json == {"key": "value", "extra": "unexpected", "name": "post"}