import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for('url_for')
    assert url == '/url-for'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_missing_param(app):
    @app.route('/url-for/<param>')
    def url_for_with_param(request, param):
        return text(param)

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_param')
        e.match("Required parameter `param` was not passed to url_for")

def test_url_for_with_invalid_param_type(app):
    @app.route('/url-for/<int:param>')
    def url_for_with_int_param(request, param):
        return text(param)

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_int_param', param='not-an-int')
        e.match('Value "not-an-int" for parameter `param` does not match pattern for type `int`')

def test_url_for_with_extra_params(app):
    @app.route('/url-for/<param>')
    def url_for_with_extra_param(request, param):
        return text(param)

    url = app.url_for('url_for_with_extra_param', param='test', extra='extra')
    assert url == '/url-for/test'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'test'