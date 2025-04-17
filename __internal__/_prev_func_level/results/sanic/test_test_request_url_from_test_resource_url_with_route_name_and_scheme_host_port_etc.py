import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.mark.parametrize('proxy', ['', 'proxy', 'servername'])
def test_url_for_with_proxy(app: Sanic, proxy: str):
    @app.route('/url-for')
    def url_for(request: Request):
        return text('url-for')

    app.config.SERVER_NAME = (
        "https://example.com" if proxy == "servername" else ""
    )
    
    expected_url = f"http://{app.config.SERVER_NAME}/url-for" if proxy == "servername" else "http://127.0.0.1/url-for"
    
    url = app.url_for('url_for', _external=True)
    assert url == expected_url

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "url-for"

def test_fails_if_endpoint_not_found(app: Sanic):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_endpoint")
        assert "Endpoint with name `non_existent_endpoint` was not found" in str(e.value)

def test_url_for_with_additional_params(app: Sanic):
    @app.route('/url-with-params/<param>')
    def url_with_params(request: Request, param: str):
        return text(f'param: {param}')

    url = app.url_for('url_with_params', param='test')
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "param: test"