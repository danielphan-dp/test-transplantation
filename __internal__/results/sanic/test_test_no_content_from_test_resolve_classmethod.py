def test_get_method(json_app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    json_app.add_route(DummyView().get, "/get-method")

    request, response = json_app.test_client.get("/get-method")
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
    
def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(json_app):
    class DummyView:
        def get(self, request):
            return text(f'I am get method with param: {request.args.get("param")}')

    json_app.add_route(DummyView().get, "/get-method-with-param")

    request, response = json_app.test_client.get("/get-method-with-param?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'