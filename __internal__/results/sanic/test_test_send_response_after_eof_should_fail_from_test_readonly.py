def test_get_method_response(app):
    @app.get("/test")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == "I am get method", f"Expected response text 'I am get method', got {response.text}"

def test_get_method_with_query_params(app):
    @app.get("/test")
    async def handler(request):
        name = request.args.get('name', 'World')
        return text(f'I am get method, hello {name}')

    request, response = app.test_client.get("/test?name=Alice")
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == "I am get method, hello Alice", f"Expected response text 'I am get method, hello Alice', got {response.text}"

def test_get_method_with_no_query_params(app):
    @app.get("/test")
    async def handler(request):
        return text('I am get method, hello World')

    request, response = app.test_client.get("/test")
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == "I am get method, hello World", f"Expected response text 'I am get method, hello World', got {response.text}"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
    assert "Requested URL /invalid_route not found" in response.text, f"Expected error message in response, got {response.text}"