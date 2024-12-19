import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('proxy', ['', 'proxy', 'servername'])
def test_url_for(app: Sanic, proxy: str):
    @app.route('/test-url-for')
    def test_url_for_handler(request):
        return text('test-url-for')

    app.config.FORWARDED_SECRET = proxy
    app.config.SERVER_NAME = (
        "https://example.com" if proxy == "servername" else ""
    )

    request, response = app.test_client.get('/test-url-for')
    assert response.status == 200
    assert response.text == 'test-url-for'

    url = app.url_for('test_url_for_handler')
    assert url == '/test-url-for'
    
    if proxy == "servername":
        assert url.startswith("https://example.com")
    else:
        assert url.startswith("http://127.0.0.1") or url.startswith("http://localhost")