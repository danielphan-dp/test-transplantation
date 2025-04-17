import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route_name():
    app = Sanic("app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route')
    assert url == '/url-for'

def test_url_for_with_invalid_route_name():
    app = Sanic("app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_parameters():
    app = Sanic("app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route', param1='value1', param2='value2')
    assert url == '/url-for?param1=value1&param2=value2'

def test_url_for_with_edge_case_empty_parameters():
    app = Sanic("app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route', param1='', param2='')
    assert url == '/url-for?param1=&param2='

def test_url_for_with_special_characters():
    app = Sanic("app")

    @app.route('/url-for/<name>', name='url_for_route')
    def url_for_handler(request, name):
        return text(f'Hello, {name}')

    url = app.url_for('url_for_route', name='John Doe')
    assert url == '/url-for/John%20Doe'