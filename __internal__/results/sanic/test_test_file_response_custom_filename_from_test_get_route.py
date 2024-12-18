import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ["/", "/nonexistent"])
def test_get_method(app: Sanic, url):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    
    if url == "/":
        assert response.status == 200
        assert response.text == 'I am get method'
    else:
        assert response.status == 404
        assert "Requested URL" in response.text