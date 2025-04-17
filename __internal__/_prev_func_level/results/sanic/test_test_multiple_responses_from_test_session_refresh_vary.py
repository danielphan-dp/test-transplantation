def test_get_method(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/get")
        assert response.status == 200
        assert response.text == "I am get method"
        assert message_in_records(caplog.records, "No errors logged during the request.")

    with caplog.at_level(ERROR):
        request, response = app.test_client.get("/nonexistent")
        assert response.status == 404
        assert "404 — Not Found" in response.text
        assert message_in_records(caplog.records, "Requested URL /nonexistent not found")