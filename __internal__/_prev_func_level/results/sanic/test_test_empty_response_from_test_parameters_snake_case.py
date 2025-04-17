def test_get_method_response(app):
    @app.get("/get-test")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get-test")
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'

def test_get_method_with_query_params(app):
    @app.get("/get-test-query")
    def handler(request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/get-test-query?name=Alice")
    assert response.status_code == 200
    assert response.body == b'Hello, Alice!'

def test_get_method_with_no_query_params(app):
    @app.get("/get-test-query-default")
    def handler(request):
        return text('Hello, World!')

    request, response = app.test_client.get("/get-test-query-default")
    assert response.status_code == 200
    assert response.body == b'Hello, World!'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status_code == 404
    assert b"Requested URL /invalid-route not found" in response.body

def test_get_method_with_custom_header(app):
    @app.get("/get-test-header")
    def handler(request):
        return text('Header received', headers={'X-Custom-Header': 'Value'})

    request, response = app.test_client.get("/get-test-header")
    assert response.status_code == 200
    assert response.headers['X-Custom-Header'] == 'Value'