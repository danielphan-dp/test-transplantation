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

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_missing_parameters(app):
    @app.route('/<param>')
    def handler(request, param):
        return text(param)

    with pytest.raises(URLBuildError) as e:
        app.url_for('handler')  # Missing required parameter
        e.match("Required parameter `param` was not passed to url_for")

def test_url_for_with_extra_parameters(app):
    @app.route('/<param>')
    def handler(request, param):
        return text(param)

    url = app.url_for('handler', param='test', extra_param='extra')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'test'

def test_url_for_with_special_characters(app):
    @app.route('/<param>')
    def handler(request, param):
        return text(param)

    url = app.url_for('handler', param='test@123')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'test@123'