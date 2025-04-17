def test_get_method(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am get method'
    assert response1.json is None
    assert response2.json is None

def test_get_method_with_different_requests(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get?param=value")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am get method'
    assert response1.json is None
    assert response2.json is None

def test_get_method_no_request_body(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.json is None

def test_get_method_with_invalid_route(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/invalid_route")

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text