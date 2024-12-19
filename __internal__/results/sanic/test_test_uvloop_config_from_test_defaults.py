import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('use', (False, True))
def test_get_method(app: Sanic, monkeypatch, use):
    @app.get("/get_test", name="get_test")
    def handler(request):
        return text("I am get method")

    app.config["USE_UVLOOP"] = use
    request, response = app.test_client.get("/get_test")

    assert response.status == 200
    assert response.text == "I am get method"

    if OS_IS_WINDOWS:
        assert not app.config["USE_UVLOOP"]
    else:
        assert app.config["USE_UVLOOP"] == use

    # Additional assertions to check request properties
    assert request.method == 'GET'
    assert request.path == '/get_test'
    assert request.url == 'http://localhost/get_test'  # Adjust based on actual host
    assert request.headers.get('Content-Type') == 'text/plain; charset=utf-8'