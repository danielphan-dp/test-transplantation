def test_get_method_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")
    assert response.status_code == 200
    assert response.text == "I am get method"
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_with_query_params(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            name = request.args.get('name', 'World')
            return text(f'Hello, {name}!')

    app.add_route(DummyView.as_view(), "/greet")

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status_code == 200
    assert response.text == "Hello, Alice!"

    request, response = app.test_client.get("/greet")
    assert response.status_code == 200
    assert response.text == "Hello, World!"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status_code == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_content_length(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")
    assert response.headers.get("Content-Length") == "17"  # Length of "I am get method"