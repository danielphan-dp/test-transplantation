def test_get_method(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Forwarded-For": "192.168.1.1"})
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Real-IP": "192.168.1.2"})
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Forwarded-For": ""})
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Real-IP": "", "X-Forwarded-For": "invalid_ip"})
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Forwarded-For": "127.0.0.1, 127.0.1.1"})
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Forwarded-For": "127.0.0.1, , 127.0.1.2"})
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.get("/get", headers={"X-Forwarded-For": ", 127.0.2.2, , 127.0.0.1"})
    assert response.text == "I am get method"
    assert response.status == 200