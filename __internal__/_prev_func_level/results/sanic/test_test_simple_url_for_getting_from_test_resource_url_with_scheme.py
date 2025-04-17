import string
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def simple_app():
    app = Sanic("test_app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_with_valid_letters(simple_app):
    for letter in string.ascii_letters:
        url = simple_app.url_for(letter)
        assert url == f"/{letter}"
        request, response = simple_app.test_client.get(url)
        assert response.status == 200
        assert response.text == letter

def test_url_for_with_invalid_endpoint(simple_app):
    with pytest.raises(URLBuildError) as e:
        simple_app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `non_existent_endpoint` was not found")

def test_url_for_with_missing_params(simple_app):
    url = "/<letter>/"
    
    @simple_app.route(url)
    def fail(request, letter):
        return text(f"Received: {letter}")

    fail_args = list(string.ascii_lowercase)
    fail_args.pop()  # Remove one to simulate missing parameter

    fail_kwargs = {fail_arg: fail_arg for fail_arg in fail_args}

    with pytest.raises(URLBuildError) as e:
        simple_app.url_for("fail", **fail_kwargs)
        assert e.match("Required parameter `z` was not passed to url_for")

def test_url_for_with_query_params(simple_app):
    @simple_app.route('/query')
    def query_handler(request):
        return text(request.args.get('param', 'default'))

    url = simple_app.url_for('query_handler', param='test')
    request, response = simple_app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'test'