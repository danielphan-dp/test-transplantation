def test_get_method_response(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert type(results[0]) is Request

def test_get_method_with_custom_header(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get")
    assert response.headers["X-Custom-Header"] == "value"