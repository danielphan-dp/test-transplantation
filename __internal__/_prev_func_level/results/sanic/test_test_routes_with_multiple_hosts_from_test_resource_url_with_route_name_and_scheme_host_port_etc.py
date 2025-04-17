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
    app.config.update({"SERVER_NAME": "example.com"})
    assert app.url_for('url_for', _external=True) == 'http://example.com/url-for'

def test_url_for_with_unknown_host(app):
    with pytest.raises(ValueError) as e:
        app.url_for('url_for', _host='unknown.com')
    assert str(e.value).startswith("Requested host (unknown.com) is not available for this route")

def test_url_for_with_ambiguous_host(app):
    @app.route('/url-for', host=["example.com", "another.com"])
    def url_for(request):
        return text('url-for')
    
    with pytest.raises(ValueError) as e:
        app.url_for('url_for', _external=True)
    assert str(e.value).startswith("Host is ambiguous")

def test_url_for_with_additional_params(app):
    assert app.url_for('url_for', param1='value1', param2='value2') == '/url-for?param1=value1&param2=value2'