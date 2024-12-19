import asyncio
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

def test_url_for(app):
    # Test basic URL generation
    assert app.url_for('url_for') == '/url-for'
    
    # Test with external flag
    assert app.url_for('url_for', _external=True) == 'http://localhost/url-for'
    
    # Test with unknown host
    with pytest.raises(ValueError) as e:
        app.url_for('url_for', _host='unknown.com')
    assert str(e.value).startswith("Requested host (unknown.com) is not available for this route")
    
    # Test with ambiguous host
    @app.route('/url-for', host=["example.com", "path.example.com"])
    def url_for_multiple_hosts(request):
        return text('url-for-multiple-hosts')
    
    with pytest.raises(ValueError) as e:
        app.url_for('url_for_multiple_hosts', _external=True)
    assert str(e.value).startswith("Host is ambiguous")
    
    # Test valid host
    assert app.url_for('url_for_multiple_hosts', _host='example.com') == 'http://example.com/url-for'