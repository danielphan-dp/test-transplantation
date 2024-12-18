def test_get_method(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.get("/get")
    async def get_handler(request: Request):
        return text('I am get method')

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get")
        assert response.status == 200
        assert response.text == "I am get method"
        assert message_in_records(caplog.records, "No errors logged during the request.")

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
        assert response.status == 200
        assert response.text == "I am get method"
        assert "X-Custom-Header" in response.headers

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get", data={"key": "value"})
        assert response.status == 200
        assert response.text == "I am get method"
        assert message_in_records(caplog.records, "No errors logged during the request.")