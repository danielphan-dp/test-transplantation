import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.mark.parametrize('proxy', ['', 'proxy', 'servername'])
def test_url_for(app: Sanic, proxy: str):
    app.config.FORWARDED_SECRET = proxy
    app.config.SERVER_NAME = (
        "https://example.com" if proxy == "servername" else ""
    )

    @app.route('/url-for')
    def url_for_handler(request: Request):
        return text('url-for')

    url = app.url_for('url_for_handler')
    assert url == 'http://127.0.0.1/url-for' if proxy == '' else 'https://example.com/url-for'

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

    with pytest.raises(Exception) as e:
        app.url_for('non_existent_handler')
        assert "Endpoint with name `app.non_existent_handler` was not found" in str(e.value)