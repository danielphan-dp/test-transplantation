import string
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_url_for_returns_correct_response(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_route(app):
    @app.route('/url-for/<param>')
    def url_for_param(request, param):
        return text(param)

    with pytest.raises(URLBuildError) as e:
        app.url_for("url_for_param")
        assert e.match("Required parameter `param` was not passed to url_for")

def test_url_for_with_extra_params(app):
    @app.route('/url-for/<param>')
    def url_for_param(request, param):
        return text(param)

    fail_kwargs = {'param': 'test', 'extra': 'extra_param'}
    
    with pytest.raises(URLBuildError) as e:
        app.url_for("url_for_param", **fail_kwargs)
        assert e.match("Unexpected keyword argument `extra` passed to url_for")