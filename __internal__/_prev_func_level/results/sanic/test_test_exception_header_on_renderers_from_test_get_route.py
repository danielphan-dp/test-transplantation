import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url, expected_text', [
    ("/", "I am get method"),
    ("/nonexistent", "Not Found"),
])
def test_get_method(app: Sanic, url, expected_text):
    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    
    if url == "/":
        assert response.status == 200
        assert response.text == expected_text
    else:
        assert response.status == 404
        assert "Not Found" in response.text