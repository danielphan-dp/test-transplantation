import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url, expected_text, expected_status', [
    ("/", "I am get method", 200),
    ("/nonexistent", "Not Found", 404),
])
def test_get_method(app: Sanic, url, expected_text, expected_status):
    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    assert response.status == expected_status
    if expected_status == 200:
        assert response.text == expected_text
    else:
        assert "Not Found" in response.text