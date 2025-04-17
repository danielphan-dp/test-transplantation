import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    return app

def test_url_for_with_valid_route(app):
    expected_url = '/url-for'
    assert app.url_for('url_for_route') == expected_url

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    expected_url = '/url-for?param=value'
    assert app.url_for('url_for_route', param='value') == expected_url

def test_url_for_with_multiple_query_params(app):
    expected_url = '/url-for?param1=value1&param2=value2'
    assert app.url_for('url_for_route', param1='value1', param2='value2') == expected_url

def test_url_for_with_path_param(app):
    @app.route('/<path:path>', name='dynamic_path')
    async def dynamic_handler(request, path):
        return text(path)

    expected_url = '/test/path'
    assert app.url_for('dynamic_path', path='test/path') == expected_url

def test_url_for_with_missing_required_param(app):
    @app.route('/<param>', name='single_param')
    async def single_param_handler(request, param):
        return text(param)

    with pytest.raises(URLBuildError) as e:
        app.url_for('single_param')
        assert str(e.value) == "Required parameter `param` was not passed to url_for"