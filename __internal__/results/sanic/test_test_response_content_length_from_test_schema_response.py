def test_get_method_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/get")

    request, response = app.test_client.get("/get")
    assert response.status == 200, response.text
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text(f"Query param received: {request.args.get('param')}")

    app.add_route(DummyView.as_view(), "/get_with_query")

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.status == 200, response.text
    assert response.text == "Query param received: test"

def test_get_method_with_no_query_params(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("No query param received")

    app.add_route(DummyView.as_view(), "/get_no_query")

    request, response = app.test_client.get("/get_no_query")
    assert response.status == 200, response.text
    assert response.text == "No query param received"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404, response.text
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("Headers received", headers={"Custom-Header": "Value"})

    app.add_route(DummyView.as_view(), "/get_with_headers")

    request, response = app.test_client.get("/get_with_headers")
    assert response.status == 200, response.text
    assert response.text == "Headers received"
    assert response.headers.get("Custom-Header") == "Value"