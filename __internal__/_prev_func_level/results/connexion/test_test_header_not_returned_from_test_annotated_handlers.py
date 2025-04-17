import json
import pytest

def test_json_method(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.post("/v1.0/goodday/json", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"key": "value"}

    response = app_client.post("/v1.0/goodday/json", data="invalid json", content_type='application/json')
    assert response.status_code == 400
    data = response.json()
    assert data["type"] == "about:blank"
    assert data["title"] == "Bad Request"
    assert data["detail"] == "Invalid JSON data"
    assert data["status"] == 400

    response = app_client.post("/v1.0/goodday/json", data=json.dumps({"key": None}), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"key": None}