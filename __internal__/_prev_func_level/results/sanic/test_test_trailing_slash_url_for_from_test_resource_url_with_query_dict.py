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

def test_fails_if_endpoint_not_found(app):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_handler")
        assert "Endpoint with name `non_existent_handler` was not found" in str(e.value)

def test_url_for_with_query_params(app):
    @app.route('/url-for')
    def handler(request):
        return text('url-for')

    url = app.url_for("handler", param1="value1", param2="value2")
    assert url == '/url-for?param1=value1&param2=value2'

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'