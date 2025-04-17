def test_get_method_response(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert len(results) == 2
    assert isinstance(results[0], Request)
    assert isinstance(results[1], HTTPResponse)

def test_get_method_with_custom_header(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    response = app.test_client.get("/get")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'