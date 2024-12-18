import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_basic_functionality(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for('url_for')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_parameter(app):
    @app.route('/url-for/<some_number:float>')
    def url_for_with_param(request, some_number):
        return text(f'url-for with number: {some_number}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_param', some_number='invalid')
        e.match('Value "invalid" for parameter `some_number` does not match pattern for type `float`')

def test_url_for_with_missing_parameter(app):
    @app.route('/url-for/<some_number:float>')
    def url_for_with_param(request, some_number):
        return text(f'url-for with number: {some_number}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_param')
        e.match('Required parameter `some_number` was not passed to url_for')

def test_url_for_with_extra_parameters(app):
    @app.route('/url-for/<some_number:float>')
    def url_for_with_param(request, some_number):
        return text(f'url-for with number: {some_number}')

    url = app.url_for('url_for_with_param', some_number=3.14, extra_param='extra')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for with number: 3.14'