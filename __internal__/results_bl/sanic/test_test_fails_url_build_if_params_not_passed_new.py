import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for_returns_correct_response(app):
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(ValueError) as e:
        app.url_for("non_existent_route")
        assert e.match("No route found for non_existent_route")

def test_url_for_with_scheme_and_external(app):
    with pytest.raises(ValueError) as e:
        app.url_for("url-for", _scheme="http")
        assert e.match("When specifying _scheme, _external must be True")

def test_url_for_with_external(app):
    url = app.url_for("url-for", _external=True)
    assert url.startswith("http://") or url.startswith("https://")