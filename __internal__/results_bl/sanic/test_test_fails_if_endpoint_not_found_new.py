import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

app = Sanic("app")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_endpoint_exists():
    request = app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_with_invalid_endpoint():
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_empty_string():
    with pytest.raises(URLBuildError) as e:
        app.url_for("")
        e.match("Endpoint with name `app.` was not found")

def test_url_for_with_special_characters():
    with pytest.raises(URLBuildError) as e:
        app.url_for("!@#$%^&*()")
        e.match("Endpoint with name `app.!@#$%^&*()` was not found")