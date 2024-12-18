def test_get_method_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")

    assert response.text == 'I am get method'
    assert response.status == 200
    assert isinstance(response, HTTPResponse)

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    @app.middleware("response")
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")

    assert response.text == 'I am get method'
    assert type(results[0]) is Request
    assert type(results[1]) is Request
    assert isinstance(results[2], HTTPResponse)
    assert type(results[3]) is Request
    assert isinstance(results[4], HTTPResponse)

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_invalid_method(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

def test_get_method_with_custom_headers(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method', headers={'X-Custom-Header': 'Value'})

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")
    assert response.headers['X-Custom-Header'] == 'Value'