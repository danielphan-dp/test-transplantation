def test_get_method(app, port):
    @app.get("/get")
    async def handler(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_get_method_with_query_params(app, port):
    @app.get("/get")
    async def handler(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.get("/get?param=test")

    assert response.status == 200
    assert response.text == "I am get method with param: test"

def test_get_method_with_empty_response(app, port):
    @app.get("/get_empty")
    async def handler(request):
        return text("")

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.get("/get_empty")

    assert response.status == 200
    assert response.text == ""

def test_get_method_with_large_response(app, port):
    @app.get("/get_large")
    async def handler(request):
        return text("A" * 10_000)

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.get("/get_large")

    assert response.status == 200
    assert response.text == "A" * 10_000

def test_get_method_with_bad_request(app, port):
    @app.get("/get")
    async def handler(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)
    bad_headers = {"bad": "bad" * 5_000}

    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get", headers=bad_headers)

    assert response1.status == 200
    assert response2.status == 413
    assert response1.headers["x-request-id"] != response2.headers["x-request-id"]