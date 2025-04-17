import pytest

def test_get_with_kwargs(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/get?param1=value1&param2=value2"
    resp = app_client.get(url, headers=headers)
    assert resp.status_code == 200
    response = resp.json()
    assert response["name"] == "get"
    assert response["param1"] == "value1"
    assert response["param2"] == "value2"

def test_get_without_kwargs(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/get"
    resp = app_client.get(url, headers=headers)
    assert resp.status_code == 200
    response = resp.json()
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["name"] == "get"