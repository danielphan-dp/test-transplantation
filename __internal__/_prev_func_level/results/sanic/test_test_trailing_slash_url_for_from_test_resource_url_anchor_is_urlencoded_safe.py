import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.parametrize('path,strict,expected', [
    ('/url-for', False, '/url-for'),
    ('/url-for/', False, '/url-for'),
    ('/url-for', True, '/url-for'),
    ('/url-for/', True, '/url-for/'),
])
def test_url_for(app, path, strict, expected):
    @app.route(path, strict_slashes=strict)
    def handler(request):
        return text('url-for')

    url = app.url_for("handler")
    assert url == expected

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'