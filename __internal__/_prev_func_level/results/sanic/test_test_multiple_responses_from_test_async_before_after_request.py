def test_get_method(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.get("/get")
    async def get_handler(request: Request):
        return text('I am get method')

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get")
        assert response.status == 200
        assert response.text == 'I am get method'
        assert message_in_records(caplog.records, "No errors occurred during the request.")

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/nonexistent")
        assert response.status == 404
        assert "Requested URL /nonexistent not found" in response.text

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get", headers={"Invalid-Header": "value"})
        assert response.status == 200
        assert response.text == 'I am get method'
        assert "Invalid-Header" not in response.headers

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get", data={"key": "value"})
        assert response.status == 200
        assert response.text == 'I am get method'