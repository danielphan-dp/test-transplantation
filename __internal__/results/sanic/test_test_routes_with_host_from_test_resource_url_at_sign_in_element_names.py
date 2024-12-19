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
    assert app.url_for('url-for') == '/url-for'

def test_url_for_external(app):
    app.config.update({"SERVER_NAME": "example.com"})
    assert app.url_for('url-for', _external=True) == 'http://example.com/url-for'

def test_url_for_with_query_params(app):
    assert app.url_for('url-for', param1='value1', param2='value2') == '/url-for?param1=value1&param2=value2'

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(Exception) as e:
        app.url_for('non_existent_endpoint')
        assert str(e.value) == "Endpoint with name `non_existent_endpoint` was not found"

def test_url_for_with_different_hosts(app):
    @app.route("/hosted-url", name="hosted", host="test.example.com")
    def hosted(request):
        return text('hosted-url')

    assert app.url_for("hosted") == "/hosted-url"
    assert app.url_for("hosted", _external=True) == "http://test.example.com/hosted-url"