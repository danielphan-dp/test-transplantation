import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for_basic(app):
    assert app.url_for('url_for') == '/url-for'

def test_url_for_with_external(app):
    assert app.url_for('url_for', _external=True) == 'http://localhost/url-for'

def test_url_for_with_unknown_host(app):
    with pytest.raises(ValueError) as e:
        app.url_for('url_for', _host='unknown.com')
    assert str(e.value).startswith("Requested host (unknown.com) is not available for this route")

def test_url_for_with_ambiguous_host(app):
    @app.route("/test", name="test_route", host=["example.com", "test.example.com"])
    def test_route(request):
        return text("test route")
    
    assert app.url_for("test_route") == "/test"
    
    with pytest.raises(ValueError) as e:
        app.url_for("test_route", _external=True)
    assert str(e.value).startswith("Host is ambiguous")

def test_url_for_with_params(app):
    @app.route("/params/<param>", name="param_route")
    def param_route(request, param):
        return text(f"Param: {param}")

    assert app.url_for("param_route", param="value") == "/params/value"