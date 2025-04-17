def test_get_method(app: Sanic, caplog: LogCaptureFixture):
    @app.get("/get")
    async def get_handler(request: Request):
        return text('I am get method')

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get")
        assert response.status == 200
        assert response.text == "I am get method"
        assert "I am get method" in response.text

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
        assert response.status == 200
        assert response.text == "I am get method"
        assert response.headers.get("Custom-Header") is None

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get", data={"key": "value"})
        assert response.status == 200
        assert response.text == "I am get method"