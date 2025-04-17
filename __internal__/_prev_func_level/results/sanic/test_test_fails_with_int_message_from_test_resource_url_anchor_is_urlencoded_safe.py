import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/valid-url')
    def valid_route(request):
        return text('this should pass')

    url = app.url_for('valid_route')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'this should pass'

def test_url_for_with_missing_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_route')
    assert str(e.value) == "Endpoint with name `app.non_existent_route` was not found"

def test_url_for_with_invalid_param_type(app):
    @app.route('/param/<int:foo>')
    def param_route(request, foo):
        return text(f'foo is {foo}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('param_route', foo='not_int')
    expected_error = (
        r'Value "not_int" for parameter `foo` '
        r"does not match pattern for type `int`: ^-?\d+$"
    )
    assert str(e.value) == expected_error

def test_url_for_with_missing_required_param(app):
    @app.route('/param/<str:foo>')
    def param_route(request, foo):
        return text(f'foo is {foo}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('param_route')
    assert str(e.value) == "Required parameter `foo` was not passed to url_for"

def test_url_for_with_extra_params(app):
    @app.route('/extra/<str:foo>')
    def extra_route(request, foo):
        return text(f'foo is {foo}')

    url = app.url_for('extra_route', foo='test', extra_param='extra')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'foo is test'