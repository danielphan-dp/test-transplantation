def test_request_middleware_run_count(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    app.test_client.get("/")
    assert request_middleware_run_count == 1

def test_request_middleware_multiple_requests(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    app.test_client.get("/")
    app.test_client.get("/")
    assert request_middleware_run_count == 2

def test_request_middleware_with_payload(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.post("/data", ignore_body=False)
    async def handler(request):
        return text("Received")

    payload = {"key": "value"}
    headers = {"content-type": "application/json"}
    data = json.dumps(payload)
    request, response = app.test_client.request(
        "/data", http_method="post", data=data, headers=headers
    )

    assert request.body == data.encode("utf-8")
    assert request.json.get("key") == "value"
    assert response.body == b"Received"
    assert request_middleware_run_count == 1

def test_request_middleware_no_request(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    assert request_middleware_run_count == 0

def test_request_middleware_with_error_handling(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/error")
    async def handler(request):
        raise Exception("Test Error")

    response = app.test_client.get("/error")
    assert response.status_code == 500
    assert request_middleware_run_count == 1