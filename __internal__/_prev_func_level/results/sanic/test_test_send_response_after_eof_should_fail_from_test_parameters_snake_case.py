def test_get_method_response(app):
    @app.get("/test-get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")
    assert response.status_code == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status_code == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test-get-query")
    async def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f'I am get method, {name}')

    request, response = app.test_client.get("/test-get-query?name=John")
    assert response.status_code == 200
    assert response.text == 'I am get method, John'

def test_get_method_with_no_query_params(app):
    @app.get("/test-get-query-default")
    async def handler(request):
        return text('I am get method, Guest')

    request, response = app.test_client.get("/test-get-query-default")
    assert response.status_code == 200
    assert response.text == 'I am get method, Guest'