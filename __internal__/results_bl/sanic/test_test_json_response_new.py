def test_get_method(json_app):
    from sanic.response import text

    request, response = json_app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    request, response = json_app.test_client.get("/nonexistent")
    assert response.status == 404

    request, response = json_app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'