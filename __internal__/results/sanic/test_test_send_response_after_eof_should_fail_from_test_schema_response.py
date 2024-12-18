def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status_code == 200, response.text
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    @app.get("/greet")
    async def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status_code == 200, response.text
    assert response.text == "Hello, Alice!"

def test_get_method_with_no_query_params(app):
    @app.get("/greet")
    async def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet")
    assert response.status_code == 200, response.text
    assert response.text == "Hello, Guest!"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status_code == 404, response.text
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method", headers={"X-Custom-Header": "Value"})

    request, response = app.test_client.get("/")
    assert response.status_code == 200, response.text
    assert response.headers["X-Custom-Header"] == "Value"