def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    test_client = SanicTestClient(app, port=None)

    request, response = test_client.get("/get")
    assert response.text == "I am get method"

    request, response = test_client.post("/get")
    assert response.status == 405

    request, response = test_client.put("/get")
    assert response.status == 405

    request, response = test_client.delete("/get")
    assert response.status == 405

    request, response = test_client.options("/get")
    assert response.status == 200

    request, response = test_client.head("/get")
    assert response.status == 200
    assert response.text == ""