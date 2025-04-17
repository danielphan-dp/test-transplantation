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

def test_url_for_with_multiple_hosts(app):
    @app.route("/multi-host", name="multi", host=["example.com", "test.com"])
    def multi_host(request):
        return text('multi-host')

    assert app.url_for("multi", _host="example.com") == "http://example.com/multi-host"
    assert app.url_for("multi", _host="test.com") == "http://test.com/multi-host"

    with pytest.raises(ValueError) as e:
        app.url_for("multi", _external=True)
    assert str(e.value).startswith("Host is ambiguous")

def test_url_for_with_query_params(app):
    @app.route("/query", name="query")
    def query(request):
        return text('query')

    assert app.url_for("query", param1="value1", param2="value2") == "/query?param1=value1&param2=value2"