def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    response = app.test_client.get("/get")

    assert response.text == "I am get method"
    assert len(results) == 1
    assert type(results[0]) is Request

def test_get_method_with_custom_header(app):
    class DummyView:
        def get(self, request):
            return text('I am get method', headers={'X-Custom-Header': 'value'})

    app.add_route(DummyView().get, "/get")

    response = app.test_client.get("/get")

    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'