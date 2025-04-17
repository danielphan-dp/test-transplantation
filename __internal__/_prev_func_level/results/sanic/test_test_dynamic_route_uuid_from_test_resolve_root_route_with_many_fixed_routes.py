def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f"Query param: {request.args.get('param')}")

    app.add_route(DummyView().get, "/get_with_query")

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_empty_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f"Query param: {request.args.get('param', 'default')}")

    app.add_route(DummyView().get, "/get_with_empty_query")

    request, response = app.test_client.get("/get_with_empty_query")
    assert response.text == "Query param: default"
    assert response.status == 200

def test_get_method_with_headers(app):
    class DummyView:
        def get(self, request):
            return text(f"Header value: {request.headers.get('X-Custom-Header')}")

    app.add_route(DummyView().get, "/get_with_headers")

    request, response = app.test_client.get("/get_with_headers", headers={"X-Custom-Header": "HeaderValue"})
    assert response.text == "Header value: HeaderValue"
    assert response.status == 200

def test_get_method_with_invalid_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text