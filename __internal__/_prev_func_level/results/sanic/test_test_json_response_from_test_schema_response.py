def test_get_method_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            name = request.args.get('name', 'Guest')
            return text(f'I am get method, {name}')

    app.add_route(DummyView.as_view(), "/greet")

    request, response = app.test_client.get("/greet?name=John")
    assert response.status == 200
    assert response.text == "I am get method, John"

    request, response = app.test_client.get("/greet")
    assert response.status == 200
    assert response.text == "I am get method, Guest"