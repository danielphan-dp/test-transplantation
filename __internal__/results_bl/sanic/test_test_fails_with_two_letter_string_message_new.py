import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_valid_request(app):
    request = app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        e.match('No route found for non_existent_route')

def test_url_for_with_invalid_parameter(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("url-for", invalid_param="value")
        e.match('Invalid parameters provided for url-for')

def test_url_for_with_empty_string(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("url-for", two_letter_string="")
        e.match('Value "" for parameter `two_letter_string` does not satisfy pattern ^[A-z]{2}$')

def test_url_for_with_special_characters(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("url-for", two_letter_string="!@")
        e.match('Value "!@" for parameter `two_letter_string` does not satisfy pattern ^[A-z]{2}$')