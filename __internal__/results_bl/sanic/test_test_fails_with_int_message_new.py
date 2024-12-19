import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_with_valid_request(app):
    request = app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
    expected_error = r'No route found for endpoint `non_existent_route`'
    assert str(e.value) == expected_error

def test_url_for_with_missing_parameters(app):
    @app.route('/test/<foo:int>')
    def test_route(request, foo):
        return text(f'foo: {foo}')

    with pytest.raises(URLBuildError) as e:
        app.url_for("test_route")
    expected_error = r'Missing required parameters for endpoint `test_route`'
    assert str(e.value) == expected_error

def test_url_for_with_non_integer_parameter(app):
    @app.route('/test/<foo:int>')
    def test_route(request, foo):
        return text(f'foo: {foo}')

    failing_kwargs = {"foo": "not_int"}
    with pytest.raises(URLBuildError) as e:
        app.url_for("test_route", **failing_kwargs)
    expected_error = (
        r'Value "not_int" for parameter `foo` '
        r"does not match pattern for type `int`: ^-?\d+$"
    )
    assert str(e.value) == expected_error