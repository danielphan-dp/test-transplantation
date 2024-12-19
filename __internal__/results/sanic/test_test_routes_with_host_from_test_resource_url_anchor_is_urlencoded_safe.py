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

def test_url_for_external(app):
    app.config.update({"SERVER_NAME": "example.com"})
    assert app.url_for('url_for', _external=True) == 'http://example.com/url-for'

def test_url_for_with_query_params(app):
    assert app.url_for('url_for', param1='value1', param2='value2') == '/url-for?param1=value1&param2=value2'

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(Exception) as e:
        app.url_for('non_existent_endpoint')
        assert str(e.value) == "Endpoint with name `non_existent_endpoint` was not found"

def test_url_for_with_host(app):
    @app.route("/", name="hostindex", host="example.com")
    @app.route("/path", name="hostpath", host="path.example.com")
    def index(request):
        pass

    assert app.url_for("hostindex") == "/"
    assert app.url_for("hostpath") == "/path"
    assert app.url_for("hostindex", _external=True) == "http://example.com/"
    assert app.url_for("hostpath", _external=True) == "http://path.example.com/path"