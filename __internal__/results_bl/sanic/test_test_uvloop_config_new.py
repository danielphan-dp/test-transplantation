import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/test", "ok"),
    ("/nonexistent", "Not Found"),
])
def test_get_method(app: Sanic, request_path, expected_response):
    @app.get("/test", name="test")
    def handler(request):
        return text("ok")

    response = app.test_client.get(request_path)
    
    if request_path == "/test":
        assert response.text == expected_response
    else:
        assert response.status == 404