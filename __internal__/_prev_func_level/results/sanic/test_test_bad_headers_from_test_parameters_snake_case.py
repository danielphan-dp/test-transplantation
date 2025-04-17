def test_get_method(app, port):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app, port):
    @app.get("/query")
    async def handler(request):
        return text("Query received")

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/query?param=value")
    
    assert response.status == 200
    assert response.text == "Query received"

def test_get_method_with_invalid_route(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/invalid")
    
    assert response.status == 404

def test_get_method_with_large_request(app, port):
    @app.get("/large")
    async def handler(request):
        return text("Large request handled")

    client = ReusableClient(app, port=port)
    large_headers = {"X-Large-Header": "x" * 10_000}

    with client:
        _, response = client.get("/large", headers=large_headers)
    
    assert response.status == 413

def test_get_method_with_different_content_type(app, port):
    @app.get("/content")
    async def handler(request):
        return text("Content type test")

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/content", headers={"Content-Type": "text/plain"})
    
    assert response.status == 200
    assert response.text == "Content type test"